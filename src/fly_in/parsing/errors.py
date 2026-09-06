class MapParseError(Exception):
    """
    Excepción lanzada cuando se encuentra algún error al analizar el mapa.

    Parameters
    ----------
    line : int
        Línea del archivo txt del mapa.
    error : str
        Mensaje de error específico.
    """
    def __init__(self, line: int, error: str = "Error desconocido"):
        message = f"Línea {line}: {error}"
        super().__init__(message)


class ValueDronesError(MapParseError):
    """
    Excepción lanzada cuando se encuentra un error en el número de
    drones del analizador del mapa.

    Parameters
    ----------
    line : int
        Línea del archivo txt del mapa.
    error : str
        Mensaje de error específico.
    """
    def __init__(self,
                 line: int,
                 error: str = "el valor de 'nb_drones' no es válido"
                 ):
        super().__init__(line, error)


class DuplicateConnectionError(MapParseError):
    """
    Excepción lanzada cuando el analizador encuentra una conexión
    duplicada en el mapa.
    """
    pass


class InvalidZoneTypeError(MapParseError):
    """
    Excepción lanzada cuando se encuentra un valor inválido en los
    parámetros de la zona, definida en el analizador del mapa.
    """
    pass


class InvalidConnectionError(MapParseError):
    """
    Excepción lanzada cuando se encuentra un valor inválido en los
    parámetros de la conexión, definida en el analizador del mapa.
    """
    pass


class ReadFileError(Exception):
    """
    Excepción lanzada debido a un error encontrado al leer el mapa.
    """
    pass
