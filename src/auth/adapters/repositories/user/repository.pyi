from typing import overload, Optional

from sqlalchemy.orm import Session

from src.auth.domain import model


class UserRepository:

    session: Session

    def __init__(self, *, session: Session) -> None: ...

    def add(self, *, user: model.User) -> None: ...

    @overload
    def get(self, *, username: str, email: str) -> Optional[model.User]: ...

    @overload
    def get(self, *, username: str) -> Optional[model.User]: ...

    @overload
    def get(self, *, email: str) -> Optional[model.User]: ...
