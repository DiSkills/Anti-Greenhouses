import uuid
from typing import Union

from src.auth.domain import model
from src.auth.services import exceptions
from src.auth.services.uow import UnitOfWork
from src.base.send_email import send_email
from tests.auth.fake_uow import FakeUnitOfWork


def registration_request(*, email: str, uow: Union[UnitOfWork, FakeUnitOfWork] = UnitOfWork()) -> None:

    with uow:
        if uow.users.get(email=email) is not None:
            raise exceptions.UserWithEmailExists('User with this email exists.')

        verification = uow.verifications.get(email=email)
        if verification is not None:

            send_email(
                subject='[Anti-Greenhouses] Your registration code',
                recipient=email,
                text=f'We re-send your code: {verification.uuid}',
            )

            raise exceptions.VerificationExists(
                'Verification with this email already exists, we sent you another email with a code.',
            )

        verification = model.Verification(email=email, uuid=f'{uuid.uuid4()}')
        uow.verifications.add(verification=verification)
        uow.commit()

        send_email(
            subject='[Anti-Greenhouses] Your registration code',
            recipient=email,
            text=f'Your registration code: {verification.uuid}',
        )
