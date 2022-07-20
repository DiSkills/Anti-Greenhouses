from typing import Optional, overload

from pymongo.collection import Collection

from src.auth.domain import model


class VerificationRepository:
    collection: Collection

    def __init__(self, *, collection: Collection) -> None: ...

    def add(self, *, verification: model.Verification) -> None: ...

    @overload
    def get(self, *, email: str, uuid: str) -> Optional[model.Verification]: ...

    @overload
    def get(self, *, uuid: str) -> Optional[model.Verification]: ...

    @overload
    def get(self, *, email: str) -> Optional[model.Verification]: ...

    @overload
    def remove(self, *, email: str, uuid: str) -> None: ...

    @overload
    def remove(self, *, uuid: str) -> None: ...

    @overload
    def remove(self, *, email: str) -> None: ...
