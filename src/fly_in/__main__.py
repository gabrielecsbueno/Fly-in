from .app import start_maps
import pygame
from .ui.interface import Interface
import argparse


def parse_args() -> argparse.Namespace:
    """
    Analiza los argumentos ingresados por el usuario en la linea de
    comandos.

    Returns
    -------
    argparse.Namespace
        El objeto Namespace que devuelve parse_args(), que guarda los
        valores de los argumentos de la linea de comandos.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--map",
                        default="maps/config_map.txt",
                        type=str, help="Archivo de entrada")

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()
    file = args.map

    try:
        maps_result = start_maps([file])
        Interface(maps_result[0]).run()
        pygame.quit()

    except Exception as e:
        print(e)

    except KeyboardInterrupt:
        print("\nError: salida interrumpida inesperadamente.")
