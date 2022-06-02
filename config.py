import os
import typing

import sqlalchemy

metadata = sqlalchemy.MetaData()


def get_app_config() -> dict[typing.Literal['TITLE', 'VERSION', 'DESCRIPTION'], str]:
    TITLE = os.environ.get('TITLE', 'TITLE')
    VERSION = os.environ.get('VERSION', '0.1.0')
    DESCRIPTION = os.environ.get('DESCRIPTION', 'DESCRIPTION')
    return {'TITLE': TITLE, 'VERSION': VERSION, 'DESCRIPTION': DESCRIPTION}


def get_postgres_uri() -> str:
    HOST = os.environ.get('DB_HOST', 'localhost')
    PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'DB_NAME')
    DB_USER = os.environ.get('DB_USER', 'DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'DB_PASSWORD')
    return f'postgresql://{DB_USER}:{DB_PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
