from uuid import uuid4

import pytest

from src.auth.domain import model
from src.base.uow import UnitOfWork
from tests.conftest import TestData


def test_uow_can_save_a_verification(in_memory_db):
    uuid = f'{uuid4()}'

    uow = UnitOfWork(session_factory=in_memory_db)
    with uow:
        verification = model.Verification(email=TestData.email.user, uuid=uuid)
        uow.verifications.add(verification=verification)
        uow.commit()

    with in_memory_db() as sqlite_session:
        rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
        assert rows == ((TestData.email.user, uuid),)


def test_rolls_back_uncommitted_work_by_default(in_memory_db):
    uuid = f'{uuid4()}'

    uow = UnitOfWork(session_factory=in_memory_db)
    with uow:
        verification = model.Verification(email=TestData.email.user, uuid=uuid)
        uow.verifications.add(verification=verification)

    with in_memory_db() as sqlite_session:
        rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
        assert rows == ()


def test_rolls_back_on_error(in_memory_db):
    uuid = f'{uuid4()}'

    uow = UnitOfWork(session_factory=in_memory_db)
    with pytest.raises(Exception):
        with uow:
            verification = model.Verification(email=TestData.email.user, uuid=uuid)
            uow.verifications.add(verification=verification)
            raise Exception()

    with in_memory_db() as sqlite_session:
        rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
        assert rows == ()
