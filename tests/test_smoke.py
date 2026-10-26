# prueba para confirmar que la suite de pruebas funciona

import pytest


# funciones a probar
def print_ok() -> str:
    return ("OK")


def errors() -> None:
    raise SystemExit(1)


# pruebas que se ejecutarán
# se puede crear una clase para las pruebas
class TestClass:
    def test_smoke(self) -> None:
        assert print_ok() == "OK"

    def test_mytest(self) -> None:
        with pytest.raises(SystemExit):
            errors()
