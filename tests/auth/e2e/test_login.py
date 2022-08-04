import jwt
from fastapi import status

import config
from main import app
from src.auth.security import get_password_hash
from tests.auth.e2e._user import _create_user
from tests.conftest import TestData


def test_login_by_username_return_200_and_create_tokens(mocker, e2e):
    mongo_bad_logins = e2e.mongo[config.MongoTables.bad_logins.name]
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    _create_user(e2e=e2e, password=get_password_hash(password=TestData.password.strong))
    rows = tuple(e2e.session.execute('SELECT username FROM "users"'))
    assert rows == ((TestData.username.test,),)

    rows = tuple(e2e.session.execute('SELECT * FROM "actions"'))
    assert rows == ()
    rows = tuple(mongo_bad_logins.find({}, {'_id': False}))
    assert rows == ()

    response = e2e.client.post(
        f'{app.url_path_for("login")}', data={'username': TestData.username.test, 'password': TestData.password.strong},
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert 'access_token' in json
    assert 'refresh_token' in json
    assert json['token_type'] == 'bearer'

    # Access
    decoded = jwt.decode(json['access_token'], config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.test,
        'is_superuser': False,
        'uuid': decoded.get('uuid'),
        'subject': config.JWTConfig.access_subject,
        'exp': decoded.get('exp'),
    }

    # Refresh
    decoded = jwt.decode(json['refresh_token'], config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.test,
        'is_superuser': False,
        'uuid': decoded.get('uuid'),
        'subject': config.JWTConfig.refresh_subject,
        'exp': decoded.get('exp'),
    }

    # Check actions
    rows = tuple(e2e.session.execute('SELECT id, user_id, action_id FROM "user_actions"'))
    assert rows == ((1, 1, 1),)
    rows = tuple(e2e.session.execute('SELECT type, ip_address FROM "actions"'))
    assert rows == (('login', None),)
    rows = tuple(mongo_bad_logins.find({}, {'_id': False}))
    assert rows == ()


def test_login_by_email_return_200_and_create_tokens(mocker, e2e):
    mongo_bad_logins = e2e.mongo[config.MongoTables.bad_logins.name]
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    _create_user(e2e=e2e, password=get_password_hash(password=TestData.password.strong))
    rows = tuple(e2e.session.execute('SELECT username FROM "users"'))
    assert rows == ((TestData.username.test,),)

    rows = tuple(e2e.session.execute('SELECT * FROM "actions"'))
    assert rows == ()
    rows = tuple(mongo_bad_logins.find({}, {'_id': False}))
    assert rows == ()

    response = e2e.client.post(
        f'{app.url_path_for("login")}', data={'username': TestData.email.user, 'password': TestData.password.strong},
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert 'access_token' in json
    assert 'refresh_token' in json
    assert json['token_type'] == 'bearer'

    # Access
    decoded = jwt.decode(json['access_token'], config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.test,
        'is_superuser': False,
        'uuid': decoded.get('uuid'),
        'subject': config.JWTConfig.access_subject,
        'exp': decoded.get('exp'),
    }

    # Refresh
    decoded = jwt.decode(json['refresh_token'], config.get_app_settings().secret_key, config.JWTConfig.algorithms)
    assert decoded == {
        'username': TestData.username.test,
        'is_superuser': False,
        'uuid': decoded.get('uuid'),
        'subject': config.JWTConfig.refresh_subject,
        'exp': decoded.get('exp'),
    }

    # Check actions
    rows = tuple(e2e.session.execute('SELECT id, user_id, action_id FROM "user_actions"'))
    assert rows == ((1, 1, 1),)
    rows = tuple(e2e.session.execute('SELECT type, ip_address FROM "actions"'))
    assert rows == (('login', None),)
    rows = tuple(mongo_bad_logins.find({}, {'_id': False}))
    assert rows == ()


def test_login_return_400_when_user_with_this_username_not_found(e2e):
    # Username
    response = e2e.client.post(
        f'{app.url_path_for("login")}', data={'username': TestData.username.test, 'password': TestData.password.strong},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Invalid username or password.'}

    # Email
    response = e2e.client.post(
        f'{app.url_path_for("login")}', data={'username': TestData.email.user, 'password': TestData.password.strong},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Invalid username or password.'}


def test_login_return_400_when_invalid_password(mocker, e2e):
    mocker.patch('worker.remove_bad_login', return_value=None)
    mocker.patch('worker.remove_bad_login_task', return_value=None)
    mongo_bad_logins = e2e.mongo[config.MongoTables.bad_logins.name]

    _create_user(e2e=e2e, password=get_password_hash(password=TestData.password.strong))
    rows = tuple(e2e.session.execute('SELECT username FROM "users"'))
    assert rows == ((TestData.username.test,),)

    rows = tuple(e2e.session.execute('SELECT * FROM "actions"'))
    assert rows == ()
    rows = tuple(mongo_bad_logins.find({}, {'_id': False}))
    assert rows == ()

    response = e2e.client.post(
        f'{app.url_path_for("login")}',
        data={'username': TestData.email.user, 'password': 'bad-password'},
        headers={'x-forwarded-for': TestData.ip_address},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Invalid username or password.'}

    rows = tuple(e2e.session.execute('SELECT * FROM "actions"'))
    assert rows == ()
    rows = tuple(mongo_bad_logins.find({}, {'_id': False, 'uuid': False}))
    assert rows == ({'ip_address': TestData.ip_address},)
