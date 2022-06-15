import uuid
from typing import Union

from sqlalchemy.orm import Session

from src.auth.adapters.repositories.verification import VerificationRepository
from src.auth.domain import model
from src.auth.services import exceptions
from tests.auth.fake_repositories import FakeSession, FakeVerificationRepository


# TODO add error when user with this email exists
def registration_request(
    *,
    email: str,
    repository: Union[VerificationRepository, FakeVerificationRepository],
    session: Union[Session, FakeSession],
) -> None:

    if repository.get(email=email) is not None:
        # TODO send email
        raise exceptions.VerificationExists(
            'Verification with this email already exists, we sent you another email with a code.',
        )

    # TODO send email
    repository.add(verification=model.Verification(email=email, uuid=f'{uuid.uuid4()}'))
    session.commit()
