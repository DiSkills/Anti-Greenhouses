from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

import config

app_config = config.get_app_settings()

engine = create_engine(url=config.get_db_uri())
get_session = sessionmaker(bind=engine, expire_on_commit=False)  # TODO {maybe} expire_on_commit=True

app = FastAPI(
    title=app_config.title,
    version=app_config.version,
    description=app_config.description,
)


@app.on_event('startup')
async def startup() -> None:
    config.start_mappers()
    config.logger.debug('[DEBUG] Mappers have been mapped')

    config.metadata.create_all(bind=engine)
    config.logger.debug('[DEBUG] All metadata has been created')


@app.on_event('shutdown')
async def shutdown() -> None:
    clear_mappers()
    config.logger.debug('[DEBUG] Mappers have been cleared')

    config.metadata.drop_all(bind=engine)
    config.logger.debug('[DEBUG] All metadata has been dropped')
