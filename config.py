import logging
import os
from dataclasses import dataclass

import sqlalchemy

metadata = sqlalchemy.MetaData()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('API')


@dataclass
class AppConfig:
    title: str
    version: str
    description: str


def get_app_settings() -> AppConfig:
    title = os.environ.get('TITLE', 'Anti-Greenhouses')
    version = os.environ.get('VERSION', '0.1.0')
    description = os.environ.get('DESCRIPTION', 'Anti-Greenhouses by _Anti_')

    logger.debug(f'[DEBUG] Title: {title}, Version: {version}, Description: {description}')

    return AppConfig(title=title, version=version, description=description)


def get_db_uri() -> str:
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', '5432')
    db_name = os.environ.get('DB_NAME', 'DB_NAME')
    db_user = os.environ.get('DB_USER', 'DB_USER')
    db_password = os.environ.get('DB_PASSWORD', 'DB_PASSWORD')

    uri = f'postgresql://{db_user}:{db_password}@{host}:{port}/{db_name}'

    logger.debug(f'[DEBUG] Database URI: {uri}')

    return uri


def start_mappers() -> None:
    from src.auth.adapters.orm import start_mappers as auth_start_mappers
    auth_start_mappers()
