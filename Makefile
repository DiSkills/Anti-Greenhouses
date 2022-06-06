mypy:
	poetry run mypy *.py src/ tests/ --check-untyped-defs

pytest:
	poetry run pytest --tb=short

install:
	pip install --upgrade pip
	pip install poetry
	poetry install
