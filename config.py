import os
import typing

import sqlalchemy

metadata = sqlalchemy.MetaData()


def get_app_config() -> dict[typing.Literal['TITLE', 'VERSION', 'DESCRIPTION'], str]:
    TITLE = os.environ.get('TITLE', 'TITLE')
    VERSION = os.environ.get('VERSION', '0.1.0')
    DESCRIPTION = os.environ.get('DESCRIPTION', 'DESCRIPTION')
    return {'TITLE': TITLE, 'VERSION': VERSION, 'DESCRIPTION': DESCRIPTION}
