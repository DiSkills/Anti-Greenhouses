from uuid import uuid4

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
    uow.users.add(user=model.User(username='test', email=TestData.email.user, password=TestData.password.password))

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
