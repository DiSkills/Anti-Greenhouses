import time

import pytest
import requests
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, clear_mappers, Session

import config
from config import metadata
from src.auth.adapters.orm import start_mappers as auth_start_mappers


@pytest.fixture()
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)

    auth_start_mappers()
    yield sessionmaker(bind=engine)
    clear_mappers()

    metadata.drop_all(engine)


@pytest.fixture()
def sqlite_session(in_memory_db) -> Session:
    return in_memory_db()


def wait_for_postgres_to_come_up(*, engine: Engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail('Postgres never came up')


def wait_for_app_to_come_up():
    deadline = time.time() + 10
    url = config.get_host_url()
    while time.time() < deadline:
        try:
            return requests.get(url=url)
        except requests.ConnectionError:
            time.sleep(0.5)
    pytest.fail('API never came up')


@pytest.fixture()
def postgres_db():
    engine = create_engine(config.get_postgres_uri())
    wait_for_postgres_to_come_up(engine=engine)

    with engine.begin() as engine:
        metadata.create_all(engine)

        auth_start_mappers()
        yield sessionmaker(bind=engine)
        clear_mappers()

        metadata.drop_all(engine)


@pytest.fixture()
def postgres_session(postgres_db) -> Session:
    return postgres_db()


@pytest.fixture()
def restart_api():
    (Path(__file__).parent / '../main.py').touch()
    time.sleep(0.5)
    wait_for_app_to_come_up()
