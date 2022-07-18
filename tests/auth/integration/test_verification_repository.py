from uuid import uuid4

from src.auth.adapters.repositories.verification.repository import VerificationRepository
from src.auth.domain import model
from tests.conftest import TestData


def test_repository_can_save_a_verification(sqlite_session):
    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ()

    uuid = f'{uuid4()}'
    verification = model.Verification(email=TestData.email.user, uuid=uuid)

    repo = VerificationRepository(session=sqlite_session)
    repo.add(verification=verification)
    sqlite_session.commit()

    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ((TestData.email.user, uuid),)


def test_repository_can_retrieve_a_verification(sqlite_session):
    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'

    sqlite_session.execute(
        'INSERT INTO verifications (email, uuid) VALUES (:email1, :uuid1), (:email2, :uuid2)',
        {'email1': TestData.email.user, 'uuid1': uuid1, 'email2': TestData.email.python, 'uuid2': uuid2},
    )

    expected = model.Verification(email=TestData.email.python, uuid=uuid2)
    repo = VerificationRepository(session=sqlite_session)

    # Get by email
    retrieved = repo.get(email=TestData.email.python)
    assert expected == retrieved

    # Get by uuid
    retrieved = repo.get(uuid=uuid1)
    assert retrieved == model.Verification(email=TestData.email.user, uuid=uuid1)


def test_repository_can_not_retrieve_a_verification(sqlite_session):
    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'

    sqlite_session.execute(
        'INSERT INTO verifications (email, uuid) VALUES (:email1, :uuid1), (:email2, :uuid2)',
        {'email1': TestData.email.user, 'uuid1': uuid1, 'email2': TestData.email.python, 'uuid2': uuid2},
    )

    repo = VerificationRepository(session=sqlite_session)

    retrieved = repo.get(email=TestData.email.bot)
    assert retrieved is None


def test_repository_can_remove_verification_by_email(sqlite_session):
    uuid1, uuid2 = f'{uuid4()}', f'{uuid4()}'

    sqlite_session.execute(
        'INSERT INTO verifications (email, uuid) VALUES (:email1, :uuid1), (:email2, :uuid2)',
        {'email1': TestData.email.user, 'uuid1': uuid1, 'email2': TestData.email.python, 'uuid2': uuid2},
    )

    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ((TestData.email.user, uuid1), (TestData.email.python, uuid2))

    repo = VerificationRepository(session=sqlite_session)
    repo.remove(email=TestData.email.user)
    sqlite_session.commit()

    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ((TestData.email.python, uuid2),)


def test_repository_can_remove_verification_by_uuid(sqlite_session):
    uuid1 = f'{uuid4()}'
    uuid2 = f'{uuid4()}'

    sqlite_session.execute(
        'INSERT INTO verifications (email, uuid) VALUES (:email1, :uuid1), (:email2, :uuid2)',
        {'email1': TestData.email.user, 'uuid1': uuid1, 'email2': TestData.email.python, 'uuid2': uuid2},
    )

    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ((TestData.email.user, uuid1), (TestData.email.python, uuid2))

    repo = VerificationRepository(session=sqlite_session)
    repo.remove(uuid=uuid1)
    sqlite_session.commit()

    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ((TestData.email.python, uuid2),)
