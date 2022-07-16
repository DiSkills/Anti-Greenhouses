import uuid
from datetime import datetime
from typing import Union, Optional

import config
from src.auth.domain import model
from src.auth.entrypoints.schemas.users import Registration
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


def registration(
    *, schema: Registration, ip_address: Optional[str] = None, uow: Union[UnitOfWork, FakeUnitOfWork] = UnitOfWork(),
) -> None:

    with uow:
        if uow.users.get(username=schema.username) is not None:
            raise exceptions.UserWithUsernameExists('User with this username exists.')

        if uow.users.get(email=schema.email) is not None:
            raise exceptions.UserWithEmailExists('User with this email exists.')

        verification = uow.verifications.get(email=schema.email)
        if verification is None:
            raise exceptions.VerificationNotFound('Verification with this email address was not found.')

        if verification.uuid != schema.uuid:

            send_email(
                subject='[Anti-Greenhouses] Your registration code',
                recipient=schema.email,
                text=f'We re-send your code: {verification.uuid}',
            )

            raise exceptions.BadVerificationUUID(
                'Verification with this uuid was not found. We sent you another email with a code.',
            )

        uow.verifications.remove(uuid=schema.uuid)
        user = model.User(
            username=schema.username,
            email=schema.email,
            password=model.get_password_hash(password=schema.password),
        )
        uow.users.add(user=user)

        action = model.UserAction(
            uuid=f'{uuid.uuid4()}',
            type=config.UserActionType.registered,
            created_at=datetime.utcnow(),
            ip_address=ip_address,
        )
        model.add_action(action=action, user=user)
        uow.commit()
