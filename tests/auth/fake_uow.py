from tests.auth.fake_repositories import FakeSession, FakeVerificationRepository


class FakeVerificationUnitOfWork:
    verifications: FakeVerificationRepository

    def __init__(self) -> None:
        self.verifications = FakeVerificationRepository(session=FakeSession(), verifications=[])
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass
