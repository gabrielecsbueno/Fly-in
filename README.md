<p align="center">
    <img src=./assets/banner.png>
</p>

---

O projeto **Fly-in é um sistema que roteia, de forma eficiente, uma frota de drones a partir de uma base central (início) até um local de destino (fim)**, navegando por essa rede dinâmica sob um conjunto de restrições rígidas e objetivos de otimização.

O mapa é recebido a partir de um arquivo `.txt` passado por argumento, ou o `maps/config_map.txt` padrão caso nenhum seja informado.

O grafo é representado como uma rede de zonas conectadas, onde as conexões definem os possíveis caminhos de movimento entre as zonas.

> Objetivo principal do projeto: criacao de drones autônomos

## Estrutura do Projeto

```bash
fly_in/
├── maps/                       # mapas de exemplo (easy/medium/hard/challenger) + mapa de teste
├── src/
│   └── fly_in/                  # pacote Python principal
│       ├── __init__.py         # inicializador do pacote
│       ├── __main__.py         # ponto de entrada (make run / make debug)
│       ├── app.py              # orquestrador do programa
│       ├── domain/             # modelo de domínio: classes puras
│       │   ├── __init__.py
│       │   ├── zone_type.py    # Enum ZoneType, custo em turnos por tipo de zona
│       │   ├── zone.py         # classe Zone: dados estáticos de uma zona do mapa
│       │   ├── connection.py   # classe Connection: liga duas Zones, guarda max_link_capacity
│       │   ├── drone.py        # classe Drone: posição, status e histórico do drone
│       │   └── graph.py        # classe Graph/Network: zonas + conexões, lista de adjacência
│       ├── parsing/            # parser do arquivo de mapa
│       │   ├── __init__.py
│       │   ├── map_parser.py   # MapParser: lê o arquivo linha a linha e monta o Graph
│       │   ├── metadata.py     # parser dos metadados [chave=valor chave2=valor2]
│       │   └── errors.py       # MapParseError e outras exceções customizadas do parser
│       ├── pathfinding/         # algoritmos para buscar o caminho
│       │   ├── __init__.py
│       │   ├── dijkstra.py     # Dijkstra: menor custo total
│       │   └── bfs.py          # BFS: menor número de saltos
│       ├── simulation/         # motor de simulação
│       │   ├── __init__.py
│       │   ├── engine.py       # SimulationEngine: loop principal de turnos
│       │   ├── occupancy.py    # ZoneOccupancy e ConnectionOccupancy: estado dinâmico de ocupação
│       │   └── output.py       # MapsResult: guarda os dados de simulacao pronto para rederizacao
│       ├── ui/                 # visualização da simulação
│       │   ├── assets/         # imagens usadas na visualizacao do pygame
│       │   ├── __init__.py
│       │   └── interface.py    # saída do pygame
│       └── bonus/
│           ├── __init__.py
│           └── benchmark.py
├── README.md
├── Makefile                     # install/run/debug/clean/lint/bonus
├── pyproject.toml              # dependências (uv) e configuração de flake8/mypy/pytest
├── uv.lock                     # versões exatas travadas pelo uv (reprodutibilidade)
└── .gitignore                  # artefatos Python ignorados pelo Git
```

## Construção do projeto


### 1. Construção do grafo

O mapa é parseado uma vez em um `Graph` (zonas + conexões), com a lista de adjacência pré-calculada — evita varrer todas as conexões toda vez que se precisa saber os vizinhos de uma zona.

### 2. Algoritmo BFS: valida se existe caminho
Antes de simular, um `BFS` simples confirma que existe rota entre `start` e `end`, ignorando zonas `blocked`. Falha rápido se o mapa for impossível, em vez de descobrir isso turno a turno.

### 3. Algoritmo Dijkstra: encontra o caminho mais barato em turnos
`BFS` só conta saltos, já o `Dijkstra` (com `heapq`) encontra o caminho de menor custo em turnos, já que `restricted` custa 2 turnos e `normal`/`priority` custam 1. Zonas `blocked` nunca são expandidas.

### 4. Balanceamento de carga
`Dijkstra` resolve para um único drone. Com vários drones, o caminho de cada um é calculado uma vez só (não recalculado a cada turno) e, se existirem caminhos alternativos de mesmo custo, os drones são distribuídos entre eles — evita todo mundo competir pela mesma rota.

### 5. Turno em duas fases
Cada turno resolve primeiro todas as saídas, depois todas as chegadas — isso é o que permite um drone entrar numa zona no mesmo turno em que outro está saindo dela.

