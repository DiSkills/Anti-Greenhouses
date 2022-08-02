from uuid import uuid4

from src.auth.domain import model
from tests.auth import fake_repositories
from tests.conftest import TestData


def _create_user_repository(*, users: list[model.User]) -> fake_repositories.FakeUserRepository:
    return fake_repositories.FakeUserRepository(users=users)


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
    repository = fake_repositories.FakeUserRepository(users=[user1, user2])
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


def test_add_a_bad_login():
    repository = fake_repositories.FakeBadLoginRepository(bad_logins=[])
    assert repository._bad_logins == set()

    bad_login = model.BadLogin(uuid=f'{uuid4()}', ip_address=TestData.ip_address)
    repository.add(bad_login=bad_login)
    assert repository._bad_logins == {bad_login}


def test_add_bad_logins():
    repository = fake_repositories.FakeBadLoginRepository(bad_logins=[])
    assert repository._bad_logins == set()

    bad_login1 = model.BadLogin(uuid=f'{uuid4()}', ip_address=TestData.ip_address)
    repository.add(bad_login=bad_login1)
    assert repository._bad_logins == {bad_login1}

    bad_login2 = model.BadLogin(uuid=f'{uuid4()}')
    repository.add(bad_login=bad_login2)
    assert repository._bad_logins == {bad_login1, bad_login2}


def test_get_count_bad_logins_by_ip():
    repository = fake_repositories.FakeBadLoginRepository(bad_logins=[])
    assert repository.count() == 0
    assert repository.count(ip_address=TestData.ip_address) == 0
    assert repository.count(ip_address='bad-ip') == 0

    bad_login1 = model.BadLogin(uuid=f'{uuid4()}', ip_address=TestData.ip_address)
    bad_login2 = model.BadLogin(uuid=f'{uuid4()}', ip_address=TestData.ip_address)
    bad_login3 = model.BadLogin(uuid=f'{uuid4()}')

    for bad_login in bad_login1, bad_login2, bad_login3:
        repository.add(bad_login=bad_login)

    assert repository.count() == 1
    assert repository.count(ip_address=TestData.ip_address) == 2
    assert repository.count(ip_address='bad-ip') == 0


def test_remove_a_bad_login():
    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'
    uuid3 = f'{uuid4()}'

    bad_login1 = model.BadLogin(uuid=uuid1, ip_address=TestData.ip_address)
    bad_login2 = model.BadLogin(uuid=uuid2, ip_address=TestData.ip_address)
    bad_login3 = model.BadLogin(uuid=uuid3)

    repository = fake_repositories.FakeBadLoginRepository(bad_logins=[bad_login1, bad_login2, bad_login3])
    assert repository._bad_logins == {bad_login1, bad_login2, bad_login3}

    # By uuid
    repository.remove(uuid=uuid1)
    assert repository._bad_logins == {bad_login2, bad_login3}

    # Bad uuid
    repository.remove(uuid='bad-uuid')
    assert repository._bad_logins == {bad_login2, bad_login3}
