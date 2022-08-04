import re
import string
from typing import Generator, Callable, Literal

from pydantic import BaseModel, EmailStr, validator


class Password(str):

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[str], str], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, password: str) -> str:
        punctuation = re.escape(string.punctuation)

        # True if the password contains at least 1 upper and lower case letter, number and punctuation
        regular_expression = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[%s])[A-Za-z\d%s]{8,20}$' % (punctuation, punctuation),
        )

        if not regular_expression.fullmatch(password):
            raise ValueError('Invalid password.')
        return password


class Registration(BaseModel):

    username: str
    uuid: str
    email: EmailStr
    password: Password
    confirm_password: str

    @validator('username')
    def validate_username(cls, username: str) -> str:
        # True if it contains at least 3 letters of the English alphabet
        # After can contain any number of letters, numbers and "_.-"
        if not re.fullmatch(r'[A-Za-z]{3,}[A-Za-z\d_.-]*', username):
            raise ValueError('Invalid username.')
        return username

    @validator('confirm_password')
    def validate_confirm_password(
        cls, confirm_password: str, values: dict[Literal['username', 'uuid', 'email', 'password'], str],
    ) -> str:
        password = values.get('password')
        if (password is not None) and (confirm_password != password):
            raise ValueError('Passwords do not match.')
        return confirm_password


class Login(BaseModel):

    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
