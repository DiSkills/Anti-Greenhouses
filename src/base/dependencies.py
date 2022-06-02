from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import config


def get_db() -> Session:
    get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
    with get_session() as db:
        yield db
