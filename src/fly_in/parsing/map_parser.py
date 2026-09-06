import re
from typing import Union, Any
from ..domain.drone import Drone, DroneStatus
from ..domain.zone import Zone
from ..domain.connection import Connection
from ..domain.graph import Graph
from .metadata import Metadata
from .errors import ValueDronesError, InvalidZoneTypeError, MapParseError
from .errors import InvalidConnectionError, DuplicateConnectionError


class MapParser:
    """
    Lee el archivo recibido usando un gestor de contexto, analiza el mapa,
    crea los drones (Drone), las zonas (Zone) y las conexiones entre
    zonas (Connection), y construye la lista de adyacencia (Graph).

    Parameters
    ----------
    map_path : str
        Ruta del archivo (txt) del mapa.
    """
    def __init__(self, map_path: str) -> None:
        self.map_path = map_path
        self._drones: list[Drone] = []
        self._zones: list[Zone] = []
        self._zone_start: Union[Zone, None] = None
        self._zone_end: Union[Zone, None] = None
        self._connections: list[Connection] = []
        self._graph: Union[Graph, None] = None

        # analiza el mapa
        self._parse_map()

    def _parse_map(self) -> dict[str, Any]:
        """
        Llama a los métodos que leen el archivo (txt) y construyen el grafo.

        Returns
        -------
            Un diccionario con las entradas 'graph', 'drones', 'zones',
            'zone_start' y 'zone_end'.
        """

        # lee el archivo (txt)
        self._read_map()
        # construye el grafo
        self._init_graph()

        return {
            'graph': self.graph,
            'drones': self.drones,
            'zones': self.zones,
            'zone_start': self.zone_start,
            'zone_end': self.zone_end
            }

    def _read_map(self) -> None:
        """
        Lee el archivo recibido, usando un gestor de contexto, línea por
        línea para analizar el mapa.

        Raises
        ------
        ValueDronesError
            Si el número de drones no es válido.
        InvalidZoneTypeError
            Si el formato de los parámetros de la zona no es válido.
        InvalidConnectionError
            Si el formato de los parámetros de la conexión no es válido.
        DuplicateConnectionError
            La conexión ya existe.
        MapParseError
            Cualquier otro error de análisis. Por ejemplo, una línea
            inválida o un archivo vacío.
        """
        with open(self.map_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, start=1):
                data = line.strip()

                # COMENTARIOS (#)
                if data.startswith('#') or not data:
                    continue

                # DRONES
                elif data.startswith('nb_drones:'):

                    try:
                        nb_drones = int(data[11:])

                    except ValueError:
                        raise ValueDronesError(i)

                    else:
                        self._init_drones(nb_drones, i)

                # ZONAS
                elif (data.startswith('start_hub:')
                      or data.startswith('hub:')
                      or data.startswith('end_hub:')):

                    content = data.split(':', 1)[1].strip()

                    zone_data = re.split(r'\s+', content, maxsplit=3)
                    # zone_data : <nombre> <x> <y> [metadatos]

                    if not zone_data:
                        raise InvalidZoneTypeError(
                            i, "no contiene información de la zona."
                            )

                    name = zone_data[0]

                    if '-' in name:
                        raise InvalidZoneTypeError(
                            i, f"nombre de zona inválido: {name}"
                            )

                    if any(z.name == name for z in self.zones):
                        raise InvalidZoneTypeError(
                            i, f"zona '{name}' duplicada"
                            )

                    try:
                        x = int(zone_data[1])
                        y = int(zone_data[2])

                    except ValueError:
                        raise InvalidZoneTypeError(
                            i, 'valor de coordenada inválido'
                            )

                    metadata: dict[str, Any] = {}
                    if len(zone_data) > 3 and zone_data[3]:
                        ignore_keys = [
                            'max_drones'
                            if (data.startswith('start_hub:')
                                or data.startswith('end_hub:'))
                            else ''
                            ]

                        metadata = self._init_metadata(
                            zone_data[3],
                            ['zone', 'color', 'max_drones'],
                            ignore_keys, i
                        )

                    # crea el objeto zona
                    self._init_zones(name, x, y, metadata)

                    # ZONA START
                    if data.startswith('start_hub:'):

                        if self._zone_start is not None:
                            raise MapParseError(
                                i, "solo puede haber un start_hub."
                                )

                        self.zone_start = self.zones[-1]

                    # ZONA END
                    elif data.startswith('end_hub:'):

                        if self._zone_end is not None:
                            raise MapParseError(
                                i, "solo puede haber un end_hub"
                                )

                        self.zone_end = self.zones[-1]

                # CONEXIONES
                elif data.startswith('connection:'):

                    content = data.split(':', 1)[1].strip()

                    # lo convierte en una lista de 2 o 3 (si hay metadatos)
                    connection = re.split(r"-|\s+(?=\[)", content, maxsplit=2)

                    zone1_name = connection[0]
                    zone2_name = connection[1]

                    # si no hay 2, o si los dos primeros están vacíos
                    if (
                            len(connection) < 2
                            or not zone1_name
                            or not zone2_name
                    ):
                        raise InvalidConnectionError(
                            i, f"formato '{connection}' inválido."
                        )

                    # si no existe ninguna zona con estos nombres
                    if not any(z.name == zone1_name for z in self.zones):
                        raise InvalidConnectionError(
                            i, f'la zona {zone1_name} no existe'
                        )

                    if not any(z.name == zone2_name for z in self.zones):
                        raise InvalidConnectionError(
                            i, f'la zona {zone2_name} no existe'
                            )

                    metadata = {}
                    if len(connection) > 2 and connection[2]:
                        metadata = self._init_metadata(
                            connection[2], ['max_link_capacity'], [], i
                        )

                    if any(
                        {c.zone1_name, c.zone2_name}
                        == {zone1_name, zone2_name}
                        for c in self._connections
                    ):
                        raise DuplicateConnectionError(
                            i,
                            f"conexión duplicada "
                            f"'{zone1_name}-{zone2_name}'"
                        )

                    # crea el objeto
                    self._init_connections(zone1_name, zone2_name, metadata)

                # LÍNEA INVÁLIDA
                else:
                    raise MapParseError(i,
                                        f"la línea {data} tiene un valor "
                                        "inválido")

        # si el archivo está vacío
        if self._zone_start is None or self._zone_end is None:
            raise MapParseError(1, "el mapa necesita exactamente un "
                                "start_hub y un end_hub")

        # coloca los drones ahí
        for drone in self._drones:
            drone.position = [self.zone_start]

    def _init_metadata(
            self,
            metadata: str,
            allowed_keys: list[str],
            ignore_keys: list[str],
            line: int) -> dict[str, Any]:
        """
        Llama a la clase Metadata.

        Parameters
        ----------
        metadata: str
            Texto con las claves y valores del archivo.
        allowed_keys: list[str]
            Claves válidas que se van a leer.
        ignore_keys: list[str]
            Claves que se van a ignorar durante la lectura.
        line: int
            Línea del archivo (txt). Para el manejo de errores.

        Returns
        -------
            Un diccionario con los metadatos.

        Raises
        ------
        InvalidZoneTypeError
            Si algún valor de la línea no es válido.
        """
        metadata_data: dict[str, Any] = {}
        if metadata:
            try:
                metadata_data = Metadata(
                    metadata,
                    allowed_keys,
                    ignore_keys
                    ).metadata

            except Exception as err:
                raise InvalidZoneTypeError(line, str(err))

        return metadata_data

    @property
    def graph(self) -> Union[Graph]:
        """Devuelve el objeto Graph"""
        if not self._graph:
            raise ValueError("el grafo no ha sido creado.")
        return self._graph

    def _init_graph(self) -> None:
        """Crea el objeto Graph con la lista de adyacencia."""
        self._graph = Graph(self._zones, self._connections)

    @property
    def drones(self) -> list[Drone]:
        """Devuelve la lista de objetos drone"""
        return self._drones

    def _init_drones(self, nb_drones: int, line: int) -> None:
        """Crea los drones a partir de la cantidad indicada"""

        if nb_drones <= 0:
            raise ValueDronesError(line,
                                   "el valor de 'nb_drones' no es válido.")

        for n in range(1, nb_drones+1):
            self._drones.append(Drone(
                id=n,
                position=[],
                history=[],
                status=DroneStatus.WAITING
                ))

    @property
    def zones(self) -> list[Zone]:
        """Devuelve la lista de objetos zona"""
        return self._zones

    def _init_zones(
            self,
            name: str,
            x: int,
            y: int,
            metadata: dict[str, Any]) -> None:
        """Crea los objetos zona a partir de los datos recibidos"""

        self.zones.append(Zone(name=name, x=x, y=y, **metadata))

    @property
    def zone_start(self) -> Zone:
        """Devuelve el objeto de la zona de inicio"""
        if not self._zone_start:
            raise ValueError("la zona de inicio no existe.")
        return self._zone_start

    @zone_start.setter
    def zone_start(self, zone: Zone) -> None:
        """Guarda el valor de la zona de inicio, en caso de que aún no
        haya sido definida."""

        if self._zone_start:
            raise ValueError("la zona de inicio ya fue definida.")

        self._zone_start = zone

    @property
    def zone_end(self) -> Zone:
        """Devuelve el objeto de la zona final"""
        if not self._zone_end:
            raise ValueError("la zona final no existe.")
        return self._zone_end

    @zone_end.setter
    def zone_end(self, zone: Zone) -> None:
        """Guarda el valor de la zona final, en caso de que aún no
        haya sido definida."""

        if self._zone_end:
            raise ValueError("la zona final ya fue definida.")

        self._zone_end = zone

    @property
    def connections(self) -> list[Connection]:
        """Devuelve una lista de objetos conexión"""
        return self._connections

    def _init_connections(self,
                          zone1_name: str,
                          zone2_name: str,
                          metadata: dict[str, Any]
                          ) -> None:
        """Crea los objetos conexión a partir de los datos recibidos"""
        self._connections.append(Connection(
            zone1_name=zone1_name,
            zone2_name=zone2_name,
            **metadata
        ))
