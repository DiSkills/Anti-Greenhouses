from uuid import uuid4

from src.auth.domain import model
from tests.conftest import TestData


def test_bad_logins_are_equal_by_uuid():
    uuid = f'{uuid4()}'
    first_bad_login = model.BadLogin(uuid=uuid)
    second_bad_login = model.BadLogin(uuid=uuid, ip_address=TestData.ip_address)

    assert first_bad_login == second_bad_login


def test_bad_logins_are_not_equal_by_uuid():
    first_bad_login = model.BadLogin(uuid=f'{uuid4()}')
    second_bad_login = model.BadLogin(uuid=f'{uuid4()}')

    assert (first_bad_login == second_bad_login) is False


def test_bad_login_is_not_equal_another_object():

    class AnotherObject:
        pass

    bad_login = model.BadLogin(uuid=f'{uuid4()}')
    another_object = AnotherObject()

    assert (bad_login == another_object) is False


def test_bad_login_the_represent_method():
    bad_login = model.BadLogin(uuid=f'{uuid4()}')

    assert bad_login.__repr__() == f'<BadLogin {bad_login.uuid}>'
    assert f'{bad_login}' == f'<BadLogin {bad_login.uuid}>'
