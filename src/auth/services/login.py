from datetime import datetime
from typing import Optional
from uuid import uuid4

import config
from src.auth import jwt, exceptions
from src.auth.domain import model
from src.auth.security import check_password_hash
from src.base.aliases import TypeUoW
from src.base.send_email import send_email
from src.base.uow import UnitOfWork
from worker import remove_bad_login


# TODO add otp
def login(
    *, username: str, password: str, ip_address: Optional[str] = None, uow: TypeUoW = UnitOfWork(),
) -> jwt.LoginTokens:

    with uow:
        if '@' in username:
            user = uow.users.get(email=username)
        else:
            user = uow.users.get(username=username)

        if user is None:
            raise exceptions.InvalidUsernameOrPassword('Invalid username or password.')

        if not check_password_hash(password=password, hashed_password=user.password):
            bad_login = model.BadLogin(uuid=f'{uuid4()}', ip_address=ip_address)
            uow.bad_logins.add(bad_login=bad_login)

            remove_bad_login(uuid=bad_login.uuid)

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
