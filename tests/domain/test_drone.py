from fly_in import Drone, DroneStatus, Zone


def build_drones() -> list[Drone]:
    zone = Zone('A', 0, 0)
    return [
        Drone(id=1, position=[zone], status=DroneStatus.WAITING, history=[]),
        Drone(id=2, position=[zone], status=DroneStatus.MOVING, history=[]),
        Drone(id=3, position=[zone], status=DroneStatus.IN_TRANSIT,
              history=[]),
        Drone(id=4, position=[zone], status=DroneStatus.DELIVERED,
              history=[]),
        Drone(id=5, position=[zone], status=DroneStatus.IN_TRANSIT,
              history=[]),
        Drone(id=6, position=[zone], status=DroneStatus.WAITING, history=[]),
        Drone(id=7, position=[zone], status=DroneStatus.DELIVERED,
              history=[]),
        Drone(id=8, position=[zone], status=DroneStatus.DELIVERED,
              history=[]),
        Drone(id=9, position=[zone], status=DroneStatus.DELIVERED,
              history=[]),
        ]


class TestClassDrones:
    def test_drones(self) -> None:
        assert build_drones()
