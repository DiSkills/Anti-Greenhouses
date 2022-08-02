from datetime import datetime
from typing import Optional
from uuid import uuid4

import config
from src.auth.domain import model
from src.auth.entrypoints.schemas.users import Registration
from src.auth.services import exceptions, jwt
from src.base.aliases import TypeUoW
from src.base.uow import UnitOfWork
from src.base.send_email import send_email


def registration_request(*, email: str, uow: TypeUoW = UnitOfWork()) -> None:

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

        verification = model.Verification(email=email, uuid=f'{uuid4()}')
        uow.verifications.add(verification=verification)
        uow.commit()

        send_email(
            subject='[Anti-Greenhouses] Your registration code',
            recipient=email,
            text=f'Your registration code: {verification.uuid}',
        )


def registration(
    *, schema: Registration, ip_address: Optional[str] = None, uow: TypeUoW = UnitOfWork(),
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
            uuid=f'{uuid4()}',
            type=config.UserActionType.registered,
            created_at=datetime.utcnow(),
            ip_address=ip_address,
        )
        model.add_action(action=action, user=user)
        uow.commit()


# TODO add otp
def login(
    *,
    username: str,
    password: str,
    ip_address: Optional[str] = None,
    uow: TypeUoW = UnitOfWork(),
) -> jwt.LoginTokens:
    with uow:
        if '@' in username:
            user = uow.users.get(email=username)
        else:
            user = uow.users.get(username=username)

        if user is None:
            raise exceptions.InvalidUsernameOrPassword('Invalid username or password.')

        if not model.check_password_hash(password=password, hashed_password=user.password):
            bad_login = model.BadLogin(uuid=f'{uuid4()}', ip_address=ip_address)
            uow.bad_logins.add(bad_login=bad_login)

            # TODO celery task

            uow.commit()
            raise exceptions.InvalidUsernameOrPassword('Invalid username or password.')

        send_email(
            subject='[Anti-Greenhouses] New login to your account',
            recipient=user.email,
            text=f'Logged into your account with ip: {ip_address}',
        )
        action = model.UserAction(
            uuid=f'{uuid4()}',
            type=config.UserActionType.login,
            created_at=datetime.utcnow(),
            ip_address=ip_address,
        )
        model.add_action(action=action, user=user)
        uow.commit()
        return jwt.create_login_tokens(username=user.username, uuid=user.uuid, is_superuser=user.is_superuser)
