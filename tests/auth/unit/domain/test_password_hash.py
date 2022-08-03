import config
from src.auth.security import get_password_hash, check_password_hash
from tests.conftest import TestData


def test_get_password_hash():
    password = TestData.password.strong
    hashed_password = get_password_hash(password=password)

    assert (password == hashed_password) is False

    assert config.get_pwd_context().verify(password, hashed_password) is True


def test_check_password_hash():
    password = TestData.password.strong
    hashed_password = config.get_pwd_context().hash(password)

    assert check_password_hash(password=password, hashed_password=hashed_password) is True

    hashed_password = get_password_hash(password=password)
    assert check_password_hash(password=password, hashed_password=hashed_password) is True

    assert check_password_hash(password=TestData.password.password, hashed_password=hashed_password) is False
