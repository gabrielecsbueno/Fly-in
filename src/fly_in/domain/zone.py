from typing import Union
from dataclasses import dataclass
from .zone_type import ZoneType


@dataclass(frozen=True)
class Zone:
    """
    Instancia inmutable (frozen) que define una zona en el mapa.

    Parameters
    ----------
    name : str
        Nombre de la zona.
    x : int
        Coordenada x del mapa.
    y : int
        Coordenada y del mapa.
    zone_type : ZoneType (opcional)
        Define el tipo de zona y su costo en turnos.
    color : str (opcional)
        Define el color de la zona, usado para la representación visual.
    max_drones : int (opcional)
        Número máximo de drones que pueden estar en esta zona al mismo
        tiempo.
    """
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.normal
    color: Union[str, None] = None
    max_drones: int = 1
