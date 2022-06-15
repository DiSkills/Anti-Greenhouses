import typing

from fastapi import APIRouter, status, HTTPException

from config import get_session
from src.auth.adapters.repositories.verification import VerificationRepository
from src.auth.entrypoints.schemas import verifications as schemas
from src.auth.services import exceptions, services
from src.base.schemas import Message

verifications = APIRouter(prefix='/auth', tags=['auth'])


# TODO add error when user with this email exists
@verifications.post(
    '/registration/request',
    name='registration_request',
    description='Send verification mail for registration',
    status_code=status.HTTP_201_CREATED,
    response_description='Message',
    response_model=Message,
)
async def registration_request(schema: schemas.RegistrationRequest) -> dict[typing.Literal['msg'], str]:
    with get_session() as session:
        repo = VerificationRepository(session=session)

        try:
            services.registration_request(email=schema.email, repository=repo, session=session)
        except exceptions.VerificationExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Verification with this email already exists, we sent you another email with a code.',
            )

        return {
            'msg': 'Please check your email, copy the sent code, you will need it to continue registration.',
        }
