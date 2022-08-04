from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

from src.base import exceptions
from src.base.services import services


async def ip_middleware(request: Request, call_next: Callable) -> Response:
    request.state.ip = request.headers.get('x-forwarded-for')
    return await call_next(request)


async def bad_logins_middleware(request: Request, call_next: Callable) -> Response:
    try:
        services.bad_logins(ip=request.state.ip)
        return await call_next(request)
    except exceptions.ManyBadLogins:
        return JSONResponse(
            {'detail': 'Many bad login attempts, your ip is temporarily blocked.'},
            status_code=status.HTTP_403_FORBIDDEN,
        )
