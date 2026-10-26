from fly_in import Zone, ZoneType


def build_zones() -> list[Zone]:
    return [
        Zone(name="A", x=0, y=1),
        Zone(name="B", x=1, y=2, zone_type=ZoneType.blocked),
        Zone(name="C", x=2, y=3, zone_type=ZoneType.normal, max_drones=2),
        Zone(name="D", x=3, y=4, zone_type=ZoneType.restricted),
        Zone(name="E", x=4, y=5, color='blue')
        ]


class TestClassZones:
    def test_zone(self) -> None:
        assert build_zones()

    def test_movement_cost_by_zone_type(self) -> None:
        assert ZoneType.normal.get_turn == 1
        assert ZoneType.priority.get_turn == 1
        assert ZoneType.restricted.get_turn == 2
        assert ZoneType.blocked.get_turn == 0
