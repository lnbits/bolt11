all: black ruff mypy pyright test

format: black ruff-fix

black:
	poetry run black --preview .

ruff:
	poetry run ruff check . --fix

checkruff:
	poetry run ruff check .

mypy:
	poetry run mypy .

pyright:
	poetry run pyright

test:
	poetry run pytest tests
