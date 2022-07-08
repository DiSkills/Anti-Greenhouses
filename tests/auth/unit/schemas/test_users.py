import string

import pytest

from src.auth.entrypoints.schemas.users import Password


def test_password_characters_less_than_8():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='pass')


def test_password_characters_length_is_more_than_20():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='pass' * 6)


def test_passwords_does_not_have_capital_letters():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='passwordddd')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='passwordddd12')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='passwordddd12!')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='passwordddd!')


def test_passwords_does_not_have_lower_letters():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDDDD')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDDDD12')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDDDD12!')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDDDD!')


def test_passwords_does_not_have_digits():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='passwordddd')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='passwordddd!')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDDDD')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDDDD!')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDdd')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDdd!')


def test_passwords_does_not_have_punctuations():
    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='passwordddd')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='passwordddd12')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDDDD')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDDDD12')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDDdd')

    with pytest.raises(ValueError, match='Invalid password.'):
        Password.validate(password='PASSWORDDDdd12')


def test_passwords_has_been_validated():
    password = 'Admin2248!'
    assert Password.validate(password=password) == password

    for char in string.punctuation:
        assert Password.validate(password=f'Admin2248{char}')
