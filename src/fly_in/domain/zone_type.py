from enum import Enum


class ZoneType(str, Enum):
    """
    Define los cuatro tipos de zona fijos del mapa.
    Enum basado en str para comparar con el valor de texto que viene
    del archivo de mapa (ej.: "restricted")

    Attributes
    ----------
        normal: Zona estándar, costo de movimiento de 1 turno (por defecto).
        blocked: Zona inaccesible.
        restricted: Una zona sensible o peligrosa.
        priority: Una zona preferida.
    """

    normal = "normal"
    blocked = "blocked"
    restricted = "restricted"
    priority = "priority"

    @property
    def get_turn(self) -> int:
        """
        Devuelve el costo en turnos de moverse hacia una zona de este tipo.

        Returns
        -------
        int
            0 si la zona es blocked (inaccesible, ningún camino puede
            usarla), 2 si es restricted, o 1 para normal/priority.
        """
        if self == ZoneType.blocked:
            return 0

        elif self == ZoneType.normal:
            return 1

        elif self == ZoneType.priority:
            return 1

        elif self == ZoneType.restricted:
            return 2
