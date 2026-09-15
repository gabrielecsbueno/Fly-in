from typing import Any
from ..domain.zone_type import ZoneType


class Metadata:
    """
    Lee la cadena de metadatos y construye el objeto según la lista de
    claves recibidas en valid_keys.

    Parameters
    ----------
    metadata_value: str
        Texto con las claves y valores recibidos del archivo.
    valid_keys: list[str]
        Claves válidas que se van a leer.
    ignore_keys: list[str]
        Claves que se van a ignorar durante la lectura.

    Raises
    ------
    ValueError
        Si se encuentra algún valor inválido al analizar los metadatos.
    """

    def __init__(
            self,
            metadata_value: str,
            valid_keys: list[str],
            ignore_keys: list[str]
            ) -> None:

        self.metadata_value = metadata_value.strip("[]")
        self.valid_keys = valid_keys
        self.ignore_keys = ignore_keys
        self._metadata: dict[str, Any] = {}

        self._init_metadata()

    @property
    def metadata(self) -> dict[str, Any]:
        """Devuelve el valor de los metadatos."""
        return self._metadata

    def _init_metadata(self) -> None:
        """
        Lee la cadena de metadatos y agrega la información de metadatos
        al diccionario.

        Raises
        ------
        ValueError
            Si se encuentra algún valor inválido al analizar los metadatos
            (clave no reconocida, tipo de zona inválido, o capacidad no
            positiva).
        """

        # split en el espacio
        pairs = self.metadata_value.split()

        # divido la cadena por los espacios para obtener cada par clave=valor
        for pair in pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)
                self._metadata[key] = value

        # comprueba si hay claves no aceptadas en los metadatos
        invalid_keys = [md
                        for md in self._metadata
                        if md not in self.valid_keys]

        if invalid_keys:
            raise ValueError(f'valor inválido {invalid_keys}')

        for key in list(self._metadata):

            # ignora las claves de la lista, aunque estén presentes
            if key in self.ignore_keys:
                self._metadata.pop(key)
                continue

            if key == 'zone':

                zone_value = self._metadata.pop('zone')

                # cambia la clave zone por el nombre válido de ZoneType
                try:
                    self._metadata['zone_type'] = ZoneType(zone_value)

                except ValueError:
                    raise ValueError(f'tipo de zona inválido {zone_value}')

            if key == 'max_drones' or key == 'max_link_capacity':

                try:
                    # convierte los dos valores a int
                    self._metadata[key] = int(self._metadata[key])

                except ValueError:
                    raise ValueError(f'{key} debe ser un número')

                else:
                    if self._metadata[key] <= 0:
                        raise ValueError(f'{key} debe ser un entero '
                                         'positivo')
