import pytest

from src.auth.domain import model
from src.base.uow import UnitOfWork
from tests.conftest import TestData


def test_uow_can_save_a_user(in_memory_db):
    uow = UnitOfWork(session_factory=in_memory_db)
    with uow:
        user = model.User(username=TestData.username.test, email=TestData.email.user, password='hashed_password')
        uow.users.add(user=user)
        uow.commit()

    with in_memory_db() as sqlite_session:
        rows = tuple(sqlite_session.execute('SELECT username FROM "users"'))
        assert rows == ((TestData.username.test,),)


def test_rolls_back_uncommitted_work_by_default(in_memory_db):
    uow = UnitOfWork(session_factory=in_memory_db)
    with uow:
        user = model.User(username=TestData.username.test, email=TestData.email.user, password='hashed_password')
        uow.users.add(user=user)

    with in_memory_db() as sqlite_session:
        rows = tuple(sqlite_session.execute('SELECT username FROM "users"'))
        assert rows == ()


def test_rolls_back_on_error(in_memory_db):
    uow = UnitOfWork(session_factory=in_memory_db)
    with pytest.raises(Exception):
        with uow:
            user = model.User(username=TestData.username.test, email=TestData.email.user, password='hashed_password')
            uow.users.add(user=user)
            raise Exception()

    with in_memory_db() as sqlite_session:
        rows = tuple(sqlite_session.execute('SELECT username FROM "users"'))
        assert rows == ()
