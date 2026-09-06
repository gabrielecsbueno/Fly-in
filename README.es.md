*Este proyecto ha sido creado como parte del currículo de 42 por [gabde-so](https://profile-v3.intra.42.fr/users/gabde-so)*

# **FLY_IN**

---

# Description

> Objetivo principal del proyecto: enrutamiento eficiente de drones autónomos

El proyecto **Fly-in es un sistema que enruta, de forma eficiente, una flota de drones desde una base central (inicio) hasta un lugar de destino (fin)**, navegando por esa red dinámica bajo un conjunto de restricciones estrictas y objetivos de optimización.

El mapa se recibe a partir de un archivo `.txt` pasado por argumento, o el `maps/config_map.txt` por defecto si no se indica ninguno.

El grafo se representa como una red de zonas conectadas, donde las conexiones definen los posibles caminos de movimiento entre las zonas.

## Estructura del Proyecto

```bash
fly_in/
├── maps/                       # mapas de ejemplo (easy/medium/hard/challenger) + mapa de prueba
├── src/
│   └── fly_in/                 # paquete Python principal
│       ├── __init__.py         # inicializador del paquete
│       ├── __main__.py         # punto de entrada (make run / make debug)
│       ├── app.py              # orquestador del programa
│       ├── domain/             # modelo de dominio: clases puras
│       │   ├── __init__.py
│       │   ├── zone_type.py    # Enum ZoneType, costo en turnos por tipo de zona
│       │   ├── zone.py         # clase Zone: datos estáticos de una zona del mapa
│       │   ├── connection.py   # clase Connection: une dos Zones, guarda max_link_capacity
│       │   ├── drone.py        # clase Drone: posición, estado e historial del drone
│       │   └── graph.py        # clase Graph/Network: zonas + conexiones, lista de adyacencia
│       ├── parsing/            # analizador del archivo de mapa
│       │   ├── __init__.py
│       │   ├── map_parser.py   # MapParser: lee el archivo línea a línea y construye el Graph
│       │   ├── metadata.py     # analizador de metadatos [clave=valor clave2=valor2]
│       │   └── errors.py       # MapParseError y otras excepciones propias del parser
│       ├── pathfinding/        # algoritmos para buscar el camino
│       │   ├── __init__.py
│       │   ├── dijkstra.py     # Dijkstra: menor costo total
│       │   └── bfs.py          # BFS: menor número de saltos
│       ├── simulation/         # motor de simulación
│       │   ├── __init__.py
│       │   ├── engine.py       # SimulationEngine: bucle principal de turnos
│       │   ├── occupancy.py    # ZoneOccupancy y ConnectionOccupancy: estado dinámico de ocupación
│       │   └── output.py       # MapsResult: guarda los datos de la simulación listos para renderizar
│       ├── ui/                 # visualización de la simulación
│       │   ├── assets/         # imágenes usadas en la visualización de pygame
│       │   ├── __init__.py
│       │   └── interface.py    # salida de pygame
│       └── bonus/
│           ├── __init__.py
│           └── benchmark.py
├── README.md
├── Makefile                    # install/run/debug/clean/lint/bonus
├── pyproject.toml              # dependencias (uv) y configuración de flake8/mypy/pytest
├── uv.lock                     # versiones exactas fijadas por uv (reproducibilidad)
└── .gitignore                  # artefactos de Python ignorados por Git
```

## Algorithm Choices

### 1. Construcción del grafo
El mapa se analiza una sola vez en un `Graph` (zonas + conexiones), con la lista de adyacencia precalculada — evita recorrer todas las conexiones cada vez que se necesita saber los vecinos de una zona.

### 2. BFS: valida si existe un camino
Antes de simular, un `BFS` simple confirma que existe una ruta entre `start` y `end`, ignorando las zonas `blocked`. Falla rápido si el mapa es imposible, en lugar de descubrirlo turno a turno.

### 3. Dijkstra: camino más barato en turnos
`BFS` solo cuenta saltos; `Dijkstra` (con `heapq`) encuentra el camino de menor costo en turnos, ya que `restricted` cuesta 2 turnos y `normal`/`priority` cuestan 1. Las zonas `blocked` nunca se expanden.

### 4. Balanceo de carga
`Dijkstra` resuelve el problema para un único drone. Con varios drones, el camino de cada uno se calcula una sola vez (no se recalcula en cada turno) y, si existen caminos alternativos del mismo costo, los drones se distribuyen entre ellos — evita que todos compitan por la misma ruta.

### 5. Turno en dos fases
Cada turno resuelve primero todas las salidas y después todas las llegadas — esto es lo que permite que un drone entre a una zona en el mismo turno en que otro está saliendo de ella.

### 6. Tránsito de 2 turnos (`restricted`)
Modelado como un pequeño estado en el drone (`STOPPED` -> `IN_TRANSIT`), con el lugar en el destino reservado ya desde la salida — el drone nunca se queda esperando a mitad de camino.

### 7. Conflictos y deadlock
Quien pierde la disputa por un lugar simplemente espera y lo vuelve a intentar en el turno siguiente (el desempate se hace por el orden de la lista, determinístico). Un límite máximo de turnos evita un bucle infinito.

## Visualization

### Renderizado del mapa
Las zonas se convierten en ilustraciones temáticas según su tipo (`start`/`end`/`normal`/`priority`/`restricted`/`blocked`), con las coordenadas `x`/`y` del mapa convertidas a píxeles de forma dinámica (escala calculada a partir de los límites del mapa cargado, no fija). Las conexiones se dibujan como líneas entre los centros de las zonas.

### Drones por turno
Cada drone aparece sobre la zona donde está; en tránsito (`restricted`, 2 turnos), aparece en el punto medio entre origen y destino — deja visualmente claro que está "en camino", no detenido en una zona.

### Navegación
`K_RIGHT`/`K_LEFT` avanzan y retroceden un turno manualmente, y `K_RETURN` corre toda la simulación automáticamente, turno a turno, con un pequeño retraso entre ellos.

### Información en pantalla
El turno actual y la lista de movimientos de ese turno son visibles en pantalla, además de imprimirse en la consola — la misma información en dos formatos (visual y texto), reforzando lo que está pasando.

---

# Instructions

## Requisitos previos

- Python 3.10+ (el proyecto usa 3.12)
- Módulo `uv` instalado

## Instalación

```bash
make install
```

## Ejecutar el proyecto

```bash
make run
```

> Corre la simulación con el mapa por defecto (`maps/config_map.txt`) y abre la interfaz gráfica.

Para correr un mapa específico:

```bash
uv run python -m src.fly_in maps/easy/01_linear_path.txt
```

## Dentro de la interfaz:

- `→` / `←` avanza/retrocede un turno;
- `Enter` corre todo automáticamente.

## Debug

```bash
make debug
```

Abre el `pdb` en el punto de entrada del programa.

## Correr los mapas de referencia

```bash
make bonus
```

> Corre los 10 mapas oficiales (easy/medium/hard/challenger) y muestra los turnos obtenidos contra la meta de cada uno.

## Lint

```bash
make lint
```

## Limpiar cachés

```bash
make clean
```

---

# Resources

## Referencias de documentación usada, artículos, tutoriales, etc.

[Guía de inicio rápido de pytest](https://docs.pytest.org/en/stable/getting-started.html)
[Documentación oficial de uv](https://docs.astral.sh/uv/)
[Documentación de dataclasses](https://docs.python.org/es/dev/library/dataclasses.html)
[Grafos y algoritmos](https://medium.com/programadores-ajudando-programadores/os-grafos-e-os-algoritmos-697c1fd4a416)
[Implementando el algoritmo de Dijkstra en Python: un tutorial paso a paso](https://www.datacamp.com/es/tutorial/dijkstra-algorithm-in-python)
[Breadth-First Search en Python: una guía con ejemplos](https://www.datacamp.com/es/tutorial/breadth-first-search-in-python)
[Python Graphs](https://www.w3schools.com/python/python_dsa_graphs.asp)
[Documentación de heapq (cola de prioridad en Python)](https://docs.python.org/3/library/heapq.html)
[Documentación de collections.deque (cola eficiente, para BFS)](https://docs.python.org/3/library/collections.html#collections.deque)
[Documentación de re - W3Schools](https://www.w3schools.com/python/ref_module_re.asp)
[Regular expression HOWTO](https://docs.python.org/es/3.14/howto/regex.html)
[Documentación de re](https://docs.python.org/es/3.14/library/re.html)
[Documentación oficial de pygame v2.6.0](https://www.pygame.org/docs/)

## Uso de IA

El agente de IA Sonnet, de Claude, fue utilizado para ayudar en la estructuración del proyecto (carpetas y subcarpetas, así como sus nombres correctos).
Ayuda indicando qué pruebas unitarias podrían hacerse.
Traducción de todas las variables, clases y módulos al inglés; y de los docstrings, comentarios y salidas (prints y errores) al español. Así como la traducción de este README.
El agente de IA nano-banana, de Gemini, fue utilizado para generar más imágenes, tomando como referencia imágenes ya creadas.
