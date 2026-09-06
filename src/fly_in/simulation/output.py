from dataclasses import dataclass
from ..parsing.map_parser import MapParser
from ..domain.graph import Graph
from ..domain.zone import Zone
from ..domain.drone import Drone


@dataclass
class MapsResult:
    """
    Datos de una simulación completa, listos para ser renderizados.

    Parameters
    ----------
    file : str
        Ruta del archivo de mapa que generó este resultado.
    map_obj : MapParser
        El mapa ya analizado.
    graph : Graph
        El grafo del mapa.
    drones : list[Drone]
        Los drones del mapa (con su estado final, tras la simulación).
    zones : list[Zone]
        Todas las zonas del mapa.
    start : Zone
        La zona de inicio.
    end : Zone
        La zona de destino.
    adjacency : dict[Zone, list[Zone]]
        La lista de adyacencia del grafo.
    n_turns : int
        Número total de turnos que tardó la simulación.
    drone_positions_per_turn : list[list[tuple[Drone, list[Zone], str]]]
        Una entrada por turno (empezando por el turno 0, la posición
        inicial); cada una es una lista de (drone, posición, estado)
        para todos los drones en ese momento.
    turn_results : list[list[str]]
        La salida de cada turno, en el formato del enunciado
        (D<id>-<zona> o D<id>-<zona1>-<zona2>).
    """
    file: str
    map_obj: MapParser
    graph: Graph
    drones: list[Drone]
    zones: list[Zone]
    start: Zone
    end: Zone
    adjacency: dict[Zone, list[Zone]]
    n_turns: int
    drone_positions_per_turn: list[list[tuple[Drone, list[Zone], str]]]
    turn_results: list[list[str]]

    def show_benchmarks(self) -> None:
        """
        Imprime en consola el total de turnos, el costo total del
        camino (suma de los costos de zona de cada movimiento, sin
        contar de nuevo las travesías restricted de 2 turnos) y
        cuántos drones se movieron en cada turno.
        """
        print(f"Mapa '{self.file}'")
        print()

        print(f" - Número total de turnos: {self.n_turns} turnos")
        print(" - Costo total del camino: ", end='')
        turn_zones = [
            self.graph.get_zone(drone.split('-')[1])
            for turn in self.turn_results
            for drone in turn
            if len(drone.split('-')) == 2
        ]
        cost = sum(c.zone_type.get_turn for c in turn_zones)
        print(f"{cost}*")

        print(" - Número de drones movidos por turno: ")
        for i, turn in enumerate(self.turn_results, 1):
            drone_ids = ', '.join(drone.split('-')[0] for drone in turn)
            print(f"     - Turno {i}: {len(turn)} drones ({drone_ids})")

        print()
        print("*(suma de los costos de movimiento ponderados de todos "
              "los drones)")
