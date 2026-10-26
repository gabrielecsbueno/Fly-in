import fly_in


def simple_graph() -> tuple[list[str], int]:
    zones = {
        'A': fly_in.Zone('A', 0, 0),
        'B': fly_in.Zone('B', 0, 1),
        'C': fly_in.Zone('C', 0, 2)
    }

    adjacency_list = {
        zones['A']:  [zones['B']],
        zones['B']:  [zones['A'], zones['C']],
        zones['C']:  [zones['B']]
    }

    return fly_in.pathfinding.dijkstra(
        zones['A'],
        zones['C'],
        adjacency_list)


def restricted_graph() -> tuple[list[str], int]:
    zones = {
        'A': fly_in.Zone('A', 0, 0),
        'B': fly_in.Zone('B', 1, 1, zone_type=fly_in.ZoneType.restricted),
        'C': fly_in.Zone('C', -1, 1),
        'D': fly_in.Zone('D', 0, 2, zone_type=fly_in.ZoneType.restricted),
        'E': fly_in.Zone('E', -1, 3),
        'F': fly_in.Zone('F', 1, 4),
    }

    adjacency_list = {
        zones['A']:  [zones['B'], zones['C']],
        zones['B']:  [zones['A'], zones['D']],
        zones['C']:  [zones['A'], zones['D'], zones['E']],
        zones['D']:  [zones['B'], zones['C'], zones['E'], zones['F']],
        zones['E']:  [zones['C'], zones['D'], zones['F']],
        zones['F']:  [zones['D'], zones['E']]
    }

    return fly_in.pathfinding.dijkstra(
        zones['A'],
        zones['F'],
        adjacency_list)


def blocked_graph() -> tuple[list[str], int]:
    zones = {
        'A': fly_in.Zone('A', 0, 0),
        'B': fly_in.Zone('B', 1, 1, zone_type=fly_in.ZoneType.blocked),
        'C': fly_in.Zone('C', -1, 1),
        'D': fly_in.Zone('D', 0, 2),
        'E': fly_in.Zone('E', -1, 3),
        'F': fly_in.Zone('F', 1, 4),
    }

    adjacency_list = {
        zones['A']:  [zones['B'], zones['C']],
        zones['B']:  [zones['A'], zones['D']],
        zones['C']:  [zones['A'], zones['D'], zones['E']],
        zones['D']:  [zones['B'], zones['C'], zones['E'], zones['F']],
        zones['E']:  [zones['C'], zones['D'], zones['F']],
        zones['F']:  [zones['D'], zones['E']]
    }

    return fly_in.pathfinding.dijkstra(
        zones['A'],
        zones['F'],
        adjacency_list)


class TestDijkstra:
    def test_dijkstra_simple(self) -> None:
        assert simple_graph() == (['A', 'B', 'C'], 2)

    def test_dijkstra_restricted(self) -> None:
        assert restricted_graph() == (['A', 'C', 'E', 'F'], 3)

    def test_dijkstra_blocked(self) -> None:
        assert blocked_graph() == (['A', 'C', 'D', 'F'], 3)
