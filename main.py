from fastapi import FastAPI

import config

app_config = config.get_app_settings()

app = FastAPI(
    title=app_config.title,
    version=app_config.version,
    description=app_config.description,
)
