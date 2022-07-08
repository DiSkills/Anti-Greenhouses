import re
import string


class Password(str):

    @classmethod
    def validate(cls, password: str) -> str:
        punctuation = re.escape(string.punctuation)
        # TODO comment
        regular_expression = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[%s])[A-Za-z\d%s]{8,20}$' % (punctuation, punctuation),
        )

        if not regular_expression.fullmatch(password):
            raise ValueError('Invalid password.')
        return password
