import re
import string
from typing import Generator, Callable


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
