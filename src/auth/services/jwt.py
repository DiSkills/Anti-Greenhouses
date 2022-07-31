from datetime import datetime, timedelta
from typing import Any

import jwt

import config
from config import Seconds, JWTConfig


def create_token(*, data: dict[str, Any], expires_delta: Seconds = JWTConfig.default) -> str:
    encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    encode.update({'exp': expire})
    return jwt.encode(encode, config.get_app_settings().secret_key, algorithm=JWTConfig.algorithms[0])
