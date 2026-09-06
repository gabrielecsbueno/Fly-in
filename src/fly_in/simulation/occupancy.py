from ..domain.zone import Zone
from ..domain.drone import Drone
from ..domain.connection import Connection


class ZoneOccupancy:
    """
    Controla cuántos drones hay en cada zona en cada turno, respetando
    max_drones. El start y el end nunca tienen límite de capacidad.

    Parameters
    ----------
    zones_list : list[Zone]
        Todas las zonas del mapa.
    start_zone : Zone
        La zona de inicio (sin límite de capacidad).
    end_zone : Zone
        La zona de destino (sin límite de capacidad).
    """
    def __init__(
        self,
        zones_list: list[Zone],
        start_zone: Zone,
        end_zone: Zone
    ) -> None:
        self.__start_zone = start_zone
        self.__end_zone = end_zone
        self.__occupation_list: dict[Zone, list[Drone]] = {
            zone: [] for zone in zones_list
        }

    def occupation_list(self, zone: Zone) -> list[Drone]:
        """Devuelve la lista de drones que ocupan la zona recibida."""
        return self.__occupation_list[zone]

    def has_space(self, zone: Zone) -> bool:
        """
        Indica si la zona todavía tiene espacio para un drone más.

        El start y el end siempre devuelven True, sin importar cuántos
        drones ya la ocupen.

        Raises
        ------
        ReferenceError
            Si la zona recibida no pertenece a este mapa.
        """
        if zone not in self.__occupation_list:
            raise ReferenceError('¡Esa zona no existe!')

        if (
            len(self.__occupation_list[zone]) < zone.max_drones or
            zone == self.__start_zone or
            zone == self.__end_zone
        ):
            return True
        else:
            return False

    def occupy(self, zone: Zone, drone: Drone) -> None:
        """
        Ocupa la zona con el drone recibido (si hay espacio y el drone
        todavía no la ocupa) y registra la zona en su historial.
        """
        if self.has_space(zone) and drone not in self.__occupation_list[zone]:
            self.__occupation_list[zone].append(drone)
            drone.history.append(zone)

    def release(self, zone: Zone, drone: Drone) -> None:
        """Libera el espacio que el drone ocupaba en la zona recibida."""
        if drone in self.__occupation_list[zone]:
            self.__occupation_list[zone].remove(drone)


class ConnectionOccupancy:
    """
    Controla cuántos drones atraviesan cada conexión al mismo tiempo,
    respetando max_link_capacity.

    Parameters
    ----------
    connections_list : list[Connection]
        Todas las conexiones del mapa.
    """
    def __init__(
        self,
        connections_list: list[Connection]
    ) -> None:
        self.__occupation_list: dict[Connection, list[Drone]] = {
            connection: [] for connection in connections_list
        }

    def has_space(self, connection: Connection) -> bool:
        """
        Indica si la conexión todavía tiene espacio para un drone más.

        Raises
        ------
        ReferenceError
            Si la conexión recibida no pertenece a este mapa.
        """
        if connection not in self.__occupation_list:
            raise ReferenceError('¡Esa conexión no existe!')

        if (len(
            self.__occupation_list[connection]
        ) < connection.max_link_capacity):
            return True
        return False

    def occupy(self, connection: Connection, drone: Drone) -> None:
        """Ocupa la conexión con el drone recibido, si hay espacio."""
        if (
            self.has_space(connection) and
            drone not in self.__occupation_list[connection]
        ):
            self.__occupation_list[connection].append(drone)

    def release(self, connection: Connection, drone: Drone) -> None:
        """Libera el espacio que el drone ocupaba en la conexión."""
        if drone in self.__occupation_list[connection]:
            self.__occupation_list[connection].remove(drone)
