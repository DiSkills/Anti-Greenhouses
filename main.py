from fastapi import FastAPI

import config

app = FastAPI(
    title=config.get_app_config()['TITLE'],
    version=config.get_app_config()['VERSION'],
    description=config.get_app_config()['DESCRIPTION'],
)
