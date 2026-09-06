from ..domain.zone import Zone, ZoneType
from collections import deque
from typing import Union


def bfs(
        start: Zone,
        end: Zone,
        adjacency: dict[Zone, list[Zone]]
        ) -> list[str]:
    """
    Busca en anchura (BFS) el camino con menor número de saltos entre
    start y end, ignorando por completo las zonas blocked.

    Parameters
    ----------
    start : Zone
        Zona de inicio.
    end : Zone
        Zona de destino.
    adjacency : dict[Zone, list[Zone]]
        Lista de adyacencia del grafo (Graph.adjacency).

    Returns
    -------
    list[str]
        Los nombres de las zonas del camino encontrado, en orden,
        desde start hasta end.

    Raises
    ------
    ValueError
        Si no existe ningún camino entre start y end.
    """

    # cola (collections.deque - permite quitar del inicio en tiempo
    # constante)
    queue: deque[Zone] = deque([start])

    # diccionario para reconstruir el camino más corto recorrido
    came_from: dict[str, Union[str, None]] = {start.name: None}

    # conjunto de nombres ya visitados, para no procesar la misma zona 2x
    visited = set()
    visited.add(start.name)

    while queue:
        # extrae la zona más antigua, índice 0
        zone = queue.popleft()

        if zone.name == end.name:
            break

        for neighbor in adjacency[zone]:

            if neighbor.zone_type == ZoneType.blocked:
                continue

            if neighbor.name not in visited:
                # la marca como visitada
                visited.add(neighbor.name)
                # la agrega al camino
                came_from[neighbor.name] = zone.name
                # la agrega a la cola
                queue.append(neighbor)

    if end.name not in visited:
        raise ValueError(
            f"No existe un camino entre {start.name} y {end.name}"
            )

    # reconstruye el camino recorrido
    path = []
    current: Union[str, None] = end.name
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    return path
