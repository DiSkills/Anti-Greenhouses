import typing

from fastapi import APIRouter, status, HTTPException

from src.auth.entrypoints.schemas import verifications as schemas
from src.auth.services import exceptions, services
from src.base.schemas import Message

verifications = APIRouter(prefix='/auth', tags=['auth'])


@verifications.post(
    r'/registration/request',
    name='registration_request',
    description='Send verification mail for registration',
    status_code=status.HTTP_201_CREATED,
    response_description='Message',
    response_model=Message,
)
async def registration_request(schema: schemas.RegistrationRequest) -> dict[typing.Literal['msg'], str]:

    try:
        services.registration_request(email=schema.email)
    except exceptions.UserWithEmailExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this email exists.')
    except exceptions.VerificationExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Verification with this email already exists, we sent you another email with a code.',
        )

    return {
        'msg': 'Please check your email, copy the sent code, you will need it to continue registration.',
    }
