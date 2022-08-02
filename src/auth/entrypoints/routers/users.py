from fastapi import APIRouter, status, Request, HTTPException

from src.auth.entrypoints.schemas import users as schemas
from src.auth.services import services, exceptions
from src.base.aliases import Msg
from src.base.entrypoints.schemas import Message

users = APIRouter(prefix='/auth', tags=['auth'])


@users.post(
    r'/registration',
    name='registration',
    description='Registration',
    status_code=status.HTTP_201_CREATED,
    response_description='Message',
    response_model=Message,
)
async def registration(request: Request, schema: schemas.Registration) -> Msg:
    try:
        services.registration(schema=schema, ip_address=request.state.ip)
    except exceptions.UserWithUsernameExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this username exists.')
    except exceptions.UserWithEmailExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this email exists.')
    except exceptions.VerificationNotFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Verification with this email address was not found.',
        )
    except exceptions.BadVerificationUUID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Verification with this uuid was not found. We sent you another email with a code.',
        )

    return {'msg': 'You have been successfully registered on our website!'}
