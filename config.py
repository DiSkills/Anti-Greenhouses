import os
from dataclasses import dataclass

import sqlalchemy

metadata = sqlalchemy.MetaData()


@dataclass
class AppConfig:
    title: str
    version: str
    description: str


def get_app_settings() -> AppConfig:
    title = os.environ.get('TITLE', 'Anti-Greenhouses')
    version = os.environ.get('VERSION', '0.1.0')
    description = os.environ.get('DESCRIPTION', 'Anti-Greenhouses by _Anti_')
    return AppConfig(title=title, version=version, description=description)


def get_db_uri() -> str:
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', '5432')
    db_name = os.environ.get('DB_NAME', 'DB_NAME')
    db_user = os.environ.get('DB_USER', 'DB_USER')
    db_password = os.environ.get('DB_PASSWORD', 'DB_PASSWORD')
    return f'postgresql://{db_user}:{db_password}@{host}:{port}/{db_name}'


def get_host_url() -> str:
    url = os.environ.get('HOST', 'http://localhost:8000')
    return url
