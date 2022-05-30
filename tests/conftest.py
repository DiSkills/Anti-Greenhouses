import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers, Session

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
