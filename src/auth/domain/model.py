from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import config


@dataclass
class Verification:
    """ Verification """

    email: str
    uuid: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Verification):
            return False
        return self.uuid == other.uuid

    def __repr__(self) -> str:
        return f'<Verification {self.uuid}>'

    def __hash__(self) -> int:
        return hash(self.uuid)


@dataclass
class UserAction:
    """ User action """

    uuid: str
    type: config.UserActionType
    created_at: datetime
    ip_address: Optional[str] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserAction):
            return False
        return self.uuid == other.uuid

    def __repr__(self) -> str:
        return f'<UserAction {self.uuid}>'

    def __hash__(self) -> int:
        return hash(self.uuid)
