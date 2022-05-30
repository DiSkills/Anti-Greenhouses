from dataclasses import dataclass


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
