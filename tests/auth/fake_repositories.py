from typing import Optional

from src.auth.domain import model


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
