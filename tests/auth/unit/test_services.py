from uuid import uuid4

import jwt
import pytest
from pydantic import EmailStr

import config
from src.auth.domain import model
from src.auth.entrypoints.schemas.users import Registration, Password
from src.auth.services import services, exceptions
from tests.base.fake_uow import FakeUnitOfWork
from tests.conftest import TestData


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

    services.registration_request(email=TestData.email.user, uow=uow)

    assert uow.committed is True


def test_registration_request_verification_with_this_email_exists(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False
    uow.verifications.add(verification=model.Verification(email=TestData.email.user, uuid=f'{uuid4()}'))

    error_text = 'Verification with this email already exists, we sent you another email with a code.'
    with pytest.raises(exceptions.VerificationExists, match=error_text):
        services.registration_request(email=TestData.email.user, uow=uow)

    assert uow.committed is False


def test_registration_request_user_with_this_email_exists(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False
    uow.users.add(
        user=model.User(username=TestData.username.test, email=TestData.email.user, password=TestData.password.password)
    )

    error_text = 'User with this email exists.'
    with pytest.raises(exceptions.UserWithEmailExists, match=error_text):
        services.registration_request(email=TestData.email.user, uow=uow)

    assert uow.committed is False


def test_registration_create_user():
    uow = FakeUnitOfWork()
    assert uow.committed is False

    uuid = f'{uuid4()}'
    email = TestData.email.user

    uow.verifications.add(verification=model.Verification(uuid=uuid, email=email))
    schema = _create_registration_schema(
        username=TestData.username.test, uuid=uuid, email=email, password=TestData.password.strong,
    )

    services.registration(schema=schema, uow=uow)

    assert len(uow.verifications._verifications) == 0
    assert len(uow.users._users) == 1

    user = uow.users.get(username=TestData.username.test)
    assert user is not None
    assert user.password != TestData.password.strong
    assert model.check_password_hash(password=TestData.password.strong, hashed_password=user.password) is True
    assert user.count_actions == 1
    assert user.actions[0].type == config.UserActionType.registered

    assert uow.committed is True


def test_registration_user_with_this_username_exists():
    uow = FakeUnitOfWork()
    assert uow.committed is False

    uuid = f'{uuid4()}'

    uow.users.add(
        user=model.User(username=TestData.username.test, email=TestData.email.user, password=TestData.password.password)
    )
    schema = _create_registration_schema(
        username=TestData.username.test, email=TestData.email.user, uuid=uuid, password=TestData.password.strong,
    )

    error_text = 'User with this username exists.'
    with pytest.raises(exceptions.UserWithUsernameExists, match=error_text):
        services.registration(schema=schema, uow=uow)

    assert uow.committed is False


def test_registration_user_with_this_email_exists():
    uow = FakeUnitOfWork()
    assert uow.committed is False

    uuid = f'{uuid4()}'

    uow.users.add(
        user=model.User(username=TestData.username.user, email=TestData.email.user, password=TestData.password.password)
    )
    schema = _create_registration_schema(
        username=TestData.username.test, email=TestData.email.user, uuid=uuid, password=TestData.password.strong
    )

    error_text = 'User with this email exists.'
    with pytest.raises(exceptions.UserWithEmailExists, match=error_text):
        services.registration(schema=schema, uow=uow)

    assert uow.committed is False


def test_registration_invalid_verification_uuid(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False

    uuid = f'{uuid4()}'
    email = TestData.email.user

    uow.verifications.add(verification=model.Verification(uuid=uuid, email=email))

    # Verification by uuid not found, but found by email
    schema = _create_registration_schema(
        username=TestData.username.test, email=email, password=TestData.password.strong, uuid='bad-uuid',
    )

    error_text = 'Verification with this uuid was not found. We sent you another email with a code.'
    with pytest.raises(exceptions.BadVerificationUUID, match=error_text):
        services.registration(schema=schema, uow=uow)

    assert uow.committed is False


def test_registration_verification_not_found():
    uow = FakeUnitOfWork()
    assert uow.committed is False

    schema = _create_registration_schema(
        username=TestData.username.test, uuid='bad-uuid', email=TestData.email.user, password=TestData.password.strong,
    )

    error_text = 'Verification with this email address was not found.'
    with pytest.raises(exceptions.VerificationNotFound, match=error_text):
        services.registration(schema=schema, uow=uow)

    assert uow.committed is False


def test_login_by_username_create_tokens(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False
    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 0

    password = model.get_password_hash(password=TestData.password.password)
    uow.users.add(user=model.User(username=TestData.username.user, email=TestData.email.user, password=password))

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 0

    tokens = services.login(username=TestData.username.user, password=TestData.password.password, uow=uow)

    # Access
    decoded = jwt.decode(tokens.access, config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.user,
        'is_superuser': False,
        'uuid': user.uuid,
        'subject': config.JWTConfig.access_subject,
        'exp': decoded.get('exp'),
    }

    # Refresh
    decoded = jwt.decode(tokens.refresh, config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.user,
        'is_superuser': False,
        'uuid': user.uuid,
        'subject': config.JWTConfig.refresh_subject,
        'exp': decoded.get('exp'),
    }

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 1
    assert user.actions[0].type == config.UserActionType.login

    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 0
    assert uow.committed is True


def test_login_by_email_create_tokens(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False
    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 0

    password = model.get_password_hash(password=TestData.password.password)
    uow.users.add(user=model.User(username=TestData.username.user, email=TestData.email.user, password=password))

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 0

    tokens = services.login(username=TestData.email.user, password=TestData.password.password, uow=uow)

    # Access
    decoded = jwt.decode(tokens.access, config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.user,
        'is_superuser': False,
        'uuid': user.uuid,
        'subject': config.JWTConfig.access_subject,
        'exp': decoded.get('exp'),
    }

    # Refresh
    decoded = jwt.decode(tokens.refresh, config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.user,
        'is_superuser': False,
        'uuid': user.uuid,
        'subject': config.JWTConfig.refresh_subject,
        'exp': decoded.get('exp'),
    }

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 1
    assert user.actions[0].type == config.UserActionType.login

    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 0
    assert uow.committed is True


def test_login_invalid_username():
    uow = FakeUnitOfWork()
    assert uow.committed is False

    # Username
    with pytest.raises(exceptions.InvalidUsernameOrPassword, match='Invalid username or password.'):
        services.login(username=TestData.username.bot, password=TestData.password.password, uow=uow)
    assert uow.committed is False

    # Email
    with pytest.raises(exceptions.InvalidUsernameOrPassword, match='Invalid username or password.'):
        services.login(username=TestData.email.user, password=TestData.password.password, uow=uow)
    assert uow.committed is False


def test_login_invalid_password(mocker):
    mocker.patch('worker.remove_bad_login', return_value=None)
    mocker.patch('worker.remove_bad_login_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False
    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 0

    password = model.get_password_hash(password=TestData.password.strong)
    uow.users.add(user=model.User(username=TestData.username.user, email=TestData.email.user, password=password))

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 0

    with pytest.raises(exceptions.InvalidUsernameOrPassword, match='Invalid username or password.'):
        services.login(
            username=TestData.email.user, password=TestData.password.password, ip_address=TestData.ip_address, uow=uow,
        )

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 0

    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 1
    assert uow.committed is True
