from fly_in import Graph, Connection, Zone


def build_graph() -> Graph:
    zones = [
        Zone(name="A", x=0, y=1),
        Zone(name="B", x=1, y=2),
        Zone(name="C", x=2, y=3),
        Zone(name="D", x=3, y=4),
        Zone(name="E", x=4, y=5)
        ]

    connections = [
        Connection(zone1_name="A", zone2_name="B"),
        Connection(zone1_name="A", zone2_name="C"),
        Connection(zone1_name="B", zone2_name="D"),
        Connection(zone1_name="C", zone2_name="D"),
        Connection(zone1_name="B", zone2_name="E"),
        Connection(zone1_name="D", zone2_name="E")
    ]

    return Graph(zones=zones, connections=connections)


def check_graph_neighbors() -> list[Zone]:
    graph = build_graph()
    return graph.get_neighbors(graph.get_zone("A"))


def check_connections() -> Connection | None:
    graph = build_graph()
    return graph.get_connection(graph.get_zone("A"), graph.get_zone("B"))


def build_adjacency() -> dict[Zone, list[Zone]]:
    graph = build_graph()
    return graph.adjacency


class TestClassGraphs:
    def test_build_graph(self) -> None:
        assert build_graph()

    def test_check_graph_neighbors(self) -> None:
        assert check_graph_neighbors()

    def test_check_connections(self) -> None:
        assert check_connections()

    def test_build_adjacency(self) -> None:
        assert build_adjacency()
