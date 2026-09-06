*This project has been created as part of the 42 curriculum by [gabde-so](https://profile-v3.intra.42.fr/users/gabde-so)*

# **FLY_IN**

---

# Description

> Main goal of the project: efficient routing of autonomous drones

**Fly-in is a system that efficiently routes a fleet of drones from a central base (start) to a target location (end)**, navigating that dynamic network under a set of strict constraints and optimization goals.

The map is read from a `.txt` file passed as an argument, or from the default `maps/config_map.txt` if none is given.

The graph is represented as a network of connected zones, where connections define the possible movement paths between zones.

## Project Structure

```bash
fly_in/
├── maps/                       # example maps (easy/medium/hard/challenger) + test map
├── src/
│   └── fly_in/                 # main Python package
│       ├── __init__.py         # package initializer
│       ├── __main__.py         # entry point (make run / make debug)
│       ├── app.py              # program orchestrator
│       ├── domain/             # domain model: plain classes
│       │   ├── __init__.py
│       │   ├── zone_type.py    # ZoneType Enum, turn cost per zone type
│       │   ├── zone.py         # Zone class: static data for a map zone
│       │   ├── connection.py   # Connection class: links two Zones, holds max_link_capacity
│       │   ├── drone.py        # Drone class: position, status and history of the drone
│       │   └── graph.py        # Graph/Network class: zones + connections, adjacency list
│       ├── parsing/            # map file parser
│       │   ├── __init__.py
│       │   ├── map_parser.py   # MapParser: reads the file line by line and builds the Graph
│       │   ├── metadata.py     # metadata parser [key=value key2=value2]
│       │   └── errors.py       # MapParseError and other custom parser exceptions
│       ├── pathfinding/        # path-search algorithms
│       │   ├── __init__.py
│       │   ├── dijkstra.py     # Dijkstra: lowest total cost
│       │   └── bfs.py          # BFS: fewest number of hops
│       ├── simulation/         # simulation engine
│       │   ├── __init__.py
│       │   ├── engine.py       # SimulationEngine: main turn loop
│       │   ├── occupancy.py    # ZoneOccupancy and ConnectionOccupancy: dynamic occupancy state
│       │   └── output.py       # MapsResult: simulation data ready to be rendered
│       ├── ui/                 # simulation visualization
│       │   ├── assets/         # images used in the pygame visualization
│       │   ├── __init__.py
│       │   └── interface.py    # pygame output
│       └── bonus/
│           ├── __init__.py
│           └── benchmark.py
├── README.md
├── Makefile                    # install/run/debug/clean/lint/bonus
├── pyproject.toml              # dependencies (uv) and flake8/mypy/pytest configuration
├── uv.lock                     # exact versions locked by uv (reproducibility)
└── .gitignore                  # Python artifacts ignored by Git
```

## Algorithm Choices

### 1. Graph construction
The map is parsed once into a `Graph` (zones + connections), with the adjacency list precomputed — this avoids scanning every connection each time a zone's neighbors are needed.

### 2. BFS: checks that a path exists
Before simulating, a simple `BFS` confirms that a route exists between `start` and `end`, ignoring `blocked` zones. It fails fast if the map is impossible, instead of discovering it turn by turn.

### 3. Dijkstra: cheapest path in turns
`BFS` only counts hops; `Dijkstra` (with `heapq`) finds the path with the lowest cost in turns, since `restricted` costs 2 turns and `normal`/`priority` cost 1. `blocked` zones are never expanded.

### 4. Load balancing
`Dijkstra` solves the problem for a single drone. With several drones, each one's path is computed only once (never recalculated every turn), and if alternative paths of the same cost exist, drones are distributed across them — avoiding everyone competing for the same route.

### 5. Two-phase turn
Each turn resolves all departures first, then all arrivals — this is what lets a drone enter a zone in the same turn another one is leaving it.

### 6. 2-turn transit (`restricted`)
Modeled as a small state on the drone (`STOPPED` -> `IN_TRANSIT`), with the destination spot reserved right at departure — the drone never gets stuck waiting halfway.

### 7. Conflicts and deadlock
Whoever loses a spot simply waits and retries the following turn (ties are broken by list order, deterministically). A maximum turn limit prevents an infinite loop.

## Visualization

### Map rendering
Zones become themed illustrations per type (`start`/`end`/`normal`/`priority`/`restricted`/`blocked`), with the map's `x`/`y` coordinates converted to pixels dynamically (scale computed from the loaded map's bounds, not fixed). Connections are drawn as lines between zone centers.

### Drones per turn
Each drone appears over the zone it's in; while in transit (`restricted`, 2 turns), it appears at the midpoint between origin and destination — making it visually clear it's "on the way", not standing in a zone.

### Navigation
`K_RIGHT`/`K_LEFT` step one turn forward/backward manually, and `K_RETURN` runs the whole simulation automatically, turn by turn, with a short delay between them.

### On-screen information
The current turn and that turn's list of movements are visible on screen, as well as printed to the console — the same information in two formats (visual and text), reinforcing what's happening.

---

# Instructions

## Requirements

- Python 3.10+ (the project uses 3.12)
- `uv` installed

## Installation

```bash
make install
```

## Running the project

```bash
make run
```

> Runs the simulation with the default map (`maps/config_map.txt`) and opens the graphical interface.

To run a specific map:

```bash
uv run python -m src.fly_in maps/easy/01_linear_path.txt
```

## Inside the interface:

- `→` / `←` step one turn forward/backward;
- `Enter` runs everything automatically.

## Debug

```bash
make debug
```

Opens `pdb` at the program's entry point.

## Running the reference maps

```bash
make bonus
```

> Runs the 10 official maps (easy/medium/hard/challenger) and shows the turns obtained against each one's target.

## Lint

```bash
make lint
```

## Cleaning caches

```bash
make clean
```

---

# Resources

## References: documentation used, articles, tutorials, etc.

[pytest quickstart guide](https://docs.pytest.org/en/stable/getting-started.html)
[Official uv documentation](https://docs.astral.sh/uv/)
[dataclasses documentation](https://docs.python.org/3/library/dataclasses.html)
[Graphs and algorithms](https://medium.com/programadores-ajudando-programadores/os-grafos-e-os-algoritmos-697c1fd4a416)
[Implementing Dijkstra's Algorithm in Python: A Step-by-Step Tutorial](https://www.datacamp.com/tutorial/dijkstra-algorithm-in-python)
[Breadth-First Search in Python: A Guide with Examples](https://www.datacamp.com/tutorial/breadth-first-search-in-python)
[Python Graphs](https://www.w3schools.com/python/python_dsa_graphs.asp)
[heapq documentation (priority queue in Python)](https://docs.python.org/3/library/heapq.html)
[collections.deque documentation (efficient queue, for BFS)](https://docs.python.org/3/library/collections.html#collections.deque)
[re documentation - W3Schools](https://www.w3schools.com/python/ref_module_re.asp)
[Regular expression HOWTO](https://docs.python.org/3/howto/regex.html)
[re documentation](https://docs.python.org/3/library/re.html)
[Official pygame v2.6.0 documentation](https://www.pygame.org/docs/)

## AI usage

Claude's Sonnet AI agent was used to help structure the project (folders and subfolders, and their correct naming).
Help pointing out which unit tests could be written.
Translation of all variables, classes and modules to English; and of docstrings, comments and outputs (prints and errors) to Spanish. As well as the translation of this README.
Gemini's nano-banana AI agent was used to generate additional images, using previously created images as reference.
