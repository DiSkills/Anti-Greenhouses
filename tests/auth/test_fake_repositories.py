from uuid import uuid4

from src.auth.domain import model
from tests.auth import fake_repositories


def test_add_a_verification():
    session = fake_repositories.FakeSession()
    repository = fake_repositories.FakeVerificationRepository(session=session, verifications=[])
    assert repository._verifications == set()

    verification = model.Verification(email='user@example.com', uuid=f'{uuid4()}')
    repository.add(verification=verification)
    assert repository._verifications == {verification}


def test_add_verifications():
    session = fake_repositories.FakeSession()
    repository = fake_repositories.FakeVerificationRepository(session=session, verifications=[])
    assert repository._verifications == set()

    verification1 = model.Verification(email='user@example.com', uuid=f'{uuid4()}')
    repository.add(verification=verification1)
    assert repository._verifications == {verification1}

    verification2 = model.Verification(email='user-2@example.com', uuid=f'{uuid4()}')
    repository.add(verification=verification2)
    assert repository._verifications == {verification1, verification2}


def test_get_verification():
    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'

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
    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'

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


def test_add_a_user():
    session = fake_repositories.FakeSession()
    repository = fake_repositories.FakeUserRepository(session=session, users=[])
    assert repository._users == set()

    user = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    repository.add(user=user)
    assert repository._users == {user}


def test_add_users():
    session = fake_repositories.FakeSession()
    repository = fake_repositories.FakeUserRepository(session=session, users=[])
    assert repository._users == set()

    user1 = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    repository.add(user=user1)
    assert repository._users == {user1}

    user2 = model.User(username='test2', email='user2@example.com', password='password', otp_secret='secret')
    repository.add(user=user2)
    assert repository._users == {user1, user2}


def test_get_user():
    session = fake_repositories.FakeSession()
    user1 = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    user2 = model.User(username='test2', email='user2@example.com', password='password', otp_secret='secret')
    repository = fake_repositories.FakeUserRepository(session=session, users=[user1, user2])
    assert repository._users == {user1, user2}

    # By username
    retrieved = repository.get(username='test')
    assert retrieved == user1

    retrieved = repository.get(username='bot')
    assert retrieved is None

    # By email
    retrieved = repository.get(email='user2@example.com')
    assert retrieved == user2

    retrieved = repository.get(email='hello@world.com')
    assert retrieved is None

    # By username & email
    retrieved = repository.get(username='test', email='user@example.com')
    assert retrieved == user1

    retrieved = repository.get(username='test', email='hello@example.com')
    assert retrieved is None

    retrieved = repository.get(username='bot', email='user@example.com')
    assert retrieved is None

    retrieved = repository.get(username='bot', email='bot@example.com')
    assert retrieved is None

    # By hello
    retrieved = repository.get(hello='world!')
    assert retrieved is None
