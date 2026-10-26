from fly_in import Connection


def build_connections() -> list[Connection]:
    return [
        Connection(zone1_name="A", zone2_name="B", max_link_capacity=10),
        Connection(zone1_name="A", zone2_name="C"),
        Connection(zone1_name="B", zone2_name="D"),
        Connection(zone1_name="C", zone2_name="D"),
        Connection(zone1_name="B", zone2_name="E"),
        Connection(zone1_name="D", zone2_name="E")
        ]


class TestClassConnections:
    def test_connections(self) -> None:
        assert build_connections()

    def test_default_max_link_capacity_is_one(self) -> None:
        connection = Connection(zone1_name="A", zone2_name="B")
        assert connection.max_link_capacity == 1
