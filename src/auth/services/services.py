import uuid
from typing import Union

from src.auth.domain import model
from src.auth.services import exceptions
from src.auth.services.uow.verifications import VerificationUnitOfWork
from tests.auth.fake_uow import FakeVerificationUnitOfWork


# TODO add error when user with this email exists
def registration_request(
    *,
    email: str,
    uow: Union[VerificationUnitOfWork, FakeVerificationUnitOfWork],
) -> None:

    with uow:
        if uow.verifications.get(email=email) is not None:
            # TODO send email
            raise exceptions.VerificationExists(
                'Verification with this email already exists, we sent you another email with a code.',
            )

        # TODO send email
        uow.verifications.add(verification=model.Verification(email=email, uuid=f'{uuid.uuid4()}'))
        uow.commit()
