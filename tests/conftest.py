import typing

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers, Session

from config import metadata, start_mappers


@pytest.fixture()
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')

    start_mappers()
    metadata.create_all(engine)

    yield sessionmaker(bind=engine)
    clear_mappers()

    metadata.drop_all(engine)


@pytest.fixture()
def sqlite_session(in_memory_db) -> typing.Generator[Session, None, None]:
    with in_memory_db() as session:
        yield session
