from .parsing.map_parser import MapParser
from .parsing.errors import ReadFileError
from .pathfinding.bfs import bfs
from .simulation.engine import SimulationEngine
from .simulation.output import MapsResult
from .domain.zone import Zone
from .domain.drone import Drone


def run_map(file: str) -> MapsResult:
    """
    Analiza un archivo de mapa y ejecuta la simulación completa hasta
    que todos los drones son entregados (o se alcanza el límite de
    turnos).

    Parameters
    ----------
    file : str
        Ruta del archivo de mapa a analizar y simular.

    Returns
    -------
    MapsResult
        Los datos completos de la simulación, listos para renderizar.

    Raises
    ------
    ReadFileError
        Si el archivo no puede leerse, o si no existe un camino entre
        el inicio y el final del mapa.
    """
    parsed_map = MapParser(file)
    graph = parsed_map.graph
    start = parsed_map.zone_start
    end = parsed_map.zone_end
    drones = parsed_map.drones
    zones = parsed_map.zones

    if not graph:
        raise ReadFileError('No fue posible leer el archivo:', file)

    adjacency_list = graph.adjacency

    # comprobamos si existe un camino entre el inicio y el final
    try:
        bfs(start, end, adjacency_list)
    except ValueError:
        raise ReadFileError(
            f'El mapa {file} no tiene conexión entre el inicio y el final'
        )

    # crea el objeto de simulación de turnos, todavía sin iniciar los turnos
    engine = SimulationEngine(parsed_map)

    turn_results: list[list[str]] = []
    drone_positions_per_turn: list[list[tuple[Drone, list[Zone], str]]] = []

    # guarda la posición inicial de cada drone
    drone_positions_per_turn.append([
        (
            drone,
            [zone for zone in drone.position],
            str(drone.status)
        )
        for drone in drones
    ])

    # ejecuta la simulación hasta que todos los drones terminen
    while (not engine.finished
           and engine.current_turn < engine.max_turn_limit):
        # ejecuta y guarda el resultado de este turno
        turn_results.append(engine.run_turn())

        # guarda la posición de todos los drones
        drone_positions_per_turn.append([
            (
                drone,
                [zone for zone in drone.position],
                str(drone.status)
            )
            for drone in drones
        ])

    return MapsResult(
        file=file,
        map_obj=parsed_map,
        graph=graph,
        drones=drones,
        zones=zones,
        start=start,
        end=end,
        adjacency=adjacency_list,
        n_turns=engine.current_turn,
        drone_positions_per_turn=drone_positions_per_turn,
        turn_results=turn_results
    )


def start_maps(files: list[str]) -> list[MapsResult]:
    """
    Ejecuta run_map para cada archivo recibido, y salta (imprimiendo
    el error) cualquier mapa que no pueda leerse.

    Parameters
    ----------
    files : list[str]
        Rutas de los archivos de mapa a analizar y simular.

    Returns
    -------
    list[MapsResult]
        El resultado de cada mapa que pudo ser leído y simulado.
    """
    maps_result: list[MapsResult] = []

    for file in files:
        try:
            maps_result.append(run_map(file))
        except ReadFileError as err:
            print(err)

    return maps_result
