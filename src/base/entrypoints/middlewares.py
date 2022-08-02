from typing import Callable

from fastapi import Request, Response


async def ip_middleware(request: Request, call_next: Callable) -> Response:
    request.state.ip = request.headers.get('x-forwarded-for')
    response = await call_next(request)
    return response


async def bad_logins_middleware(request: Request, call_next: Callable) -> Response:
    # TODO
    response = await call_next(request)
    return response
