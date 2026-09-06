# Instala as dependências do projeto usando uv
install:
	uv sync

# Executa o script principal do projeto
run:
	clear
	uv run python -m src.fly_in

# Executa o script principal em modo de depuração usando o depurador interno do Python
debug:
	uv run python -m pdb -m src.fly_in

# Remove arquivos temporários ou caches
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name ".DS_Store" -exec rm -rf {} +
	rm -rf .venv

# Executa os comandos flake8 e mypy
lint:
	uv run flake8 src
	uv run mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

bonus:
	uv run python -m src.fly_in.bonus.benchmark

# Define nome dos comandos a serem executados no make
.PHONY: install run debug clean lint bonus
