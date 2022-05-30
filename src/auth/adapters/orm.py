import sqlalchemy
from sqlalchemy.orm import mapper

from src.auth.domain import model

metadata = sqlalchemy.MetaData()

verifications = sqlalchemy.Table(
    'verifications',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False),
    sqlalchemy.Column('uuid', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('email', sqlalchemy.String, unique=True, nullable=False),
)


def start_mappers():
    mapper(model.Verification, verifications)
