from typing import Optional

from src.auth.domain import model


class FakeVerificationRepository:

    def __init__(self, *, verifications: list[model.Verification]) -> None:
        self._verifications = set(verifications)

    def add(self, *, verification: model.Verification) -> None:
        self._verifications.add(verification)

    def _get(self, **filtration: str) -> Optional[model.Verification]:
        # Get by email and uuid
        if ('email' in filtration) and ('uuid' in filtration):
            return next(
                v for v in self._verifications if (v.email == filtration['email']) and (v.uuid == filtration['uuid'])
            )
        # Get by email
        elif 'email' in filtration:
            return next(v for v in self._verifications if v.email == filtration['email'])
        # Get by uuid
        elif 'uuid' in filtration:
            return next(v for v in self._verifications if v.uuid == filtration['uuid'])

        return None

    def get(self, **filtration: str) -> Optional[model.Verification]:
        try:
            return self._get(**filtration)
        except StopIteration:
            return None

    def remove(self, **filtration: str) -> None:
        verification = self.get(**filtration)

        if verification is not None:
            self._verifications.remove(verification)


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
