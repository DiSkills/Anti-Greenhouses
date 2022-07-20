from typing import Optional

from pymongo.collection import Collection

from src.auth.domain import model


class VerificationRepository:

    def __init__(self, *, collection: Collection) -> None:
        self.collection = collection

    def add(self, *, verification: model.Verification) -> None:
        data = {
            'email': verification.email,
            'uuid': verification.uuid,
        }
        self.collection.insert_one(data)

    def get(self, **filtration: str) -> Optional[model.Verification]:
        data = self.collection.find_one(filtration)
        if data is not None:
            data = model.Verification(uuid=data['uuid'], email=data['email'])
        return data

    def remove(self, **filtration: str) -> None:
        self.collection.delete_one(filtration)
