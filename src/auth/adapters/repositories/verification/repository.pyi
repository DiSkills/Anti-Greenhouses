import typing

from sqlalchemy.orm import Session

from src.auth.domain import model


class VerificationRepository:

    session: Session

    def __init__(self, *, session: Session) -> None: ...

    def add(self, *, verification: model.Verification) -> None: ...

    @typing.overload
    def get(self, *, email: str, uuid: str) -> typing.Optional[model.Verification]: ...

    @typing.overload
    def get(self, *, uuid: str) -> typing.Optional[model.Verification]: ...

    @typing.overload
    def get(self, *, email: str) -> typing.Optional[model.Verification]: ...

    @typing.overload
    def remove(self, *, email: str, uuid: str) -> None: ...

    @typing.overload
    def remove(self, *, uuid: str) -> None: ...

    @typing.overload
    def remove(self, *, email: str) -> None: ...
