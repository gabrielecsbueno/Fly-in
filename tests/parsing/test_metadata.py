import fly_in


def build_metadata_zone() -> fly_in.Metadata:
    return fly_in.Metadata(
        '[zone=restricted color=red max_drones=2]',
        ['zone', 'color', 'max_drones'],
        []
    )


def build_metadata_zone_start_end() -> fly_in.Metadata:
    return fly_in.Metadata(
        '[zone=restricted color=red max_drones=2]',
        ['zone', 'color', 'max_drones'],
        ['max_drones']
    )


def build_metadata_connection() -> fly_in.Metadata:
    return fly_in.Metadata(
        '[max_link_capacity=1]',
        ['max_link_capacity'],
        []
    )


class TestMetadata:
    def test_metadata_zone(self) -> None:
        data = build_metadata_zone().metadata
        assert data['zone_type'] == fly_in.ZoneType.restricted
        assert data['color'] == 'red'
        assert data['max_drones'] == 2

    def test_metadata_zone_start_end(self) -> None:
        data = build_metadata_zone_start_end().metadata
        assert 'max_drones' not in data

    def test_metadata_connection(self) -> None:
        data = build_metadata_connection().metadata
        assert data['max_link_capacity'] == 1
