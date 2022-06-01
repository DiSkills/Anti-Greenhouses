mypy:
	mypy *.py src/ tests/ --check-untyped-defs

pytest:
	pytest --tb=short

install:
	pip install --upgrade pip
	pip install poetry
	poetry install

test: mypy pytest
