from fastapi import APIRouter, Request, HTTPException, status

from src.auth import exceptions
from src.auth.entrypoints.schemas.users import Registration
from src.auth.services import registration as services
from src.base.aliases import Msg
from src.base.entrypoints.schemas import Message

registration_router = APIRouter()


@registration_router.post(
    r'/registration',
    name='registration',
    description='Registration',
    status_code=status.HTTP_201_CREATED,
    response_description='Message',
    response_model=Message,
)
async def registration(request: Request, schema: Registration) -> Msg:
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
