from ..app import start_maps


def benchmark() -> None:
    """
    Ejecuta los mapas oficiales (easy/medium/hard/challenger) y muestra
    en consola, para cada uno, si el número de turnos obtenido cumple
    la meta de referencia del enunciado.
    """
    easy_files = [
        'maps/easy/01_linear_path.txt',
        'maps/easy/02_simple_fork.txt',
        'maps/easy/03_basic_capacity.txt'
    ]

    medium_files = [
        'maps/medium/01_dead_end_trap.txt',
        'maps/medium/02_circular_loop.txt',
        'maps/medium/03_priority_puzzle.txt'
    ]

    hard_files = [
        'maps/hard/01_maze_nightmare.txt',
        'maps/hard/02_capacity_hell.txt',
        'maps/hard/03_ultimate_challenge.txt'
    ]

    challenger_files = [
            'maps/challenger/01_the_impossible_dream.txt'
        ]

    def show() -> None:
        """Corre cada grupo de mapas y compara contra su meta de turnos."""
        print("-"*50)
        print("Rendimiento excepcional: ")
        print()

        # EASY
        print("Easy:")
        print("-"*50)
        easy_result = start_maps(easy_files)

        # imprime los benchmarks
        for n, result in enumerate(easy_result, 1):
            max_turns = [6, 8, 6]
            if result.n_turns <= max_turns[n-1]:
                print(f"\n\033[1;32m[ {n} ](≤ {max_turns[n-1]} turnos)\033[m")
            else:
                print(f"\n\033[31m[ {n} ](≤ {max_turns[n-1]} turnos)\033[m")
            result.show_benchmarks()
        print("-"*50)
        print()

        # MEDIUM
        print("Medium:")
        print("-"*50)
        medium_result = start_maps(medium_files)

        # imprime los benchmarks
        for n, result in enumerate(medium_result, 1):
            max_turns = [12, 15, 12]
            if result.n_turns <= max_turns[n-1]:
                print(f"\n\033[1;32m[ {n} ](≤ {max_turns[n-1]} turnos)\033[m")
            else:
                print(f"\n\033[31m[ {n} ](≤ {max_turns[n-1]} turnos)\033[m")
            result.show_benchmarks()
        print("-"*50)
        print()

        # HARD
        print("Hard:")
        print("-"*50)
        hard_result = start_maps(hard_files)

        # imprime los benchmarks
        for n, result in enumerate(hard_result, 1):
            max_turns = [30, 35, 45]
            if result.n_turns <= max_turns[n-1]:
                print(f"\n\033[1;32m[ {n} ](≤ {max_turns[n-1]} turnos)\033[m")
            else:
                print(f"\n\033[31m[ {n} ](≤ {max_turns[n-1]} turnos)\033[m")
            result.show_benchmarks()
        print("-"*50)
        print()

        # CHALLENGER
        print()
        print("Mapa Challenger: ")
        print("-"*50)
        challenger_result = start_maps(challenger_files)

        # imprime los benchmarks
        for n, result in enumerate(challenger_result, 1):
            if result.n_turns <= 45:
                print(f"\n\033[1;32m[ {n} ](≤ 45 turnos)\033[m")
            else:
                print(f"\n\033[31m[ {n} ](≤ 45 turnos)\033[m")
            result.show_benchmarks()
        print("-"*50)
        print()

    return show()


if __name__ == "__main__":
    try:
        benchmark()

    except Exception as e:
        print(e)

    except KeyboardInterrupt:
        print("\nError: salida interrumpida inesperadamente.")
