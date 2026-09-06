from .zone import Zone
from enum import Enum
from typing import Union


class DroneStatus(str, Enum):
    """
    Representa los estados posibles de un drone.

    Attributes
    ----------
    WAITING
        El drone está parado en una zona (inicial o intermedia) y todavía
        no intentó moverse en el turno actual.
    MOVING
        El drone salió de su zona hacia un movimiento de 1 turno; en la
        fase de llegada del mismo turno intentará ocupar el destino.
    STOPPED
        El drone salió hacia una zona restricted (viaje de 2 turnos) y
        está en el primer turno de esa travesía: la conexión y el lugar
        de destino ya fueron reservados, solo falta esperar el turno
        siguiente.
    IN_TRANSIT
        El drone está en el segundo (y último) turno de un viaje hacia
        una zona restricted; en la fase de llegada de este turno
        finalmente ocupa el destino ya reservado.
    DELIVERED
        El drone llegó a la zona de destino y ya no es rastreado.
    """
    WAITING = 'waiting'
    MOVING = 'moving'
    STOPPED = 'stopped'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'


class Drone:
    """
    Define un drone.

    Parameters
    ----------
    id : int
        Número de identificación del drone.
    position : list[Zone]
        Posición actual del drone.
    status : DroneStatus
        Estado actual del drone.
    history : list[Union[Zone, None]]
        Historial de posiciones (zonas) por las que ya pasó el drone.
    """

    def __init__(
        self,
        id: int,
        position: list[Zone],
        status: DroneStatus,
        history: list[Union[Zone, None]],
    ):
        self.__id = id
        self.__position = position
        self.__status = status
        self.__history = history

    @property
    def id(self) -> int:
        """Devuelve el valor del ID del drone."""
        return self.__id

    @property
    def position(self) -> list[Zone]:
        """Devuelve la posición del drone en el mapa."""
        return self.__position

    @position.setter
    def position(self, position: list[Zone]) -> None:
        """Guarda la posición del drone en el mapa."""
        self.__position = position

    @property
    def status(self) -> DroneStatus:
        """Devuelve el estado actual del drone en el mapa."""
        return self.__status

    @status.setter
    def status(self, status: DroneStatus) -> None:
        """Guarda el estado actual del drone en el mapa."""
        self.__status = status

    @property
    def history(self) -> list[Union[Zone, None]]:
        """Devuelve el historial de posiciones del drone en el mapa."""
        return self.__history

    @history.setter
    def history(self, history: list[Union[Zone, None]]) -> None:
        """Guarda cada posición del drone en el historial."""
        self.__history = history
