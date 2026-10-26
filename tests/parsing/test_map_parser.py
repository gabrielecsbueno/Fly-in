from pytest import fixture
import fly_in


@fixture
def built_map(tmp_path):
    content = """
        # Camino lineal simple
        nb_drones: 1

        start_hub: start 0 0 [color=green]
        end_hub: goal 3 0 [color=red]

        connection: start-goal

        """
    txt_file = tmp_path / "test.txt"
    txt_file.write_text(content, encoding="utf-8")
    return fly_in.MapParser(txt_file)


class TestMapParser:
    def test_map_parser(self, built_map) -> None:
        assert built_map is not None

    def test_check_drones(self, built_map) -> None:
        assert built_map.drones

    def test_check_zones(self, built_map) -> None:
        assert built_map.zones

    def test_check_zone_start(self, built_map) -> None:
        assert built_map.zone_start

    def test_check_zone_end(self, built_map) -> None:
        assert built_map.zone_end

    def test_check_connections(self, built_map) -> None:
        assert built_map.connections

    def test_check_graph(self, built_map) -> None:
        assert built_map.graph
