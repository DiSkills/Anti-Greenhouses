from sqlalchemy.orm import Session

import config
from src.auth.adapters.repositories.user.repository import UserRepository
from src.auth.adapters.repositories.verification.repository import VerificationRepository


class UnitOfWork:

    verifications: VerificationRepository
    users: UserRepository
    session: Session

    def __init__(self, *, session_factory = config.get_session) -> None:
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.verifications = VerificationRepository(session=self.session)
        self.users = UserRepository(session=self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
