from sqlalchemy.orm import Session

import config
from src.auth.adapters.repositories.bad_login.repository import BadLoginRepository
from src.auth.adapters.repositories.user.repository import UserRepository
from src.auth.adapters.repositories.verification.repository import VerificationRepository


class UnitOfWork:

    verifications: VerificationRepository
    users: UserRepository
    bad_logins: BadLoginRepository
    session: Session

    def __init__(self, *, session_factory = config.get_session, mongo_client = config.mongo_client) -> None:
        self.session_factory = session_factory
        self.mongo_session = mongo_client[config.mongo_config.name]

    def __enter__(self):
        self.session = self.session_factory()
        self.verifications = VerificationRepository(
            collection=self.mongo_session[config.MongoTables.verifications.name],
        )
        self.users = UserRepository(session=self.session)
        self.bad_logins = BadLoginRepository(collection=self.mongo_session[config.MongoTables.bad_logins.name])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
