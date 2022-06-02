from fastapi import FastAPI

import config
from src.auth.adapters import orm as auth_orm

auth_orm.start_mappers()

app = FastAPI(
    title=config.get_app_config()['TITLE'],
    version=config.get_app_config()['VERSION'],
    description=config.get_app_config()['DESCRIPTION'],
)
