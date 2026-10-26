from pathlib import Path
import pytest
import fly_in


# define un pytest.Fixture para crear y procesar el archivo temporal
@pytest.fixture
def built_map(tmp_path: Path) -> Path:
    content = """
        nb_drones: 1

        start_hub: start 0 0 [max_drones=-2]
        end_hub: goal 3 0

        connection: start-goal
        """
    txt_file = tmp_path / "test.txt"
    txt_file.write_text(content, encoding="utf-8")
    return txt_file


# CASOS DE ERROR:
# tipo de zona inválido
@pytest.fixture
def type_zone_invalid(tmp_path: Path) -> Path:
    content = """
            nb_drones: 1

            start_hub: start 0 0
            hub: name 0 0 [zone=name]
            end_hub: goal 3 0

            connection: start-goal
            """
    txt_file = tmp_path / "type_zone_invalid.txt"
    txt_file.write_text(content, encoding="utf-8")
    return txt_file


# conexión duplicada
@pytest.fixture
def connection_invalid(tmp_path: Path) -> Path:
    content = """
            nb_drones: 1

            start_hub: start 0 0
            end_hub: goal 3 0

            connection: start-goal
            connection: goal-start
            """
    txt_file = tmp_path / "connection_invalid.txt"
    txt_file.write_text(content, encoding="utf-8")
    return txt_file


# la zona referenciada no existe
@pytest.fixture
def not_zone(tmp_path: Path) -> Path:
    content = """
            nb_drones: 1

            start_hub: start 0 0
            end_hub: goal 3 0

            connection: start-goal
            connection: start-name
            """
    txt_file = tmp_path / "test.txt"
    txt_file.write_text(content, encoding="utf-8")
    return txt_file


# capacidad no positiva
@pytest.fixture
def not_capability_connection(tmp_path: Path) -> Path:
    content = """
        nb_drones: 1

        start_hub: start 0 0
        end_hub: goal 3 0

        connection: start-goal [max_link_capacity=-2]
        """
    txt_file = tmp_path / "test.txt"
    txt_file.write_text(content, encoding="utf-8")
    return txt_file


# capacidad no positiva
@pytest.fixture
def not_capability_hub(tmp_path: Path) -> Path:
    content = """
        nb_drones: 1

        start_hub: start 0 0
        hub: name 1 0 [max_drones=-2]
        end_hub: goal 3 0

        connection: start-goal
        """
    txt_file = tmp_path / "test.txt"
    txt_file.write_text(content, encoding="utf-8")
    return txt_file


# nombre de zona con guion/espacio
@pytest.fixture
def name_zone_invalid(tmp_path: Path) -> Path:
    content = """
            nb_drones: 1

            start_hub: start 0 0
            hub: name-name 0 0
            end_hub: goal 3 0

            connection: start-goal
            """
    txt_file = tmp_path / "test.txt"
    txt_file.write_text(content, encoding="utf-8")
    return txt_file


# más de un start/end
@pytest.fixture
def start_invalid(tmp_path: Path) -> Path:
    content = """
            nb_drones: 1

            start_hub: start_1 0 0
            start_hub: start_2 1 0
            end_hub: goal 3 0

            connection: start_1-start_2
            connection: start_2-goal
            """
    txt_file = tmp_path / "test.txt"
    txt_file.write_text(content, encoding="utf-8")
    return txt_file


@pytest.fixture
def end_invalid(tmp_path: Path) -> Path:
    content = """
            nb_drones: 1

            start_hub: start 0 0
            end_hub: goal_1 2 0
            end_hub: goal_2 3 0

            connection: start-goal_1
            connection: goal_1-goal_2
            """
    txt_file = tmp_path / "test.txt"
    txt_file.write_text(content, encoding="utf-8")
    return txt_file


class TestMapParserErrors:
    def test_built_map(self, built_map) -> None:
        assert fly_in.MapParser(built_map) is not None

    def test_type_zone_invalid(self, type_zone_invalid):
        with pytest.raises(Exception):
            fly_in.MapParser(type_zone_invalid)

    def test_connection_invalid(self, connection_invalid):
        with pytest.raises(Exception):
            fly_in.MapParser(connection_invalid)

    def test_not_zone(self, not_zone):
        with pytest.raises(Exception):
            fly_in.MapParser(not_zone)

    def test_not_capability_connection(self, not_capability_connection):
        with pytest.raises(Exception):
            fly_in.MapParser(not_capability_connection)

    def test_not_capability_hub(self, not_capability_hub):
        with pytest.raises(Exception):
            fly_in.MapParser(not_capability_hub)

    def test_name_zone_invalid(self, name_zone_invalid):
        with pytest.raises(Exception):
            fly_in.MapParser(name_zone_invalid)

    def test_start_invalid(self, start_invalid):
        with pytest.raises(Exception):
            fly_in.MapParser(start_invalid)

    def test_end_invalid(self, end_invalid):
        with pytest.raises(Exception):
            fly_in.MapParser(end_invalid)
