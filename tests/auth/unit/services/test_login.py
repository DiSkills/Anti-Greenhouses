import jwt
import pytest

import config
from src.auth.domain import model
from src.auth.exceptions import InvalidUsernameOrPassword
from src.auth.services.services import login
from tests.base.fake_uow import FakeUnitOfWork
from tests.conftest import TestData


def test_login_by_username_create_tokens(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False
    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 0

    password = model.get_password_hash(password=TestData.password.password)
    uow.users.add(user=model.User(username=TestData.username.user, email=TestData.email.user, password=password))

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 0

    tokens = login(username=TestData.username.user, password=TestData.password.password, uow=uow)

    # Access
    decoded = jwt.decode(tokens.access, config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.user,
        'is_superuser': False,
        'uuid': user.uuid,
        'subject': config.JWTConfig.access_subject,
        'exp': decoded.get('exp'),
    }

    # Refresh
    decoded = jwt.decode(tokens.refresh, config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.user,
        'is_superuser': False,
        'uuid': user.uuid,
        'subject': config.JWTConfig.refresh_subject,
        'exp': decoded.get('exp'),
    }

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 1
    assert user.actions[0].type == config.UserActionType.login

    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 0
    assert uow.committed is True


def test_login_by_email_create_tokens(mocker):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False
    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 0

    password = model.get_password_hash(password=TestData.password.password)
    uow.users.add(user=model.User(username=TestData.username.user, email=TestData.email.user, password=password))

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 0

    tokens = login(username=TestData.email.user, password=TestData.password.password, uow=uow)

    # Access
    decoded = jwt.decode(tokens.access, config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.user,
        'is_superuser': False,
        'uuid': user.uuid,
        'subject': config.JWTConfig.access_subject,
        'exp': decoded.get('exp'),
    }

    # Refresh
    decoded = jwt.decode(tokens.refresh, config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.user,
        'is_superuser': False,
        'uuid': user.uuid,
        'subject': config.JWTConfig.refresh_subject,
        'exp': decoded.get('exp'),
    }

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 1
    assert user.actions[0].type == config.UserActionType.login

    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 0
    assert uow.committed is True


def test_login_invalid_username():
    uow = FakeUnitOfWork()
    assert uow.committed is False

    # Username
    with pytest.raises(InvalidUsernameOrPassword, match='Invalid username or password.'):
        login(username=TestData.username.bot, password=TestData.password.password, uow=uow)
    assert uow.committed is False

    # Email
    with pytest.raises(InvalidUsernameOrPassword, match='Invalid username or password.'):
        login(username=TestData.email.user, password=TestData.password.password, uow=uow)
    assert uow.committed is False


def test_login_invalid_password(mocker):
    mocker.patch('worker.remove_bad_login', return_value=None)
    mocker.patch('worker.remove_bad_login_task', return_value=None)

    uow = FakeUnitOfWork()
    assert uow.committed is False
    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 0

    password = model.get_password_hash(password=TestData.password.strong)
    uow.users.add(user=model.User(username=TestData.username.user, email=TestData.email.user, password=password))

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 0

    with pytest.raises(InvalidUsernameOrPassword, match='Invalid username or password.'):
        login(
            username=TestData.email.user, password=TestData.password.password, ip_address=TestData.ip_address, uow=uow,
        )

    user = uow.users.get(username=TestData.username.user)
    assert user is not None
    assert user.count_actions == 0

    assert uow.bad_logins.count(ip_address=TestData.ip_address) == 1
    assert uow.committed is True
