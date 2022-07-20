from datetime import datetime
from typing import Literal
from uuid import uuid4

from fastapi import status
from typing_extensions import TypeAlias

from config import MongoTables
from main import app
from src.auth.domain import model
from tests.conftest import TestData

registration_data: TypeAlias = dict[Literal['username', 'email', 'password', 'confirm_password', 'uuid'], str]


def _get_registration_data(
    *,
    uuid: str,
    username: str = TestData.username.test,
    email: str = TestData.email.user,
    password: str = TestData.password.strong,
) -> registration_data:
    return {
        'username': username,
        'email': email,
        'password': password,
        'confirm_password': password,
        'uuid': uuid,
    }


def _create_user(
    *,
    e2e,
    username: str = TestData.username.test,
    email: str = TestData.email.user,
    password: str = TestData.password.strong,
) -> None:
    e2e.session.execute(
        'INSERT INTO users (username, email, password, otp_secret, otp, is_superuser, avatar, date_joined)'
        ' VALUES (:username, :email, :password, :secret, FALSE, FALSE, NULL, :date_joined)',
        {
            'username': username,
            'email': email,
            'password': password,
            'secret': 'secret',
            'date_joined': datetime.utcnow(),
        },
    )
    e2e.session.commit()


def _create_verification(*, e2e, email: str = TestData.email.user) -> str:
    mongo_verifications = e2e.mongo[MongoTables.verifications.name]

    uuid = f'{uuid4()}'
    mongo_verifications.insert_one({'email': email, 'uuid': uuid})
    return uuid


def test_registration_return_201_and_create_user(e2e):
    mongo_verifications = e2e.mongo[MongoTables.verifications.name]

    # Create verification
    uuid = _create_verification(e2e=e2e)

    # Database check
    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ({'email': TestData.email.user, 'uuid': uuid},)
    rows = tuple(e2e.session.execute('SELECT * FROM "users"'))
    assert rows == ()
    rows = tuple(e2e.session.execute('SELECT * FROM "user_actions"'))
    assert rows == ()
    rows = tuple(e2e.session.execute('SELECT * FROM "actions"'))
    assert rows == ()

    # Send request
    response = e2e.client.post(f'{app.url_path_for("registration")}', json=_get_registration_data(uuid=uuid))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'msg': 'You have been successfully registered on our website!'}

    # Database check
    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ()
    rows = tuple(e2e.session.execute('SELECT username FROM "users"'))
    assert rows == ((TestData.username.test,),)

    password, = tuple(e2e.session.execute('SELECT password FROM "users"'))[0]
    assert model.check_password_hash(password=TestData.password.strong, hashed_password=password) is True

    # Check actions
    rows = tuple(e2e.session.execute('SELECT id, user_id, action_id FROM "user_actions"'))
    assert rows == ((1, 1, 1),)
    rows = tuple(e2e.session.execute('SELECT type, ip_address FROM "actions"'))
    assert rows == (('registered', None),)


def test_registration_return_400_when_user_with_this_username_exists(e2e):
    _create_user(e2e=e2e)
    rows = tuple(e2e.session.execute('SELECT username FROM "users"'))
    assert rows == ((TestData.username.test,),)

    response = e2e.client.post(f'{app.url_path_for("registration")}', json=_get_registration_data(uuid='bad-uuid'))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'User with this username exists.'}

    rows = tuple(e2e.session.execute('SELECT username FROM "users"'))
    assert rows == ((TestData.username.test,),)


def test_registration_return_400_when_user_with_this_email_exists(e2e):
    _create_user(e2e=e2e, username='user')
    rows = tuple(e2e.session.execute('SELECT email FROM "users"'))
    assert rows == ((TestData.email.user,),)

    response = e2e.client.post(f'{app.url_path_for("registration")}', json=_get_registration_data(uuid='bad-uuid'))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'User with this email exists.'}

    rows = tuple(e2e.session.execute('SELECT email FROM "users"'))
    assert rows == ((TestData.email.user,),)


def test_registration_return_400_when_invalid_verification_uuid(mocker, e2e):
    mongo_verifications = e2e.mongo[MongoTables.verifications.name]
    mocker.patch('worker.send_email_task', return_value=None)
    mocker.patch('src.base.send_email.send_email', return_value=None)

    # Create verification
    uuid = _create_verification(e2e=e2e)

    # Database check
    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ({'email': TestData.email.user, 'uuid': uuid},)
    rows = tuple(e2e.session.execute('SELECT * FROM "users"'))
    assert rows == ()

    # Send request
    response = e2e.client.post(f'{app.url_path_for("registration")}', json=_get_registration_data(uuid='bad-uuid'))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'Verification with this uuid was not found. We sent you another email with a code.',
    }

    # Database check
    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ({'email': TestData.email.user, 'uuid': uuid},)
    rows = tuple(e2e.session.execute('SELECT * FROM "users"'))
    assert rows == ()


def test_registration_return_400_when_verification_not_found(e2e):
    rows = tuple(e2e.session.execute('SELECT * FROM "users"'))
    assert rows == ()

    response = e2e.client.post(f'{app.url_path_for("registration")}', json=_get_registration_data(uuid='bad-uuid'))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Verification with this email address was not found.'}

    rows = tuple(e2e.session.execute('SELECT * FROM "users"'))
    assert rows == ()
