import string

import pytest

from src.auth.entrypoints.schemas.users import Password


def test_password_characters_less_than_8():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='pass')


def test_password_characters_length_is_more_than_20():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='pass' * 6)


def test_passwords_does_not_have_capital_letters():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='passwordddd')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='passwordddd12')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='passwordddd12!')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='passwordddd!')


def test_passwords_does_not_have_lower_letters():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDDDD')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDDDD12')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDDDD12!')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDDDD!')


def test_passwords_does_not_have_digits():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='passwordddd')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='passwordddd!')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDDDD')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDDDD!')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDdd')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDdd!')


def test_passwords_does_not_have_punctuations():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='passwordddd')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='passwordddd12')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDDDD')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDDDD12')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDDdd')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate_password(password='PASSWORDDDdd12')


def test_passwords_has_been_validated():
    password = 'Admin2248!'
    assert Password.validate_password(password=password) == password

    for char in string.punctuation:
        assert Password.validate_password(password=f'Admin2248{char}')
