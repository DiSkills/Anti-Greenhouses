import config
from src.auth.domain.model import get_password_hash


def test_get_password_hash():
    password = 'Admin2248!'
    hashed_password = get_password_hash(password=password)

    assert (password == hashed_password) is False

    assert config.get_pwd_context().verify(password, hashed_password) is True
