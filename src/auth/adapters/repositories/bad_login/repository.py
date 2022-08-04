from typing import Optional

from pymongo.collection import Collection

from src.auth.domain import model


class BadLoginRepository:

    def __init__(self, *, collection: Collection) -> None:
        self.collection = collection

    def add(self, *, bad_login: model.BadLogin) -> None:
        self.collection.insert_one(bad_login.dict())

    def count(self, *, ip_address: Optional[str] = None) -> int:
        return self.collection.count_documents({'ip_address': ip_address})

    def remove(self, *, uuid: str) -> None:
        self.collection.delete_one({'uuid': uuid})
