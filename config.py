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
