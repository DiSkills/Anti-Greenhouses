from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

import jwt

import config
from config import Seconds, JWTConfig


@dataclass
class LoginTokens:
    access: str
    refresh: str


def create_token(*, data: dict[str, Any], expires_delta: Seconds = JWTConfig.default) -> str:
    encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    encode.update({'exp': expire})
    return jwt.encode(encode, config.get_app_settings().secret_key, algorithm=JWTConfig.algorithms[0])


def create_access_token(*, user_id: int, uuid: str, is_superuser: bool = False) -> str:
    data = {
        'user_id': user_id,
        'uuid': uuid,
        'is_superuser': is_superuser,
        'subject': JWTConfig.access_subject,
    }
    return create_token(data=data, expires_delta=JWTConfig.access)


def create_login_tokens(*, user_id: int, uuid: str, is_superuser: bool = False) -> LoginTokens:
    access_token = create_access_token(user_id=user_id, uuid=uuid, is_superuser=is_superuser)

    data = {
        'user_id': user_id,
        'uuid': uuid,
        'is_superuser': is_superuser,
        'subject': JWTConfig.refresh_subject,
    }
    refresh_token = create_token(data=data, expires_delta=JWTConfig.refresh)
    return LoginTokens(access=access_token, refresh=refresh_token)
