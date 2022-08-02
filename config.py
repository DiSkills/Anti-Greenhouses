import logging
import os
from dataclasses import dataclass
from enum import Enum

import sqlalchemy
from passlib.context import CryptContext
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing_extensions import TypeAlias

metadata = sqlalchemy.MetaData()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('API')

Seconds: TypeAlias = int


class Verifications:
    name = 'verifications'

    uuid = 'uuid'
    email = 'email'


class BadLogins:
    name = 'bad_logins'

    uuid = 'uuid'


class MongoTables:
    verifications = Verifications()
    bad_logins = BadLogins()


@dataclass
class MongoConfig:
    host: str
    port: int

    name: str
    user: str
    password: str


def get_db_uri() -> str:
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', '5432')
    db_name = os.environ.get('DB_NAME', 'DB_NAME')
    db_user = os.environ.get('DB_USER', 'DB_USER')
    db_password = os.environ.get('DB_PASSWORD', 'DB_PASSWORD')

    uri = f'postgresql://{db_user}:{db_password}@{host}:{port}/{db_name}'

    logger.debug(f'[DEBUG] Database URI: {uri}')

    return uri


def get_mongo_settings() -> MongoConfig:
    host = os.environ.get('MONGO_HOST', 'localhost')
    port = int(os.environ.get('MONGO_PORT', '27017'))
    db_name = os.environ.get('MONGO_NAME', 'MONGO_NAME')
    db_user = os.environ.get('MONGO_USER', 'MONGO_USER')
    db_password = os.environ.get('MONGO_PASSWORD', 'MONGO_PASSWORD')

    logger.debug(f'[DEBUG] Mongo uri: {db_user}:{db_password}@{host}:{port}/{db_name}')

    return MongoConfig(host=host, port=port, name=db_name, user=db_user, password=db_password)


engine = create_engine(url=get_db_uri())
get_session = sessionmaker(bind=engine, expire_on_commit=False)  # TODO {maybe} expire_on_commit=True
mongo_config = get_mongo_settings()
mongo_client: MongoClient = MongoClient(
    host=mongo_config.host, port=mongo_config.port, username=mongo_config.user, password=mongo_config.password,
)


@dataclass
class AppConfig:
    title: str
    version: str
    description: str
    secret_key: str


@dataclass
class CeleryConfig:
    broker: str
    result: str

    bad_login_countdown: Seconds


@dataclass
class EmailConfig:
    sender_email: str
    sender_password: str
    host: str
    port: int


class JWTConfig:
    default: Seconds = 60 * 15
    access: Seconds = 60 * 15
    refresh: Seconds = 60 * 60 * 24 * 14

    access_subject: str = 'access'
    refresh_subject: str = 'refresh'

    algorithms: list[str] = ['HS256']


class UserActionType(Enum):
    registered = 'User registered'
    login = 'User authorized'


def get_app_settings() -> AppConfig:
    title = os.environ.get('TITLE', 'Anti-Greenhouses')
    version = os.environ.get('VERSION', '0.1.0')
    description = os.environ.get('DESCRIPTION', 'Anti-Greenhouses by _Anti_')

    logger.debug(f'[DEBUG] Title: {title}, Version: {version}, Description: {description}')

    secret_key = os.environ.get('SECRET_KEY', 'SECRET_KEY')
    logger.debug(f'[DEBUG] Secret key: {secret_key}')

    return AppConfig(title=title, version=version, description=description, secret_key=secret_key)


def get_api_url() -> str:
    return os.environ.get('API_URL', '/api/v1')


def get_celery_settings() -> CeleryConfig:
    host = os.environ.get('CELERY_HOST', 'localhost')
    port = os.environ.get('CELERY_PORT', '5672')
    celery_user = os.environ.get('CELERY_USER', 'CELERY_USER')
    celery_password = os.environ.get('CELERY_PASSWORD', 'CELERY_PASSWORD')

    bad_login_countdown = Seconds(os.environ.get('BAD_LOGIN_COUNTDOWN', 60 * 10))

    broker = f'amqp://{celery_user}:{celery_password}@{host}:{port}//'
    result = os.environ.get('CELERY_RESULT', 'rpc://')

    logger.debug(f'[DEBUG] Celery broker: {broker}, Celery result: {result}')

    return CeleryConfig(broker=broker, result=result, bad_login_countdown=bad_login_countdown)


def get_email_settings() -> EmailConfig:
    host = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    port = int(os.environ.get('EMAIL_PORT', 587))

    sender_email = os.environ.get('EMAIL_USER', 'EMAIL_USER')
    sender_password = os.environ.get('EMAIL_PASSWORD', 'EMAIL_PASSWORD')

    logger.debug(f'[DEBUG] Email: {sender_email}, Password: {sender_password}, Server: {host}:{port}')

    return EmailConfig(host=host, port=port, sender_email=sender_email, sender_password=sender_password)


def get_pwd_context() -> CryptContext:
    return CryptContext(schemes=['bcrypt'], deprecated='auto')


def start_mappers() -> None:
    from src.auth.adapters.orm import auth_start_mappers
    auth_start_mappers()
