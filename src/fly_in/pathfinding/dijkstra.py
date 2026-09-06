from ..domain.zone import Zone
from ..domain.zone_type import ZoneType
from typing import Union
import heapq


def dijkstra(
        start: Zone,
        end: Zone,
        adjacency: dict[Zone, list[Zone]],
        ignore_zone: str = ''
        ) -> tuple[list[str], int]:

    """
    Implementa Dijkstra (con heapq como cola de prioridad), considerando
    el costo en turnos de cada tipo de zona (normal=1, priority=1,
    restricted=2). Las zonas blocked nunca se expanden.

    Parameters
    ----------
    start : Zone
        Zona de inicio.
    end : Zone
        Zona de destino.
    adjacency : dict[Zone, list[Zone]]
        Lista de adyacencia del grafo (Graph.adjacency).
    ignore_zone : str, opcional
        Nombre de una zona a ignorar durante la búsqueda (usado para
        encontrar caminos alternativos que no pasen por ella).

    Returns
    -------
    tuple[list[str], int]
        Los nombres de las zonas del camino más barato, en orden, y su
        costo total en turnos.

    Raises
    ------
    ValueError
        Si no existe ningún camino entre start y end.
    """

    # 1. Construcción de la estructura del grafo
    # construye un diccionario con la lista de adyacencia y el costo en
    # turnos de cada zona
    dijkstra_graph = {}

    for zone, neighbors in adjacency.items():
        turns = {}
        for neighbor in neighbors:
            if neighbor.zone_type == ZoneType.blocked:
                continue
            turns[neighbor.name] = neighbor.zone_type.get_turn
        dijkstra_graph[zone.name] = turns

    # 2. Inicializa los costos con el valor entero máximo
    # diccionario para guardar los turnos más cortos
    shortest_turns: dict = {zone: int(100000) for zone in dijkstra_graph}
    shortest_turns[start.name] = 0

    # diccionario para reconstruir el camino más corto recorrido
    came_from: dict[str, Union[str, None]] = {
        zone: None for zone in dijkstra_graph
        }

    priority_queue = [(0, start.name)]

    while priority_queue:
        # extrae la zona con menor cantidad de turnos acumulados
        current_turn, current_zone = heapq.heappop(priority_queue)

        if current_zone == end.name:
            break

        if current_zone == ignore_zone:
            continue

        # si ya encontramos un camino más corto para esta zona, se ignora
        if current_turn > shortest_turns[current_zone]:
            continue

        # revisa los vecinos de la zona actual
        for neighbor_name, turn in dijkstra_graph[current_zone].items():
            # suma el costo acumulado
            new_turn = current_turn + turn

            # actualiza solo si encuentra un camino de menor costo
            if new_turn < shortest_turns[neighbor_name]:
                shortest_turns[neighbor_name] = new_turn
                came_from[neighbor_name] = current_zone
                # agrega a la cola de prioridad
                heapq.heappush(priority_queue, (new_turn, neighbor_name))

    if shortest_turns[end.name] >= 100000:
        raise ValueError(
            f"No existe un camino entre {start.name} y {end.name}"
            )

    # 4. reconstrucción del camino más corto
    path = []
    current: Union[str, None] = end.name
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    return (path, shortest_turns[end.name])
