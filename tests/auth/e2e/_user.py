from datetime import datetime
from uuid import uuid4

from tests.conftest import TestData


def _create_user(
    *,
    e2e,
    username: str = TestData.username.test,
    email: str = TestData.email.user,
    password: str = TestData.password.strong,
) -> None:
    e2e.session.execute(
        'INSERT INTO users (username, email, password, otp_secret, otp, is_superuser, avatar, date_joined, uuid)'
        ' VALUES (:username, :email, :password, :secret, FALSE, FALSE, NULL, :date_joined, :uuid)',
        {
            'username': username,
            'email': email,
            'password': password,
            'secret': 'secret',
            'date_joined': datetime.utcnow(),
            'uuid': f'{uuid4()}',
        },
    )
    e2e.session.commit()
