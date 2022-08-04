from fastapi import APIRouter, Request, HTTPException, status, Form

from src.auth import exceptions
from src.auth.entrypoints.schemas.users import Login
from src.auth.services import login as services
from src.base.aliases import Tokens

login_router = APIRouter()


@login_router.post(
    r'/login',
    name='login',
    description='Login',
    status_code=status.HTTP_200_OK,
    response_description='Tokens',
    response_model=Login,
)
async def login(request: Request, username: str = Form(...), password: str = Form(...)) -> Tokens:
    try:
        tokens = services.login(username=username, password=password, ip_address=request.state.ip)
    except exceptions.InvalidUsernameOrPassword:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid username or password.')

    return {'access_token': tokens.access, 'refresh_token': tokens.refresh, 'token_type': 'bearer'}
