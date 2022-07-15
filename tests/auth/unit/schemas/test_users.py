import string
import typing

import pytest
from pydantic import EmailStr

from src.auth.entrypoints.schemas.users import Password, Registration


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
        assert Password.validate(password=f'Admin2248{char}') == f'Admin2248{char}'


def test_password_can_get_validators():
    generator = Password.__get_validators__()
    assert isinstance(generator, typing.Generator)

    validators = list(generator)
    assert validators == [Password.validate]


def test_confirm_password_equals_password():
    Registration(
        username='test',
        uuid='uuid',
        email=EmailStr('user@example.com'),
        password=Password('Admin2248!'),
        confirm_password='Admin2248!',
    )


def test_confirm_password_not_equals_password():
    with pytest.raises(ValueError, match='Invalid confirm password.'):
        Registration(
            username='test',
            uuid='uuid',
            email=EmailStr('user@example.com'),
            password=Password('Admin2248!'),
            confirm_password='Admin',
        )


def test_username_consists_only_of_the_english_alphabet():
    with pytest.raises(ValueError, match='Invalid username.'):
        Registration(
            username='ююююю',
            uuid='uuid',
            email=EmailStr('user@example.com'),
            password=Password('Admin2248!'),
            confirm_password='Admin2248!',
        )


def test_username_less_than_3_characters():
    with pytest.raises(ValueError, match='Invalid username.'):
        Registration(
            username='te',
            uuid='uuid',
            email=EmailStr('user@example.com'),
            password=Password('Admin2248!'),
            confirm_password='Admin2248!',
        )
