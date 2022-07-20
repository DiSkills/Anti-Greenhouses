from uuid import uuid4

from src.auth.adapters.repositories.verification.repository import VerificationRepository
from src.auth.domain import model
from tests.conftest import TestData


def test_repository_can_save_a_verification(mongo_verifications):
    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ()

    uuid = f'{uuid4()}'
    verification = model.Verification(email=TestData.email.user, uuid=uuid)

    repo = VerificationRepository(collection=mongo_verifications)
    repo.add(verification=verification)

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ({'email': TestData.email.user, 'uuid': uuid},)


def test_repository_can_retrieve_a_verification(mongo_verifications):
    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'

    mongo_verifications.insert_many(
        [{'email': TestData.email.user, 'uuid': uuid1}, {'email': TestData.email.python, 'uuid': uuid2}],
    )

    expected = model.Verification(email=TestData.email.python, uuid=uuid2)
    repo = VerificationRepository(collection=mongo_verifications)

    # Get by email
    retrieved = repo.get(email=TestData.email.python)
    assert expected == retrieved

    # Get by uuid
    retrieved = repo.get(uuid=uuid1)
    assert retrieved == model.Verification(email=TestData.email.user, uuid=uuid1)


def test_repository_can_not_retrieve_a_verification(mongo_verifications):
    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'

    mongo_verifications.insert_many(
        [{'email': TestData.email.user, 'uuid': uuid1}, {'email': TestData.email.python, 'uuid': uuid2}],
    )

    repo = VerificationRepository(collection=mongo_verifications)

    retrieved = repo.get(email=TestData.email.bot)
    assert retrieved is None


def test_repository_can_remove_verification_by_email(mongo_verifications):
    uuid1, uuid2 = f'{uuid4()}', f'{uuid4()}'

    mongo_verifications.insert_many(
        [{'email': TestData.email.user, 'uuid': uuid1}, {'email': TestData.email.python, 'uuid': uuid2}],
    )

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == (
        {'email': TestData.email.user, 'uuid': uuid1}, {'email': TestData.email.python, 'uuid': uuid2},
    )

    repo = VerificationRepository(collection=mongo_verifications)
    repo.remove(email=TestData.email.user)

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ({'email': TestData.email.python, 'uuid': uuid2},)


def test_repository_can_remove_verification_by_uuid(mongo_verifications):
    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'

    mongo_verifications.insert_many(
        [{'email': TestData.email.user, 'uuid': uuid1}, {'email': TestData.email.python, 'uuid': uuid2}],
    )

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == (
        {'email': TestData.email.user, 'uuid': uuid1}, {'email': TestData.email.python, 'uuid': uuid2},
    )

    repo = VerificationRepository(collection=mongo_verifications)
    repo.remove(uuid=uuid1)

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ({'email': TestData.email.python, 'uuid': uuid2},)
