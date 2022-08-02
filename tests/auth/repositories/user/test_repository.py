from src.auth.domain import model
from tests.auth.repositories.user.repository import FakeUserRepository
from tests.conftest import TestData


def _create_user_repository(*, users: list[model.User]) -> FakeUserRepository:
    return FakeUserRepository(users=users)


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
    user1 = model.User(username=TestData.username.test, email=TestData.email.user, password=TestData.password.password)
    user2 = model.User(username=TestData.username.user, email=TestData.email.user2, password=TestData.password.password)
    repository = FakeUserRepository(users=[user1, user2])
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
