from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import mapper, relationship

import config
from config import metadata
from src.auth.domain import model

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False),
    Column('uuid', String, unique=True, nullable=False),
    Column('username', String, unique=True, nullable=False),
    Column('email', String, unique=True, nullable=False),
    Column('password', String, nullable=False),
    Column('otp_secret', String, nullable=False),
    Column('otp', Boolean, nullable=False),
    Column('is_superuser', Boolean, nullable=False),
    Column('avatar', String, nullable=True),
    Column('date_joined', DateTime, nullable=False),
)

actions = Table(
    'actions',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False),
    Column('uuid', String, unique=True, nullable=False),
    Column('type', Enum(config.UserActionType), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('ip_address', String, nullable=True),
)

user_actions = Table(
    'user_actions',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False),
    Column('action_id', ForeignKey('actions.id', ondelete='CASCADE'), nullable=False),
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
)


def auth_start_mappers() -> None:
    """
        Mapping a domain area to a database
        :return: None
        :rtype: None
    """

    actions_mapper = mapper(model.UserAction, actions)
    mapper(
        model.User,
        users,
        properties={'_actions': relationship(actions_mapper, secondary=user_actions, collection_class=set)},
    )
