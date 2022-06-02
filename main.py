from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

import config

app_config = config.get_app_settings()

engine = create_engine(url=config.get_db_uri())
get_session = sessionmaker(bind=engine, expire_on_commit=False)

app = FastAPI(
    title=app_config.title,
    version=app_config.version,
    description=app_config.description,
)


@app.on_event('startup')
async def startup() -> None:
    config.metadata.create_all(bind=engine)
    config.logger.debug('All metadata has been created')

    config.start_mappers()
    config.logger.debug('Mappers have been mapped')


@app.on_event('shutdown')
async def shutdown() -> None:
    clear_mappers()
    config.logger.debug('Mappers have been cleared')

    config.metadata.drop_all(bind=engine)
    config.logger.debug('All metadata has been dropped')
