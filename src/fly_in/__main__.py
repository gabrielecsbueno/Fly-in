from .app import start_maps
import sys
import pygame
from .ui.interface import Interface

if __name__ == "__main__":

    # usa un mapa por defecto
    if len(sys.argv) == 1:
        file = 'maps/config_map.txt'

    # si no, lee lo que se haya pasado
    elif len(sys.argv) == 2:
        file = sys.argv[1]

    else:
        print("\nError: solo se puede leer un mapa a la vez.")
        sys.exit(1)

    try:
        maps_result = start_maps([file])
        Interface(maps_result[0]).run()
        pygame.quit()

    except Exception as e:
        print(e)

    except KeyboardInterrupt:
        print("\nError: salida interrumpida inesperadamente.")
