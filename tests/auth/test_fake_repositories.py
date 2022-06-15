import uuid

from src.auth.domain import model
from tests.auth import fake_repositories


def test_add_a_verification():
    session = fake_repositories.FakeSession()
    repository = fake_repositories.FakeVerificationRepository(session=session, verifications=[])
    assert repository._verifications == set()

    verification = model.Verification(email='user@example.com', uuid=f'{uuid.uuid4()}')
    repository.add(verification=verification)
    assert repository._verifications == {verification}


def test_add_verifications():
    session = fake_repositories.FakeSession()
    repository = fake_repositories.FakeVerificationRepository(session=session, verifications=[])
    assert repository._verifications == set()

    verification1 = model.Verification(email='user@example.com', uuid=f'{uuid.uuid4()}')
    repository.add(verification=verification1)
    assert repository._verifications == {verification1}

    verification2 = model.Verification(email='user-2@example.com', uuid=f'{uuid.uuid4()}')
    repository.add(verification=verification2)
    assert repository._verifications == {verification1, verification2}


def test_get_verification():
    uuid1 = f'{uuid.uuid4()}'
    uuid2 = f'{uuid.uuid4()}'

    session = fake_repositories.FakeSession()
    verification1 = model.Verification(email='user@example.com', uuid=f'{uuid1}')
    verification2 = model.Verification(email='user-2@example.com', uuid=f'{uuid2}')
    repository = fake_repositories.FakeVerificationRepository(
        session=session, verifications=[verification1, verification2],
    )
    assert repository._verifications == {verification1, verification2}

    # By email
    retrieved = repository.get(email='user@example.com')
    assert retrieved == verification1

    retrieved = repository.get(email='python@example.com')
    assert retrieved is None

    # By uuid
    retrieved = repository.get(uuid=uuid2)
    assert retrieved == verification2

    retrieved = repository.get(uuid='hello-world!')
    assert retrieved is None

    # By email & uuid
    retrieved = repository.get(email='user@example.com', uuid=uuid1)
    assert retrieved == verification1

    retrieved = repository.get(email='user@example.com', uuid='hello-world!')
    assert retrieved is None

    retrieved = repository.get(email='python@example.com', uuid=uuid1)
    assert retrieved is None

    retrieved = repository.get(email='python@example.com', uuid='hello-world!')
    assert retrieved is None

    # By hello
    retrieved = repository.get(hello='world!')
    assert retrieved is None


def test_remove_a_verification():
    uuid1 = f'{uuid.uuid4()}'
    uuid2 = f'{uuid.uuid4()}'

    session = fake_repositories.FakeSession()
    verification1 = model.Verification(email='user@example.com', uuid=f'{uuid1}')
    verification2 = model.Verification(email='user-2@example.com', uuid=f'{uuid2}')
    repository = fake_repositories.FakeVerificationRepository(
        session=session, verifications=[verification1, verification2],
    )
    assert repository._verifications == {verification1, verification2}

    # By email
    repository.remove(email='user@example.com')
    assert repository._verifications == {verification2}

    # By hello
    repository.remove(hello='world!')
    assert repository._verifications == {verification2}

    # By uuid
    repository.remove(uuid=uuid2)
    assert repository._verifications == set()

    repository.remove(uuid='hello-world!')
    assert repository._verifications == set()