### 6. Trânsito de 2 turnos (`restricted`)
Modelado como um pequeno estado no drone (`STOPPED` -> `IN_TRANSIT`), com a vaga no destino reservada já na saída — o drone nunca fica preso esperando no meio do caminho.

### 7. Conflitos e deadlock
Quem perde a disputa por uma vaga só espera e tenta de novo no turno seguinte (desempate é feito pela ordem da lista, determinístico). Um limite máximo de turnos evita loop infinito.


## Visualization

### Renderização do mapa
Zonas viram ilustrações temáticas por tipo (`start`/`end`/`normal`/`priority`/`restricted`/`blocked`), com as coordenadas `x`/`y` do mapa convertidas em pixels dinamicamente (escala calculada a partir dos limites do mapa carregado, não fixa). Conexões são desenhadas como linhas entre os centros das zonas.

### Drones por turno
Cada drone aparece sobre a zona onde está; em trânsito (`restricted`, 2 turnos), aparece no ponto médio entre origem e destino — deixa visualmente claro que ele está "no caminho", não parado numa zona.

### Navegação
`K_RIGHT`/`K_LEFT` avançam e voltam turno a turno manualmente e `K_RETURN` roda a simulação inteira automaticamente, turno a turno, com um pequeno delay entre eles.

### Informação na tela
O turno atual e a lista de movimentos daquele turno ficam visíveis na tela, além de serem impressos no console — a mesma informação em dois formatos (visual e texto), reforçando o que está acontecendo.


## I/O

[Exemplo de entrada e saída esperada demonstrando a funcionalidade do programa]

---

# Instructions

## Pré-requisitos

- Python 3.10+ (o projeto usa 3.12)
- Modulo `uv` instalado

## Instalação

```bash
make install
```

## Executar o projeto

```bash
make run
```

> Roda a simulação com o mapa padrão (maps/config_map.txt) e abre a interface gráfica.

Pra rodar um mapa específico:

```bash
uv run python -m src.fly_in maps/easy/01_linear_path.txt
```

## Dentro da interface:

- `→` / `←` avança/volta um turno;
- `Enter` roda tudo automaticamente.

## Debug

```bash
make debug
```

Abre o `pdb` no ponto de entrada do programa.

## Rodar os mapas de referência

```bash
make bonus
```

> Roda os 10 mapas oficiais (easy/medium/hard/challenger) e mostra os turnos obtidos contra a meta de cada um.

## Lint

```bash
make lint
```

## Limpar caches

```bash
make clean
```

---

# Resources

## Referências de documentacoes usadas, artigos, tutoriais, etc.

[Guia de início rápido do pytest](https://docs.pytest.org/en/stable/getting-started.html)

[Documentação oficial do uv](https://docs.astral.sh/uv/)

[Documentacao do dataclasses](https://docs.python.org/pt-br/dev/library/dataclasses.html)

[Grafos e algoritmos](https://medium.com/programadores-ajudando-programadores/os-grafos-e-os-algoritmos-697c1fd4a416)

[Implementando o algoritmo Dijkstra em Python: Um tutorial passo a passo](https://www.datacamp.com/pt/tutorial/dijkstra-algorithm-in-python)

[Breadth-First Search em Python: Um guia com exemplos](https://www.datacamp.com/pt/tutorial/breadth-first-search-in-python)

[Python Graphs](https://www.w3schools.com/python/python_dsa_graphs.asp)

[Documentação do heapq (fila de prioridade em Python)](https://docs.python.org/3/library/heapq.html)

[Documentação do collections.deque (fila eficiente, para BFS)](https://docs.python.org/3/library/collections.html#collections.deque)

[Documentacao re - W3Schools](https://www.w3schools.com/python/ref_module_re.asp)

[Regular expression HOWTO](https://docs.python.org/pt-br/3.14/howto/regex.html)

[Documentacao re](https://docs.python.org/pt-br/3.14/library/re.html)

[Documentação oficial do pygame v2.6.0](https://www.pygame.org/docs/)

## Uso da IA

O agente de IA sonnete, do claude, foi utilizado para auxiliar na estruturacao do projeto (como pastas e subpastas, assim como suas nomenclaturas corretas).
Auxilio indicando quais testes unitarios que poderiam ser feitos.
Traducao de todas as variaveis, classes e modulos para ingles; e as docstrings, comentarios e saidas (prints e erros) para espanhol. Assim como a traducao deste README.
O agente de IA nano-banana, do gemini, foi utilizada para gerar mais imagens, tomando como referencias de imagens criadas.