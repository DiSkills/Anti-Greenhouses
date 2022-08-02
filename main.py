from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

import config
from src.auth.entrypoints.routers.users import users
from src.auth.entrypoints.routers.verifications import verifications
from src.base import middlewares

app_config = config.get_app_settings()
mongo_config = config.get_mongo_settings()

app = FastAPI(
    title=app_config.title,
    version=app_config.version,
    description=app_config.description,
)


@app.on_event('startup')
async def startup() -> None:
    config.start_mappers()
    config.logger.debug('[DEBUG] Mappers have been mapped')

    config.metadata.create_all(bind=config.engine)
    config.logger.debug('[DEBUG] All metadata has been created')

    db = config.mongo_client[mongo_config.name]
    verifications_table = db.create_collection(config.MongoTables.verifications.name)
    verifications_table.create_index(config.MongoTables.verifications.uuid, unique=True)
    verifications_table.create_index(config.MongoTables.verifications.email, unique=True)

    bad_logins_table = db.create_collection(config.MongoTables.bad_logins.name)
    bad_logins_table.create_index(config.MongoTables.bad_logins.uuid, unique=True)
    config.logger.debug('[DEBUG] Mongo tables has been created')


@app.on_event('shutdown')
async def shutdown() -> None:
    clear_mappers()
    config.logger.debug('[DEBUG] Mappers have been cleared')

    config.metadata.drop_all(bind=config.engine)
    config.logger.debug('[DEBUG] All metadata has been dropped')

    config.mongo_client.drop_database(mongo_config.name)
    config.logger.debug('[DEBUG] Mongo tables has been dropped')


app.middleware('http')(middlewares.ip_middleware)

app.include_router(verifications, prefix=config.get_api_url())
app.include_router(users, prefix=config.get_api_url())
