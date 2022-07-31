from uuid import uuid4

import jwt

import config
from config import JWTConfig
from src.auth.services.jwt import create_token, create_access_token, create_login_tokens


def test_create_token():
    uuid = f'{uuid4()}'

    data = {'user_id': 1, 'is_superuser': False, 'uuid': uuid, 'subject': JWTConfig.access_subject}
    access_token = create_token(data=data, expires_delta=JWTConfig.access)
    decoded = jwt.decode(access_token, config.get_app_settings().secret_key, algorithms=JWTConfig.algorithms)
    assert decoded == {
        'user_id': 1,
        'is_superuser': False,
        'uuid': uuid,
        'subject': JWTConfig.access_subject,
        'exp': decoded.get('exp'),
    }
    assert data == {'user_id': 1, 'is_superuser': False, 'uuid': uuid, 'subject': JWTConfig.access_subject}


def test_create_access_token():
    uuid = f'{uuid4()}'

    token = create_access_token(user_id=1, uuid=uuid, is_superuser=False)
    decoded = jwt.decode(token, config.get_app_settings().secret_key, algorithms=JWTConfig.algorithms)
    assert decoded == {
        'user_id': 1,
        'is_superuser': False,
        'uuid': uuid,
        'subject': JWTConfig.access_subject,
        'exp': decoded.get('exp'),
    }


def test_create_login_tokens():
    uuid = f'{uuid4()}'
    secret_key = config.get_app_settings().secret_key

    tokens = create_login_tokens(user_id=1, uuid=uuid, is_superuser=False)

    # Access
    decoded = jwt.decode(tokens.access, secret_key, algorithms=JWTConfig.algorithms)
    access_expires = decoded['exp']
    assert decoded == {
        'user_id': 1,
        'is_superuser': False,
        'uuid': uuid,
        'subject': JWTConfig.access_subject,
        'exp': access_expires,
    }

    # Refresh
    decoded = jwt.decode(tokens.refresh, secret_key, algorithms=JWTConfig.algorithms)
    refresh_expires = decoded['exp']
    assert decoded == {
        'user_id': 1,
        'is_superuser': False,
        'uuid': uuid,
        'subject': JWTConfig.refresh_subject,
        'exp': refresh_expires,
    }

    assert refresh_expires > access_expires
