import uuid

import pytest

from src.auth.domain import model
from src.auth.services import services, exceptions
from tests.auth import fake_uow


def test_registration_request_create_a_verification(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = fake_uow.FakeUnitOfWork()
    assert uow.committed is False

    services.registration_request(email='user@example.com', uow=uow)

    assert uow.committed is True


def test_registration_request_verification_with_this_email_exists(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = fake_uow.FakeUnitOfWork()
    assert uow.committed is False
    uow.verifications.add(verification=model.Verification(email='user@example.com', uuid=f'{uuid.uuid4()}'))

    error_text = 'Verification with this email already exists, we sent you another email with a code.'
    with pytest.raises(exceptions.VerificationExists, match=error_text):
        services.registration_request(email='user@example.com', uow=uow)

    assert uow.committed is False


def test_registration_request_user_with_this_email_exists(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = fake_uow.FakeUnitOfWork()
    assert uow.committed is False
    uow.users.add(user=model.User(username='test', email='user@example.com', password='password', otp_secret='secret'))

    error_text = 'User with this email exists.'
    with pytest.raises(exceptions.UserWithEmailExists, match=error_text):
        services.registration_request(email='user@example.com', uow=uow)

    assert uow.committed is False
