import typing

from src.auth.domain import model


class FakeSession:

    committed = False

    def commit(self) -> None:
        self.committed = True


class FakeVerificationRepository:

    def __init__(self, *, session: FakeSession, verifications: list[model.Verification]) -> None:
        self._verifications = set(verifications)
        self.session = session

    def add(self, *, verification: model.Verification) -> None:
        self._verifications.add(verification)

    def _get(self, **filtration: str) -> typing.Optional[model.Verification]:
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

    def get(self, **filtration: str) -> typing.Optional[model.Verification]:
        try:
            return self._get(**filtration)
        except StopIteration:
            return None

    def remove(self, **filtration: str) -> None:
        verification = self.get(**filtration)

        if verification is not None:
            self._verifications.remove(verification)


class FakeUserRepository:

    def __init__(self, *, session: FakeSession, users: list[model.User]) -> None:
        self._users = set(users)
        self.session = session

    def add(self, *, user: model.User) -> None:
        self._users.add(user)

    def _get(self, **filtration: str) -> typing.Optional[model.User]:
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

    def get(self, **filtration: str) -> typing.Optional[model.User]:
        try:
            return self._get(**filtration)
        except StopIteration:
            return None
