from tests.auth.fake_repositories import FakeVerificationRepository, FakeUserRepository, FakeBadLoginRepository


class FakeUnitOfWork:

    def __init__(self) -> None:
        self.verifications = FakeVerificationRepository(verifications=[])
        self.users = FakeUserRepository(users=[])
        self.bad_logins = FakeBadLoginRepository(bad_logins=[])
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass
