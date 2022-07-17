import uuid

import pytest
from pydantic import EmailStr

import config
from src.auth.domain import model
from src.auth.entrypoints.schemas.users import Registration, Password
from src.auth.services import services, exceptions
from tests.base.fake_uow import FakeUnitOfWork


def _create_registration_schema(username: str, uuid: str, email: str, password: str) -> Registration:
    return Registration(
        username=username,
        uuid=uuid,
        email=EmailStr(email),
        password=Password(password),
        confirm_password=password,
    )


def test_registration_request_create_a_verification(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False

    services.registration_request(email='user@example.com', uow=uow)

    assert uow.committed is True


def test_registration_request_verification_with_this_email_exists(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False
    uow.verifications.add(verification=model.Verification(email='user@example.com', uuid=f'{uuid.uuid4()}'))

    error_text = 'Verification with this email already exists, we sent you another email with a code.'
    with pytest.raises(exceptions.VerificationExists, match=error_text):
        services.registration_request(email='user@example.com', uow=uow)

    assert uow.committed is False


def test_registration_request_user_with_this_email_exists(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False
    uow.users.add(user=model.User(username='test', email='user@example.com', password='password', otp_secret='secret'))

    error_text = 'User with this email exists.'
    with pytest.raises(exceptions.UserWithEmailExists, match=error_text):
        services.registration_request(email='user@example.com', uow=uow)

    assert uow.committed is False


def test_registration_create_user():
    uow = FakeUnitOfWork()
    assert uow.committed is False

    _uuid = f'{uuid.uuid4()}'
    email = 'user@example.com'

    uow.verifications.add(verification=model.Verification(uuid=_uuid, email=email))
    schema = _create_registration_schema(username='test', uuid=_uuid, email=email, password='Admin2248!')

    services.registration(schema=schema, uow=uow)

    assert len(uow.verifications._verifications) == 0
    assert len(uow.users._users) == 1

    user = uow.users.get(username='test')
    assert user is not None
    assert user.password != 'Admin2248!'
    assert model.check_password_hash(password='Admin2248!', hashed_password=user.password) is True
    assert user.count_actions == 1
    assert user.actions[0].type == config.UserActionType.registered

    assert uow.committed is True


def test_registration_user_with_this_username_exists():
    uow = FakeUnitOfWork()
    assert uow.committed is False

    _uuid = f'{uuid.uuid4()}'

    uow.users.add(user=model.User(username='test', email='user@example.com', password='password'))
    schema = _create_registration_schema(username='test', email='user@example.com', uuid=_uuid, password='Admin2248!')

    error_text = 'User with this username exists.'
    with pytest.raises(exceptions.UserWithUsernameExists, match=error_text):
        services.registration(schema=schema, uow=uow)

    assert uow.committed is False


def test_registration_user_with_this_email_exists():
    uow = FakeUnitOfWork()
    assert uow.committed is False

    _uuid = f'{uuid.uuid4()}'

    uow.users.add(user=model.User(username='user', email='user@example.com', password='password'))
    schema = _create_registration_schema(username='test', email='user@example.com', uuid=_uuid, password='Admin2248!')

    error_text = 'User with this email exists.'
    with pytest.raises(exceptions.UserWithEmailExists, match=error_text):
        services.registration(schema=schema, uow=uow)

    assert uow.committed is False


def test_registration_invalid_verification_uuid(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False

    _uuid = f'{uuid.uuid4()}'
    email = 'user@example.com'

    uow.verifications.add(verification=model.Verification(uuid=_uuid, email=email))

    # Verification by uuid not found, but found by email
    schema = _create_registration_schema(username='test', email=email, password='Admin2248!', uuid='bad-uuid')

    error_text = 'Verification with this uuid was not found. We sent you another email with a code.'
    with pytest.raises(exceptions.BadVerificationUUID, match=error_text):
        services.registration(schema=schema, uow=uow)

    assert uow.committed is False


def test_registration_verification_not_found():
    uow = FakeUnitOfWork()
    assert uow.committed is False

    schema = _create_registration_schema(
        username='test', uuid='bad-uuid', email='user@example.com', password='Admin2248!',
    )

    error_text = 'Verification with this email address was not found.'
    with pytest.raises(exceptions.VerificationNotFound, match=error_text):
        services.registration(schema=schema, uow=uow)

    assert uow.committed is False
