import abc
import typing

from sqlalchemy.orm import Session

from src.auth.domain import model


class AbstractVerificationRepository(abc.ABC):
    """ Abstract repository """

    @abc.abstractmethod
    def add(self, *, verification: model.Verification) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self, **filtration: str) -> typing.Optional[model.Verification]:
        raise NotImplementedError()

    @abc.abstractmethod
    def list(self) -> list[model.Verification]:
        raise NotImplementedError()


class VerificationRepository(AbstractVerificationRepository):
    """ Verification repository """

    def __init__(self, *, session: Session) -> None:
        self.session = session

    def add(self, *, verification: model.Verification) -> None:
        self.session.add(verification)

    def get(self, **filtration: str) -> typing.Optional[model.Verification]:
        return self.session.query(model.Verification).filter_by(**filtration).first()

    def list(self) -> list[model.Verification]:
        return self.session.query(model.Verification).all()
