from fastapi import APIRouter, status

from src.auth.entrypoints.routers.login import login_router
from src.auth.entrypoints.routers.registration import registration_router
from src.auth.entrypoints.routers.registration_request import registration_request_router
from src.base.entrypoints.schemas import HTTPError

auth = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'model': HTTPError,
        },
    },
)

auth.include_router(registration_request_router)
auth.include_router(registration_router)
auth.include_router(login_router)
