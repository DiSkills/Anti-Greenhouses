from fastapi import APIRouter

from src.auth.entrypoints.routers.registration import registration_router
from src.auth.entrypoints.routers.registration_request import registration_request_router

auth = APIRouter(prefix='/auth', tags=['auth'])

auth.include_router(registration_request_router)
auth.include_router(registration_router)
