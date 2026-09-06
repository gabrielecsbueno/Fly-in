from dataclasses import dataclass


@dataclass(frozen=True)
class Connection:
    """
    Instancia inmutable (frozen) de una conexión bidireccional (arista)
    entre dos zonas.

    Parameters
    ----------
    zone1_name : str
        Nombre de la zona 1.
    zone2_name : str
        Nombre de la zona 2.
    max_link_capacity : int (opcional, por defecto 1)
        Número máximo de drones que pueden atravesar esta conexión
        al mismo tiempo.
    """
    zone1_name: str
    zone2_name: str
    max_link_capacity: int = 1
