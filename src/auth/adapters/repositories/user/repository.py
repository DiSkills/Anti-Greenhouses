from typing import Optional

from sqlalchemy.orm import Session

from src.auth.domain import model


# TODO add filter, search, pagination...
class UserRepository:

    def __init__(self, *, session: Session) -> None:
        self.session = session

    def add(self, *, user: model.User) -> None:
        self.session.add(user)

    def get(self, **filtration: str) -> Optional[model.User]:
        return self.session.query(model.User).filter_by(**filtration).first()
