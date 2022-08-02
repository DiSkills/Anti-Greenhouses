from uuid import uuid4

import pytest

from src.auth.domain import model
from src.base.services import services, exceptions
from tests.base.fake_uow import FakeUnitOfWork
from tests.conftest import TestData


def test_user_ip_is_not_blocked():
    # 1 bad_logins
    uow = FakeUnitOfWork()
    assert uow.committed is False

    uow.bad_logins.add(bad_login=model.BadLogin(uuid=f'{uuid4()}', ip_address=TestData.ip_address))

    services.bad_logins(ip=TestData.ip_address, uow=uow)
    assert uow.committed is True

    # 2 bad_logins
    uow = FakeUnitOfWork()
    assert uow.committed is False

    uow.bad_logins.add(bad_login=model.BadLogin(uuid=f'{uuid4()}', ip_address=TestData.ip_address))
    uow.bad_logins.add(bad_login=model.BadLogin(uuid=f'{uuid4()}', ip_address=TestData.ip_address))

    services.bad_logins(ip=TestData.ip_address, uow=uow)
    assert uow.committed is True


def test_user_ip_is_blocked():
    uow = FakeUnitOfWork()
    assert uow.committed is False

    # 3 bad_logins
    uow.bad_logins.add(bad_login=model.BadLogin(uuid=f'{uuid4()}', ip_address=TestData.ip_address))
    uow.bad_logins.add(bad_login=model.BadLogin(uuid=f'{uuid4()}', ip_address=TestData.ip_address))
    uow.bad_logins.add(bad_login=model.BadLogin(uuid=f'{uuid4()}', ip_address=TestData.ip_address))

    with pytest.raises(exceptions.ManyBadLogins, match='Many bad login attempts, your ip is temporarily blocked.'):
        services.bad_logins(ip=TestData.ip_address, uow=uow)

    assert uow.committed is False

    # 4 bad_logins
    uow.bad_logins.add(bad_login=model.BadLogin(uuid=f'{uuid4()}', ip_address=TestData.ip_address))

    with pytest.raises(exceptions.ManyBadLogins, match='Many bad login attempts, your ip is temporarily blocked.'):
        services.bad_logins(ip=TestData.ip_address, uow=uow)

    assert uow.committed is False

    # Doesn't block other ip
    services.bad_logins(ip='other-ip', uow=uow)
    assert uow.committed is True
