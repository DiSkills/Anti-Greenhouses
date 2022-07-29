from uuid import uuid4

from src.auth.adapters.repositories.bad_login.repository import BadLoginRepository
from src.auth.domain import model
from tests.conftest import TestData


def test_repository_can_save_a_bad_login(mongo_bad_logins):
    rows = tuple(mongo_bad_logins.find({}, {'_id': False}))
    assert rows == ()

    uuid = f'{uuid4()}'
    bad_login = model.BadLogin(uuid=uuid)

    repo = BadLoginRepository(collection=mongo_bad_logins)
    repo.add(bad_login=bad_login)

    rows = tuple(mongo_bad_logins.find({}, {'_id': False}))
    assert rows == ({'uuid': uuid, 'ip_address': None},)


def test_repository_can_retrieve_count_bad_logins_by_ip(mongo_bad_logins):
    repo = BadLoginRepository(collection=mongo_bad_logins)

    count = repo.count(ip_address=TestData.ip_address)
    assert count == 0

    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'
    uuid3 = f'{uuid4()}'

    mongo_bad_logins.insert_many(
        [
            {'uuid': uuid1, 'ip_address': TestData.ip_address},
            {'uuid': uuid2, 'ip_address': TestData.ip_address},
            {'uuid': uuid3},
        ],
    )

    count = repo.count(ip_address=TestData.ip_address)
    assert count == 2

    count = repo.count()
    assert count == 1

    count = repo.count(ip_address='bad-ip')
    assert count == 0


def test_repository_can_remove_bad_login(mongo_bad_logins):
    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'

    mongo_bad_logins.insert_many(
        [
            {'uuid': uuid1, 'ip_address': TestData.ip_address},
            {'uuid': uuid2, 'ip_address': TestData.ip_address},
        ],
    )

    rows = tuple(mongo_bad_logins.find({}, {'_id': False}))
    assert rows == (
        {'uuid': uuid1, 'ip_address': TestData.ip_address}, {'uuid': uuid2, 'ip_address': TestData.ip_address},
    )

    repo = BadLoginRepository(collection=mongo_bad_logins)
    repo.remove(uuid=uuid1)

    rows = tuple(mongo_bad_logins.find({}, {'_id': False}))
    assert rows == ({'uuid': uuid2, 'ip_address': TestData.ip_address},)
