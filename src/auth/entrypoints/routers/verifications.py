import typing
import uuid

from fastapi import APIRouter, status, HTTPException

from config import get_session
from src.auth.adapters.repositories.verification import VerificationRepository
from src.auth.domain import model
from src.auth.entrypoints.schemas import verifications as schemas
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

        if repo.get(email=schema.email) is not None:
            # TODO send email
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Verification with this email already exists, we sent you another email with a code.',
            )

        # TODO send email
        repo.add(verification=model.Verification(email=schema.email, uuid=f'{uuid.uuid4()}'))
        repo.session.commit()
        return {
            'msg': 'Please check your email, copy the sent code, you will need it to continue registration.',
        }
