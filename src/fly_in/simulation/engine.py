from ..parsing import MapParser
from ..domain.drone import Drone, DroneStatus
from ..domain.zone_type import ZoneType
from .occupancy import ZoneOccupancy, ConnectionOccupancy
from ..pathfinding.dijkstra import dijkstra


class SimulationEngine:
    """
    Motor de la simulación por turnos: mantiene el estado de todos los
    drones y avanza el mapa turno a turno hasta que todos son entregados.

    Parameters
    ----------
    map_obj : MapParser
        El mapa ya analizado (grafo, zonas, drones, start/end).
    max_turn_limit : int, opcional
        Número máximo de turnos antes de abortar la simulación (evita
        un bucle infinito si algún mapa quedara en punto muerto).
    """
    def __init__(self, map_obj: MapParser, max_turn_limit: int = 1000):
        self.graph = map_obj.graph
        self.start_zone = map_obj.zone_start
        self.end_zone = map_obj.zone_end
        self.zones = map_obj.zones
        self.drones = map_obj.drones
        self.adjacency = self.graph.adjacency

        self.zone_occupancy = ZoneOccupancy(
            map_obj.zones, map_obj.zone_start, map_obj.zone_end
        )
        for drone in self.drones:
            self.zone_occupancy.occupy(map_obj.zone_start, drone)
        self.connection_occupancy = ConnectionOccupancy(map_obj.connections)

        self._current_turn = 0
        self.max_turn_limit = max_turn_limit
        self.drone_paths = self._assign_paths_to_drones()

    @property
    def current_turn(self) -> int:
        """Devuelve el número del turno actual de la simulación."""
        return self._current_turn

    @property
    def finished(self) -> bool:
        """La simulación termina cuando todos han sido entregados."""
        return all(d.status == DroneStatus.DELIVERED for d in self.drones)

    def run_turn(self) -> list[str]:
        """Ejecuta UN turno y devuelve la línea de salida de ese turno."""
        self._current_turn += 1
        return self._process_turn()

    def run(self) -> list[list[str]]:
        """Ejecuta hasta que todos los drones lleguen, devuelve la salida
        de cada turno."""
        history = []

        while (
            not self.finished
            and self._current_turn < self.max_turn_limit
        ):
            history.append(self.run_turn())

        return history

    def _assign_paths_to_drones(self) -> dict[Drone, list[str]]:
        """
        Encuentra el mejor camino y variantes del mismo costo, ignorando
        una zona intermedia del mejor camino a la vez, y los distribuye
        entre los drones.
        """
        # encuentra el mejor camino entre inicio y fin y su costo
        best_path, best_cost = dijkstra(self.start_zone, self.end_zone,
                                        self.adjacency)
        # guarda la primera opción
        paths = [best_path]

        # ahora, para cada zona de la lista del mejor camino
        for intermediate_zone in best_path:
            # intenta encontrar otro camino sin importar el costo,
            # ignorando la zona intermedia ya encontrada
            try:
                alternative_path, alternative_cost = dijkstra(
                    self.start_zone, self.end_zone,
                    self.adjacency, intermediate_zone)
            except Exception:
                # no existe un camino alternativo
                continue
            # si el costo de este camino encontrado es igual al del
            # mejor camino
            if (
                alternative_cost == best_cost
                and alternative_path not in paths
            ):
                # lo guarda en la lista para distribuirlo después
                paths.append(alternative_path)

        # distribuye entre los drones
        return {
            drone: paths[i % len(paths)]
            for i, drone in enumerate(self.drones)
        }

    def _process_turn(self) -> list[str]:
        """
        Ejecuta un turno completo en dos fases, para que las salidas
        liberen capacidad antes de que se evalúen las llegadas.

        Fase 1 (salida): cada drone WAITING intenta avanzar al
        siguiente paso de su camino asignado, si la conexión (y, para
        una zona restricted de destino, también la zona) tiene
        espacio; si no hay espacio, el drone se queda WAITING y lo
        vuelve a intentar en el turno siguiente.

        Fase 2 (llegada): cada drone MOVING/IN_TRANSIT intenta
        ocupar su zona de destino; si lo logra, pasa a DELIVERED (si
        era el end) o vuelve a WAITING, liberando la conexión.

        Returns
        -------
        list[str]
            Una línea por cada drone que efectivamente se movió en este
            turno, en el formato D<id>-<zona> o D<id>-<zona1>-<zona2>
            (tránsito hacia una zona restricted).
        """
        turn_output: list[str] = []

        # fase 1: salida
        for drone in self.drones:

            # se salta el drone que ya fue entregado o va camino a una zona
            if (
                drone.status == DroneStatus.DELIVERED
                or drone.status == DroneStatus.MOVING
                or drone.status == DroneStatus.IN_TRANSIT
            ):
                continue

            # si ya estaba detenido antes
            if drone.status == DroneStatus.STOPPED:
                drone.status = DroneStatus.IN_TRANSIT
                continue

            current_zone = drone.position[0]
            drone_path = self.drone_paths[drone]

            # mira la próxima zona de la lista
            current_index = len(drone.history) - 1
            next_zone = self.graph.get_zone(drone_path[current_index + 1])

            # busca la conexión hacia la posible próxima zona
            destination_connection = self.graph.get_connection(
                current_zone, next_zone
            )

            if destination_connection is None:
                raise Exception

            # zona restricted: el drone NO puede esperar en la conexión
            # por espacio en el destino, así que el lugar debe garantizarse
            # (y reservarse) ya desde la salida, no solo en la llegada 2
            # turnos después
            if next_zone.zone_type == ZoneType.restricted:
                has_destination_space = self.zone_occupancy.has_space(
                    next_zone
                )
            else:
                has_destination_space = True

            # si la conexión (y la zona de destino, si es restricted)
            # tiene espacio
            if (
                self.connection_occupancy.has_space(destination_connection)
                and has_destination_space
            ):

                # ocupa la conexión con este drone
                self.connection_occupancy.occupy(
                    destination_connection, drone
                )

                # libera la zona en la que estaba
                self.zone_occupancy.release(current_zone, drone)

                # guarda la posición del drone para la próxima vez
                drone.position = [current_zone, next_zone]

                # si la próxima zona cuesta 2 turnos
                if next_zone.zone_type == ZoneType.restricted:
                    # reserva el lugar en el destino ya desde la salida
                    self.zone_occupancy.occupy(next_zone, drone)
                    # si no, se detiene y espera el próximo turno
                    drone.status = DroneStatus.STOPPED

                    turn_output.append(
                        f"D{drone.id}-{destination_connection.zone1_name}"
                        f"-{destination_connection.zone2_name}"
                    )

                # si cuesta 1 turno
                else:
                    drone.status = DroneStatus.MOVING

            # TODO: si no hay espacio en la conexión o en la zona restricted de
            # destino, se vuelve a intentar el próximo turno

        # ENTONCES: las current_zone quedan vacías y las
        # destination_connection quedan ocupadas

        # fase 2: llegada
        for drone in self.drones:
            if (
                drone.status == DroneStatus.STOPPED
                or drone.status == DroneStatus.DELIVERED
            ):
                continue

            if drone.status == DroneStatus.MOVING:

                # ve hacia dónde va
                destination_zone = drone.position[1]

                # busca de dónde viene el drone
                previous_zone = drone.position[0]

                # busca la conexión en la que está en este momento
                current_connection = self.graph.get_connection(
                    previous_zone, destination_zone
                )

                if current_connection is None:
                    raise Exception

                # comprueba si la zona de destino tiene capacidad para
                # el drone
                if self.zone_occupancy.has_space(destination_zone):
                    # ocupa la zona de destino con el drone
                    self.zone_occupancy.occupy(destination_zone, drone)

                    if destination_zone == self.end_zone:
                        drone.status = DroneStatus.DELIVERED

                    else:
                        drone.status = DroneStatus.WAITING

                    # libera la conexión en la que estaba
                    self.connection_occupancy.release(
                        current_connection, drone
                    )

                    drone.position = [destination_zone]
                    turn_output.append(f"D{drone.id}-{destination_zone.name}")

                else:
                    # si no hay espacio en la zona de destino, el drone se
                    # queda en la conexión, se vuelve a intentar en la fase 2
                    # del próximo turno
                    pass

            # fin del tránsito de 2 turnos para zona restricted
            elif drone.status == DroneStatus.IN_TRANSIT:

                # ve hacia dónde va
                destination_zone = drone.position[1]

                # busca de dónde viene el drone
                previous_zone = drone.position[0]

                # busca la conexión en la que está en este momento
                current_connection = self.graph.get_connection(
                    previous_zone, destination_zone
                )

                if current_connection is None:
                    raise Exception

                if destination_zone == self.end_zone:
                    drone.status = DroneStatus.DELIVERED

                else:
                    # marca el drone como que ya no se está moviendo
                    drone.status = DroneStatus.WAITING

                # libera la conexión en la que estaba
                self.connection_occupancy.release(
                    current_connection, drone
                )

                drone.position = [destination_zone]
                turn_output.append(f"D{drone.id}-{destination_zone.name}")

        return turn_output
