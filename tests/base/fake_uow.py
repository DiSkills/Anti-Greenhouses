from tests.auth.fake_repositories import FakeSession, FakeVerificationRepository, FakeUserRepository


class FakeUnitOfWork:

    def __init__(self) -> None:
        session = FakeSession()
        self.verifications = FakeVerificationRepository(session=session, verifications=[])
        self.users = FakeUserRepository(session=session, users=[])
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass
