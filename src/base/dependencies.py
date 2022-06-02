from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config


def get_db():
    get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
    with get_session() as db:
        yield db
