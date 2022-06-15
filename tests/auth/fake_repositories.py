import typing

from src.auth.domain import model


class FakeSession:
    committed = False

    def commit(self) -> None:
        self.committed = True


class FakeVerificationRepository:
    """ Fake verification repository """

    def __init__(self, *, session: FakeSession, verifications: list[model.Verification]):
        self._verifications = set(verifications)
        self.session = session

    def add(self, *, verification: model.Verification) -> None:
        self._verifications.add(verification)

    def _get(self, **filtration: str) -> typing.Optional[model.Verification]:
        if ('email' in filtration) and ('uuid' in filtration):
            return next(
                v for v in self._verifications if (v.email == filtration['email']) and (v.uuid == filtration['uuid'])
            )

        elif 'email' in filtration:
            return next(v for v in self._verifications if v.email == filtration['email'])

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
