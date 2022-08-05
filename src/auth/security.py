import config

pwd_context = config.get_pwd_context()


def get_password_hash(*, password: str) -> str:
    return pwd_context.hash(password)


def check_password_hash(*, password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
