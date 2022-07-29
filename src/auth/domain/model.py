from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import config

pwd_context = config.get_pwd_context()


@dataclass
class BadLogin:

    uuid: str
    ip_address: Optional[str] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BadLogin):
            return False
        return self.uuid == other.uuid

    def __repr__(self) -> str:
        return f'<BadLogin {self.uuid}>'


@dataclass
class Verification:

    uuid: str
    email: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Verification):
            return False
        return self.uuid == other.uuid

    def __repr__(self) -> str:
        return f'<Verification {self.uuid}>'

    def __hash__(self) -> int:
        return hash(self.uuid)


@dataclass
class UserAction:

    uuid: str
    type: config.UserActionType
    created_at: datetime
    ip_address: Optional[str] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserAction):
            return False
        return self.uuid == other.uuid

    def __repr__(self) -> str:
        return f'<UserAction {self.uuid}>'

    def __hash__(self) -> int:
        return hash(self.uuid)


class User:

    def __init__(
        self,
        *,
        username: str,
        email: str,
        password: str,
        otp_secret: str = '',  # TODO add default
        otp: bool = False,
        is_superuser: bool = False,
        avatar: Optional[str] = None,
        date_joined: datetime = datetime.utcnow(),
    ) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar
        self.date_joined = date_joined

        self.otp = otp
        self.otp_secret = otp_secret

        self.is_superuser = is_superuser

        self._actions: set[UserAction] = set()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.username == other.username

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def __hash__(self) -> int:
        return hash(self.username)

    def add_action(self, *, action: UserAction) -> None:
        self._actions.add(action)

    def remove_action(self, *, action: UserAction) -> None:
        if action in self._actions:
            self._actions.remove(action)

    @property
    def count_actions(self) -> int:
        return len(self._actions)

    @property
    def actions(self) -> list[UserAction]:
        return list(self._actions)


def add_action(*, action: UserAction, user: User) -> None:
    user.add_action(action=action)


def remove_action(*, action: UserAction, user: User) -> None:
    user.remove_action(action=action)


def get_password_hash(*, password: str) -> str:
    return pwd_context.hash(password)


def check_password_hash(*, password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
