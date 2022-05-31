import sqlalchemy
from sqlalchemy.orm import mapper

from config import metadata
from src.auth.domain import model

verifications = sqlalchemy.Table(
    'verifications',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False),
    sqlalchemy.Column('uuid', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('email', sqlalchemy.String, unique=True, nullable=False),
)


def start_mappers() -> None:
    mapper(model.Verification, verifications)
