export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

mypy:
	poetry run mypy *.py src/ tests/ --check-untyped-defs

pytest:
	poetry run pytest --tb=short

install:
	pip install --upgrade pip
	pip install poetry
	poetry install

server:
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

production: down build up
