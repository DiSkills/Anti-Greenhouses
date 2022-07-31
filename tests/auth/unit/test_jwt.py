from uuid import uuid4

import jwt

import config
from config import JWTConfig
from src.auth.services.jwt import create_token, create_access_token


def test_create_token():
    uuid = f'{uuid4()}'

    access_token = create_token(
        data={'user_id': 1, 'is_superuser': False, 'uuid': uuid, 'subject': JWTConfig.access_subject},
        expires_delta=JWTConfig.access,
    )
    decoded = jwt.decode(access_token, config.get_app_settings().secret_key, algorithms=JWTConfig.algorithms)
    assert decoded == {
        'user_id': 1,
        'is_superuser': False,
        'uuid': uuid,
        'subject': JWTConfig.access_subject,
        'exp': decoded.get('exp'),
    }


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
