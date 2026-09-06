import pygame
from typing import Any
from fly_in.domain.zone import Zone
from fly_in.domain.drone import Drone
from fly_in.simulation.output import MapsResult


class Interface:
    """
    Visualización gráfica (pygame) de una simulación ya ejecutada:
    dibuja el mapa, las conexiones y la posición de los drones en cada
    turno, con avance manual (K_RIGHT/K_LEFT) o automático
    (K_RETURN).

    Parameters
    ----------
    map_result : MapsResult
        El resultado completo de la simulación a visualizar.
    """
    def __init__(self, map_result: MapsResult) -> None:
        self.map_result = map_result

        pygame.init()

        # inicia la pantalla automáticamente al crear el objeto
        self._setup_display()

    def _setup_display(self) -> None:
        """Método privado para configurar la ventana y cargar
        los recursos visuales"""

        # define el tamaño de la ventana
        self.window_size = (2560, 1440)
        # self.window_size = (1280, 720)

        # crea una ventana
        self.screen = pygame.display.set_mode(self.window_size)

        # crea un objeto para ayudar a controlar el tiempo
        self.clock = pygame.time.Clock()

        # cambia el título de la ventana
        pygame.display.set_caption("Fly-in")

        # define las nuevas coordenadas de las zonas
        self.zone_coords, self.cell_size = self._get_screen_coords()

        # crea las variables de imagen que se usarán en el renderizado
        self.background_img = pygame.image.load(
            "src/fly_in/ui/assets/background(2560x1440).png"
        )
        # self.background_img = pygame.image.load(
        #     "src/fly_in/ui/assets/background(1280x720).png"
        # )

        self.normal_zone_images = [
            pygame.image.load("src/fly_in/ui/assets/zone_normal1.png"),
            pygame.image.load("src/fly_in/ui/assets/zone_normal2.png"),
            pygame.image.load("src/fly_in/ui/assets/zone_normal3.png"),
            pygame.image.load("src/fly_in/ui/assets/zone_normal4.png"),
            pygame.image.load("src/fly_in/ui/assets/zone_normal5.png"),
            pygame.image.load("src/fly_in/ui/assets/zone_normal6.png")
        ]

        self.blocked_zone_image = pygame.image.load(
            "src/fly_in/ui/assets/zone_blocked.png"
        )
        self.restricted_zone_image = pygame.image.load(
            "src/fly_in/ui/assets/zone_restricted.png"
        )
        self.priority_zone_image = pygame.image.load(
            "src/fly_in/ui/assets/zone_priority.png"
        )
        self.start_zone_image = pygame.image.load(
            "src/fly_in/ui/assets/zone_start.png"
        )
        self.end_zone_image = pygame.image.load(
            "src/fly_in/ui/assets/zone_end.png"
        )

        self.drone_images = [
            pygame.image.load("src/fly_in/ui/assets/drone1.png"),
            pygame.image.load("src/fly_in/ui/assets/drone2.png"),
            pygame.image.load("src/fly_in/ui/assets/drone3.png"),
            pygame.image.load("src/fly_in/ui/assets/drone4.png"),
            pygame.image.load("src/fly_in/ui/assets/drone5.png"),
            pygame.image.load("src/fly_in/ui/assets/drone6.png")
        ]

        # asigna un modelo distinto a cada drone
        self.drone_models = self._set_drone_models()

        # define los colores que se pueden usar
        self.colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'gray': (128, 128, 128),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255)
        }

        # fuente usada para los textos
        self.font_text = pygame.font.SysFont('Arial', 12)
        self.font_text_name = pygame.font.SysFont('Arial', 20)
        self.font_text_file = pygame.font.SysFont('Arial', 40)
        # self.font_text = pygame.font.SysFont('Arial', 6)
        # self.font_text_name = pygame.font.SysFont('Arial', 10)
        # self.font_text_file = pygame.font.SysFont('Arial', 20)

    def _set_drone_models(self) -> dict[Drone, Any]:
        """Define qué modelo de imagen se usará para cada drone"""
        drones = self.map_result.drones

        drone_models = {}

        i = 0

        for drone in drones:
            if i >= len(self.drone_images):
                i = 0
            drone_models[drone] = self.drone_images[i]
            i += 1

        return drone_models

    def run(self) -> None:
        """Inicia y mantiene el bucle principal de la interfaz"""
        running = True

        # para controlar el turno
        turn = 0

        # inicia el renderizado de la pantalla
        self._draw(0)

        while running:
            # revisa los eventos
            for event in pygame.event.get():
                # revisa si el usuario hizo clic en la X para cerrar
                # la ventana
                if event.type == pygame.QUIT:
                    running = False

                # revisa si el usuario presionó alguna tecla
                elif event.type == pygame.KEYDOWN:

                    # enter = K_RETURN
                    if event.key == pygame.K_RETURN:
                        for n in range(self.map_result.n_turns + 1):
                            # renderiza el mapa
                            self._draw(n)
                            self.show_turn(n)
                            pygame.time.wait(1000)

                    elif event.key == pygame.K_RIGHT:
                        turn += 1
                        if turn > self.map_result.n_turns:
                            turn = 0
                        self._draw(turn)
                        self.show_turn(turn)

                    elif event.key == pygame.K_LEFT:
                        turn -= 1
                        if turn < 0:
                            turn = self.map_result.n_turns
                        self._draw(turn)
                        self.show_turn(turn)

    def _draw(self, current_turn: int) -> None:
        """Dibuja todos los elementos visuales en la pantalla"""

        # llena la pantalla con una imagen
        self.screen.blit(self.background_img, self.background_img.get_rect())

        # dibuja las conexiones
        self._render_connections()

        # dibuja las zonas
        self._render_zones()

        # dibuja los drones de este turno
        self._render_drones_turns(current_turn)

        # escribe los textos de información en la pantalla
        self._render_info(current_turn)

        # actualiza la pantalla de Pygame
        pygame.display.flip()

        # limita los FPS a 60
        self.clock.tick(60)

    def _render_info(self, current_turn: int) -> None:
        """Escribe todos los textos de información de cada turno en
        la pantalla"""

        # número del turno actual
        text1 = self.font_text_file.render(
            str(f'Turno: {current_turn}'), True, self.colors['black']
        )
        self.screen.blit(text1, (50, 40))
        # self.screen.blit(text1, (25, 20))

        # salida de los turnos
        text2 = self.font_text_name.render(
                    str("turnos:"),
                    True,
                    self.colors['white']
        )
        position = (880, 80)
        # position = (440, 40)
        self.screen.blit(
            text2,
            (self.window_size[0] - position[0],
             self.window_size[1] - position[1])
        )
        position = (880, 60)
        # position = (440, 30)
        text3 = self.font_text_name.render(
            self.show_turn(current_turn),
            True,
            self.colors['white']
        )
        self.screen.blit(
            text3,
            (self.window_size[0] - position[0],
             self.window_size[1] - position[1])
        )

        # nombre de cada zona
        for zone, coord in self.zone_coords.items():

            zone_rect = pygame.Rect(coord, self.cell_size)

            text = self.font_text.render(zone.name, True, self.colors['white'])
            self.screen.blit(text, text.get_rect(midtop=zone_rect.midtop))

            # self.screen.blit(text, text.get_rect(center=zone_rect.center))

    def _render_zones(self) -> None:
        """Dibuja todas las zonas en la pantalla"""

        # proporción según el espacio de la zona
        ratio = 0.8

        # índice de la zona
        i = 0

        for zone, coord in self.zone_coords.items():

            # define el área que se va a dibujar
            zone_rect = pygame.Rect((coord[0]), coord[1], self.cell_size[0],
                                    self.cell_size[1])

            # define la imagen que se usará
            if zone.name == self.map_result.start.name:
                image = self.start_zone_image

            elif zone.name == self.map_result.end.name:
                image = self.end_zone_image

            elif zone.zone_type.name == 'blocked':
                image = self.blocked_zone_image

            elif zone.zone_type.name == 'priority':
                image = self.priority_zone_image

            elif zone.zone_type.name == 'restricted':
                image = self.restricted_zone_image

            elif zone.zone_type.name == 'normal':
                if i >= len(self.normal_zone_images):
                    i = 0
                image = self.normal_zone_images[i]
                i += 1

            # escala la imagen
            image_size = min(zone_rect.width, zone_rect.height) * ratio
            image = pygame.transform.scale(
                image,
                (image_size, image_size)
            )

            self.screen.blit(image, image.get_rect(center=zone_rect.center))

    def _render_connections(self) -> None:
        """Dibuja las líneas de conexión entre las zonas"""
        connections = self.map_result.adjacency

        for zone, neighbors in connections.items():
            zone_rect = pygame.Rect(self.zone_coords[zone], self.cell_size)

            for neighbor in neighbors:
                neighbor_rect = pygame.Rect(
                    self.zone_coords[neighbor],
                    self.cell_size
                )
                # line(superficie, color, inicio, fin)
                pygame.draw.line(self.screen,
                                 self.colors['gray'],
                                 zone_rect.center,
                                 neighbor_rect.center)

    def _render_drone(self, drone: Drone, x: int, y: int) -> None:
        """Dibuja el drone en la coordenada recibida"""
        ratio = 0.6

        # define el área
        zone_rect = pygame.Rect(x, y, self.cell_size[0], self.cell_size[1])

        image_size = min(zone_rect.width, zone_rect.height) * ratio

        # escala la imagen
        image = pygame.transform.scale(
            self.drone_models[drone],
            (image_size, image_size)
        )

        self.screen.blit(image, image.get_rect(midtop=zone_rect.midtop))
        # self.screen.blit(image, image.get_rect(center=zone_rect.center))

    def _render_drones_turns(self, current_turn: int) -> None:
        """Dibuja la posición de los drones en el turno correspondiente"""

        drone_positions = self.map_result.drone_positions_per_turn

        # obtiene la coordenada a la que debe ir
        next_turn_drone_positions = drone_positions[current_turn]

        for drone, position, _ in next_turn_drone_positions:

            # len 1 = zona
            if len(position) == 1:
                x, y = self.zone_coords[position[0]]

            # len 2 = conexión
            else:
                # coordenadas desde donde está saliendo
                x1, y1 = self.zone_coords[position[0]]
                # coordenadas hacia donde va
                x2, y2 = self.zone_coords[position[1]]
                # punto medio
                x = int((x1 + x2) / 2)
                y = int((y1 + y2) / 2)

            self._render_drone(drone, x, y)

    def _get_screen_coords(self) -> tuple[dict[Zone, tuple[int, int]],
                                          tuple[int, int]]:
        """Calcula las coordenadas de pantalla de las zonas, a partir de
        las coordenadas originales recibidas. Devuelve un diccionario con
        las zonas y sus nuevas coordenadas"""

        zones = self.map_result.zones

        # encuentra las coordenadas de menor y mayor valor
        min_x = min(zone.x for zone in zones)
        max_x = max(zone.x for zone in zones)
        min_y = min(zone.y for zone in zones)
        max_y = max(zone.y for zone in zones)

        # encuentra el número de filas necesarias
        n_lines = max_y - min_y + 1
        n_columns = max_x - min_x + 1

        # calcula los márgenes de la pantalla
        padding = 0.05
        padding_x = int(self.window_size[0] * padding)
        padding_y = int(self.window_size[1] * padding)

        # calcula el ancho del contenido
        content_width = self.window_size[0] - (padding_x * 2)

        # calcula la altura del contenido
        content_height = self.window_size[1] - (padding_y * 2)

        # guarda los valores reales de las coordenadas x e y
        order_x = {
            coord: index
            for index, coord in enumerate(range(min_x, max_x + 1))
        }
        order_y = {
            coord: index
            for index, coord in enumerate(range(max_y, min_y - 1, - 1))
        }

        # calcula la altura de la fila
        line_height = int(content_height / n_lines)

        # calcula el ancho de la columna
        column_width = int(content_width / n_columns)

        # guarda en un diccionario la zona y sus coordenadas de pantalla
        zone_screen_coords = {}
        for zone in zones:
            new_x = (order_x[zone.x] * column_width) + padding_x
            new_y = (order_y[zone.y] * line_height) + padding_y

            zone_screen_coords[zone] = (new_x, new_y)

        return zone_screen_coords, (column_width, line_height)

    def show_turn(self, turn: int) -> str:
        """Imprime y devuelve los movimientos de los drones del turno"""
        if turn != 0:
            result = ' '.join(self.map_result.turn_results[turn-1])
            print(result)
            return result
        else:
            return ''
