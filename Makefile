all: black ruff mypy pyright test

format: black ruff-fix

black:
	uv run black --preview .

ruff:
	uv run ruff check .

ruff-fix:
	uv run ruff check . --fix

mypy:
	uv run mypy .

pyright:
	uv run pyright

test:
	uv run pytest
