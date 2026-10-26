# si se coloca más de un drone en una zona que solo acepta 1
# si se coloca más de un drone en una conexión que solo acepta 1
# si el drone a ocupar está en otra zona

import fly_in

GraphData = tuple[
    list[fly_in.Zone],
    list[fly_in.Connection],
    list[fly_in.Drone],
    fly_in.ZoneOccupancy,
    fly_in.ConnectionOccupancy,
]


def graph() -> GraphData:
    zone_list = [
        fly_in.Zone('A', 0, 0),
        fly_in.Zone('B', 1, 1),
        fly_in.Zone(
            'C', -1, 1, max_drones=2, zone_type=fly_in.ZoneType.priority
        ),
        fly_in.Zone('D', 0, 2, zone_type=fly_in.ZoneType.restricted),
        fly_in.Zone(
            'E', -1, 3, max_drones=2, zone_type=fly_in.ZoneType.restricted
        ),
        fly_in.Zone('F', 1, 4)
    ]

    connection_list = [
        fly_in.Connection(zone1_name="A", zone2_name="B"),
        fly_in.Connection(
            zone1_name="A", zone2_name="C", max_link_capacity=2
        ),
        fly_in.Connection(zone1_name="B", zone2_name="D"),
        fly_in.Connection(
            zone1_name="C", zone2_name="D", max_link_capacity=2
        ),
        fly_in.Connection(zone1_name="B", zone2_name="E"),
        fly_in.Connection(
            zone1_name="D", zone2_name="E", max_link_capacity=2
        )
    ]

    drone_list = [
        fly_in.Drone(1, [zone_list[0]], fly_in.DroneStatus.WAITING, []),
        fly_in.Drone(2, [zone_list[0]], fly_in.DroneStatus.WAITING, []),
        fly_in.Drone(3, [zone_list[0]], fly_in.DroneStatus.WAITING, []),
        fly_in.Drone(4, [zone_list[0]], fly_in.DroneStatus.WAITING, []),
    ]

    zone_occupancy = fly_in.ZoneOccupancy(
        zone_list, zone_list[0], zone_list[-1]
    )
    connection_occupancy = fly_in.ConnectionOccupancy(connection_list)
    return (zone_list, connection_list, drone_list, zone_occupancy,
            connection_occupancy)


def zone_has_space() -> bool:
    zone_list, _, _, zone_occupancy, _ = graph()

    # tiene que devolver TRUE
    return zone_occupancy.has_space(zone_list[1])


def zone_occupy() -> int:
    zone_list, _, drone_list, zone_occupancy, _ = graph()

    # no puede lanzar un error
    zone_occupancy.occupy(zone_list[1], drone_list[0])
    occupation_list_zone = zone_occupancy.occupation_list(zone_list[1])

    return len(occupation_list_zone)


def zone_release() -> None:
    zone_list, _, drone_list, zone_occupancy, _ = graph()

    # no puede lanzar un error
    zone_occupancy.release(zone_list[1], drone_list[0])


def zone_occupy_error() -> tuple[None, None]:
    zone_list, _, drone_list, zone_occupancy, _ = graph()

    # no puede lanzar un error
    return (zone_occupancy.occupy(zone_list[3], drone_list[0]),
            zone_occupancy.occupy(zone_list[3], drone_list[1]))


def zone_release_error() -> None:
    zone_list, _, drone_list, zone_occupancy, _ = graph()

    # no puede lanzar un error
    zone_occupancy.release(zone_list[2], drone_list[1])


class TestZoneOccupancy:
    def test_zone_has_space(self) -> None:
        assert zone_has_space() is True

    def test_zone_occupy(self) -> None:
        assert zone_occupy() == 1

    def test_zone_release(self) -> None:
        zone_release()

    def test_zone_occupy_error(self) -> None:
        assert zone_occupy_error() == (None, None)

    def test_zone_release_error(self) -> None:
        zone_release_error()


# pruebas de conexion

def connection_has_space() -> bool:
    _, connection_list, _, _, connection_occupancy = graph()

    # tiene que devolver TRUE
    return connection_occupancy.has_space(connection_list[1])


def connection_occupy() -> None:
    _, connection_list, drone_list, _, connection_occupancy = graph()

    # no puede lanzar un error
    connection_occupancy.occupy(connection_list[1], drone_list[0])


def connection_release() -> None:
    _, connection_list, drone_list, _, connection_occupancy = graph()

    # no puede lanzar un error
    connection_occupancy.release(connection_list[1], drone_list[0])


def connection_occupy_error() -> tuple[None, None]:
    _, connection_list, drone_list, _, connection_occupancy = graph()

    # no puede lanzar un error
    return (connection_occupancy.occupy(connection_list[2], drone_list[0]),
            connection_occupancy.occupy(connection_list[2], drone_list[1]))


def connection_release_error() -> None:
    _, connection_list, drone_list, _, connection_occupancy = graph()

    # no puede lanzar un error
    connection_occupancy.release(connection_list[3], drone_list[1])


class TestConnectionOccupancy:
    def test_connection_has_space(self) -> None:
        assert connection_has_space() is True

    def test_connection_occupy(self) -> None:
        connection_occupy()

    def test_connection_release(self) -> None:
        connection_release()

    def test_connection_occupy_error(self) -> None:
        assert connection_occupy_error() == (None, None)

    def test_connection_release_error(self) -> None:
        assert connection_release_error() is None
