from dataclasses import dataclass
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers, Session

import main
from config import metadata, start_mappers, get_session


@pytest.fixture()
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')

    start_mappers()
    metadata.create_all(engine)

    yield sessionmaker(bind=engine)
    clear_mappers()

    metadata.drop_all(engine)


@pytest.fixture()
def sqlite_session(in_memory_db) -> Generator[Session, None, None]:
    with in_memory_db() as session:
        yield session


@dataclass
class E2E:
    client: TestClient
    session: Session


@pytest.fixture()
def e2e() -> Generator[E2E, None, None]:
    with TestClient(app=main.app) as client:
        with get_session() as session:
            yield E2E(client=client, session=session)
