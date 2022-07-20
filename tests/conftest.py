from dataclasses import dataclass
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from pymongo.collection import Collection
from pymongo.database import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers, Session

import main
from config import metadata, start_mappers, get_session, mongo_client, mongo_config, MongoTables


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


@pytest.fixture()
def mongo_session() -> Generator[Database, None, None]:
    db = mongo_client[mongo_config.name]

    verifications_table = db.create_collection(MongoTables.verifications.name)
    verifications_table.create_index(MongoTables.verifications.uuid, unique=True)
    verifications_table.create_index(MongoTables.verifications.email, unique=True)

    yield db

    mongo_client.drop_database(mongo_config.name)


@pytest.fixture()
def mongo_verifications(mongo_session) -> Generator[Collection, None, None]:
    yield mongo_session[MongoTables.verifications.name]


@dataclass
class E2E:
    client: TestClient
    session: Session
    mongo: Database


@pytest.fixture()
def e2e() -> Generator[E2E, None, None]:
    with TestClient(app=main.app) as client:
        with get_session() as session:
            yield E2E(client=client, session=session, mongo=mongo_client[mongo_config.name])


class Password:
    password = 'password'
    strong = 'Admin2248!'


class Username:
    user = 'user'
    test = 'test'
    bot = 'bot'


class Email:
    user = 'user@example.com'
    user2 = 'user2@example.com'
    python = 'python@example.com'
    bot = 'bot@example.com'
    hello = 'hello@example.com'


class TestData:
    email = Email()
    username = Username()
    password = Password()
    ip_address = '0.0.0.0'
