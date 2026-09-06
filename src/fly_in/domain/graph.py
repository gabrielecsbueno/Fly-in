from .connection import Connection
from .zone import Zone
from typing import Union


class Graph():
    """
    La clase Graph construye un grafo a partir del mapa.

    Parameters
    ----------
    zones: list[Zone]
        Lista de objetos Zone.
    connections: list[Connection]
        Lista de objetos Connection.
    """
    def __init__(
            self,
            zones: list[Zone],
            connections: list[Connection]
            ) -> None:

        self.zones = zones
        self.connections = connections

    def get_neighbors(self, zone: Zone) -> list[Zone]:
        """
        Busca las zonas alcanzables directamente desde la zona recibida.

        Parameters
        ----------
        zone: Zone
            La zona de la que se buscan los vecinos.

        Returns
        -------
        Una lista de zonas vecinas de la zona recibida.
        """

        # busca el nombre de las zonas vecinas en las conexiones
        neighbor_names: list[str] = [
            c.zone2_name if c.zone1_name == zone.name else c.zone1_name
            for c in self.connections
            if c.zone1_name == zone.name or c.zone2_name == zone.name
        ]

        return [self.get_zone(name) for name in neighbor_names]

    def get_connection(self, z1: Zone, z2: Zone) -> Union[Connection, None]:
        """
        Busca la conexión entre dos zonas (para conocer su capacidad).

        Parameters
        ----------
        z1: Zone
            La primera zona a buscar.
        z2: Zone
            La segunda zona a buscar.

        Returns
        -------
        La conexión entre ellas si existe, si no, None.
        """

        return next(
            (
                c
                for c in self.connections
                if (
                    c.zone1_name == z1.name
                    and c.zone2_name == z2.name
                    )
                or (
                    c.zone1_name == z2.name
                    and c.zone2_name == z1.name
                    )
            ), None
        )

    def get_zone(self, name: str) -> Zone:
        """
        Busca la zona por el nombre indicado.

        Parameters
        ----------
        name: str
            El texto con el posible nombre de la zona.

        Returns
        -------
        La instancia de la zona.

        Raises
        -------
        ValueError
            Si ese nombre de zona no existe.
        """

        zone = next(
            (
                z
                for z in self.zones if z.name == name
            ),
            None
        )

        # si ese nombre de zona no existe, se lanza un error
        if zone is None:
            raise ValueError(f"No se encontró la zona '{name}'.")

        return zone

    @property
    def adjacency(self) -> dict[Zone, list[Zone]]:
        """
        Crea un diccionario con la lista de adyacencia de cada zona.

        Returns
        -------
        El grafo del mapa. Ej:
            zones_graph = {
                'A': ['C', 'B'],
                'B': ['A', 'D'],
                'C': ['A', 'D', 'E'],
                'D': ['B', 'C', 'E', 'F']
                'E': ['C', 'D', 'F']
                'F': ['D', 'E']
            }
        """

        return {zone: self.get_neighbors(zone) for zone in self.zones}
