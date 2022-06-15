import uuid

import pytest

from src.auth.domain import model
from src.auth.services import services, exceptions
from tests.auth import fake_repositories


def test_registration_request_create_a_verification():
    session = fake_repositories.FakeSession()

    repo = fake_repositories.FakeVerificationRepository(session=session, verifications=[])

    assert repo.session.committed is False

    services.registration_request(email='user@example.com', repository=repo)

    assert repo.session.committed is True


def test_registration_request_verification_with_this_email_exists():
    session = fake_repositories.FakeSession()

    verifications = [model.Verification(email='user@example.com', uuid=f'{uuid.uuid4()}')]
    repo = fake_repositories.FakeVerificationRepository(session=session, verifications=verifications)

    assert repo.session.committed is False

    error_text = 'Verification with this email already exists, we sent you another email with a code.'
    with pytest.raises(exceptions.VerificationExists, match=error_text):
        services.registration_request(email='user@example.com', repository=repo)

    assert repo.session.committed is False
