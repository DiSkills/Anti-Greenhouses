from typing import Optional

from src.auth.domain import model


class FakeUserRepository:

    def __init__(self, *, users: list[model.User]) -> None:
        self._users = set(users)

    def add(self, *, user: model.User) -> None:
        self._users.add(user)

    def _get(self, **filtration: str) -> Optional[model.User]:
        # Get by email and username
        if ('username' in filtration) and ('email' in filtration):
            return next(
                u for u in self._users if (u.username == filtration['username']) and (u.email == filtration['email'])
            )
        # Get by username
        elif 'username' in filtration:
            return next(u for u in self._users if u.username == filtration['username'])
        # Get by email
        elif 'email' in filtration:
            return next(u for u in self._users if u.email == filtration['email'])

        return None

    def get(self, **filtration: str) -> Optional[model.User]:
        try:
            return self._get(**filtration)
        except StopIteration:
            return None


class FakeBadLoginRepository:

    def __init__(self, *, bad_logins: list[model.BadLogin]) -> None:
        self._bad_logins = set(bad_logins)

    def add(self, *, bad_login: model.BadLogin) -> None:
        self._bad_logins.add(bad_login)

    def count(self, *, ip_address: Optional[str] = None) -> int:
        return len([bad_login for bad_login in self._bad_logins if bad_login.ip_address == ip_address])

    def remove(self, *, uuid: str) -> None:
        try:
            self._bad_logins.remove(next(bad_login for bad_login in self._bad_logins if bad_login.uuid == uuid))
        except StopIteration:
            return None
