from uuid import uuid4

from src.auth.domain import model
from tests.auth import fake_repositories
from tests.conftest import TestData


def _create_verification_repository(
    *, verifications: list[model.Verification],
) -> fake_repositories.FakeVerificationRepository:
    session = fake_repositories.FakeSession()
    return fake_repositories.FakeVerificationRepository(session=session, verifications=verifications)


def _create_user_repository(*, users: list[model.User]) -> fake_repositories.FakeUserRepository:
    session = fake_repositories.FakeSession()
    return fake_repositories.FakeUserRepository(session=session, users=users)


def test_add_a_verification():
    repository = _create_verification_repository(verifications=[])
    assert repository._verifications == set()

    verification = model.Verification(email=TestData.email.user, uuid=f'{uuid4()}')
    repository.add(verification=verification)
    assert repository._verifications == {verification}


def test_add_verifications():
    repository = _create_verification_repository(verifications=[])
    assert repository._verifications == set()

    verification1 = model.Verification(email=TestData.email.user, uuid=f'{uuid4()}')
    repository.add(verification=verification1)
    assert repository._verifications == {verification1}

    verification2 = model.Verification(email=TestData.email.user2, uuid=f'{uuid4()}')
    repository.add(verification=verification2)
    assert repository._verifications == {verification1, verification2}


def test_get_verification():
    uuid1, uuid2 = f'{uuid4()}', f'{uuid4()}'
    verifications = [
        model.Verification(email=TestData.email.user, uuid=f'{uuid1}'),
        model.Verification(email=TestData.email.user2, uuid=f'{uuid2}'),
    ]
    repository = _create_verification_repository(verifications=verifications)
    assert repository._verifications == {verifications[0], verifications[1]}

    # By email
    retrieved = repository.get(email=TestData.email.user)
    assert retrieved == verifications[0]

    retrieved = repository.get(email=TestData.email.python)
    assert retrieved is None

    # By uuid
    retrieved = repository.get(uuid=uuid2)
    assert retrieved == verifications[1]

    retrieved = repository.get(uuid='hello-world!')
    assert retrieved is None

    # By email & uuid
    retrieved = repository.get(email=TestData.email.user, uuid=uuid1)
    assert retrieved == verifications[0]

    retrieved = repository.get(email=TestData.email.user, uuid='hello-world!')
    assert retrieved is None

    retrieved = repository.get(email=TestData.email.python, uuid=uuid1)
    assert retrieved is None

    retrieved = repository.get(email=TestData.email.python, uuid='hello-world!')
    assert retrieved is None

    # By hello
    retrieved = repository.get(hello='world!')
    assert retrieved is None


def test_remove_a_verification():
    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'

    verifications = [
        model.Verification(email=TestData.email.user, uuid=f'{uuid1}'),
        model.Verification(email=TestData.email.user2, uuid=f'{uuid2}'),
    ]
    repository = _create_verification_repository(verifications=verifications)
    assert repository._verifications == {verifications[0], verifications[1]}

    # By email
    repository.remove(email=TestData.email.user)
    assert repository._verifications == {verifications[1]}

    # By hello
    repository.remove(hello='world!')
    assert repository._verifications == {verifications[1]}

    # By uuid
    repository.remove(uuid=uuid2)
    assert repository._verifications == set()

    repository.remove(uuid='hello-world!')
    assert repository._verifications == set()


def test_add_a_user():
    repository = _create_user_repository(users=[])
    assert repository._users == set()

    user = model.User(username=TestData.username.test, email=TestData.email.user, password=TestData.password.password)
    repository.add(user=user)
    assert repository._users == {user}


def test_add_users():
    repository = _create_user_repository(users=[])
    assert repository._users == set()

    user1 = model.User(username=TestData.username.test, email=TestData.email.user, password=TestData.password.password)
    repository.add(user=user1)
    assert repository._users == {user1}

    user2 = model.User(username=TestData.username.user, email=TestData.email.user2, password=TestData.password.password)
    repository.add(user=user2)
    assert repository._users == {user1, user2}


def test_get_user():
    session = fake_repositories.FakeSession()
    user1 = model.User(username=TestData.username.test, email=TestData.email.user, password=TestData.password.password)
    user2 = model.User(username=TestData.username.user, email=TestData.email.user2, password=TestData.password.password)
    repository = fake_repositories.FakeUserRepository(session=session, users=[user1, user2])
    assert repository._users == {user1, user2}

    # By username
    retrieved = repository.get(username=TestData.username.test)
    assert retrieved == user1

    retrieved = repository.get(username=TestData.username.bot)
    assert retrieved is None

    # By email
    retrieved = repository.get(email=TestData.email.user2)
    assert retrieved == user2

    retrieved = repository.get(email=TestData.email.bot)
    assert retrieved is None

    # By username & email
    retrieved = repository.get(username=TestData.username.test, email=TestData.email.user)
    assert retrieved == user1

    retrieved = repository.get(username=TestData.username.test, email=TestData.email.hello)
    assert retrieved is None

    retrieved = repository.get(username=TestData.username.bot, email=TestData.email.user)
    assert retrieved is None

    retrieved = repository.get(username=TestData.username.bot, email=TestData.email.bot)
    assert retrieved is None

    # By hello
    retrieved = repository.get(hello='world!')
    assert retrieved is None
