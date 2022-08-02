from uuid import uuid4

import pytest

from src.auth.domain import model
from src.auth.services.exceptions import UserWithEmailExists, VerificationExists
from src.auth.services.services import registration_request
from tests.base.fake_uow import FakeUnitOfWork
from tests.conftest import TestData


def test_registration_request_create_a_verification(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False

    registration_request(email=TestData.email.user, uow=uow)

    assert uow.committed is True


def test_registration_request_verification_with_this_email_exists(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False
    uow.verifications.add(verification=model.Verification(email=TestData.email.user, uuid=f'{uuid4()}'))

    error_text = 'Verification with this email already exists, we sent you another email with a code.'
    with pytest.raises(VerificationExists, match=error_text):
        registration_request(email=TestData.email.user, uow=uow)

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
    with pytest.raises(UserWithEmailExists, match=error_text):
        registration_request(email=TestData.email.user, uow=uow)

    assert uow.committed is False
