import uuid

from src.auth.adapters.repositories import verification as repository
from src.auth.domain import model


def test_repository_can_save_a_verification(sqlite_session):
    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ()

    _uuid = f'{uuid.uuid4()}'
    verification = model.Verification(email='user@example.com', uuid=_uuid)

    repo = repository.VerificationRepository(session=sqlite_session)
    repo.add(verification=verification)
    sqlite_session.commit()

    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == (('user@example.com', _uuid),)


def test_repository_can_retrieve_a_verification(sqlite_session):
    uuid1 = f'{uuid.uuid4()}'
    uuid2 = f'{uuid.uuid4()}'

    sqlite_session.execute(
        'INSERT INTO verifications (email, uuid) VALUES (:email1, :uuid1), (:email2, :uuid2)',
        {'email1': 'user@example.com', 'uuid1': uuid1, 'email2': 'python@example.com', 'uuid2': uuid2},
    )

    expected = model.Verification(email='python@example.com', uuid=uuid2)
    repo = repository.VerificationRepository(session=sqlite_session)

    # Get by email
    retrieved = repo.get(email='python@example.com')
    assert expected == retrieved

    # Get by uuid
    retrieved = repo.get(uuid=uuid1)
    assert retrieved == model.Verification(email='user@example.com', uuid=uuid1)


def test_repository_can_not_retrieve_a_verification(sqlite_session):
    uuid1 = f'{uuid.uuid4()}'
    uuid2 = f'{uuid.uuid4()}'

    sqlite_session.execute(
        'INSERT INTO verifications (email, uuid) VALUES (:email1, :uuid1), (:email2, :uuid2)',
        {'email1': 'user@example.com', 'uuid1': uuid1, 'email2': 'python@example.com', 'uuid2': uuid2},
    )

    repo = repository.VerificationRepository(session=sqlite_session)

    retrieved = repo.get(email='bot@example.com')
    assert retrieved is None


def test_repository_can_remove_verification_by_email(sqlite_session):
    uuid1 = f'{uuid.uuid4()}'
    uuid2 = f'{uuid.uuid4()}'

    sqlite_session.execute(
        'INSERT INTO verifications (email, uuid) VALUES (:email1, :uuid1), (:email2, :uuid2)',
        {'email1': 'user@example.com', 'uuid1': uuid1, 'email2': 'python@example.com', 'uuid2': uuid2},
    )

    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == (('user@example.com', uuid1), ('python@example.com', uuid2))

    repo = repository.VerificationRepository(session=sqlite_session)
    repo.remove(email='user@example.com')
    sqlite_session.commit()

    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == (('python@example.com', uuid2),)


def test_repository_can_remove_verification_by_uuid(sqlite_session):
    uuid1 = f'{uuid.uuid4()}'
    uuid2 = f'{uuid.uuid4()}'

    sqlite_session.execute(
        'INSERT INTO verifications (email, uuid) VALUES (:email1, :uuid1), (:email2, :uuid2)',
        {'email1': 'user@example.com', 'uuid1': uuid1, 'email2': 'python@example.com', 'uuid2': uuid2},
    )

    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == (('user@example.com', uuid1), ('python@example.com', uuid2))

    repo = repository.VerificationRepository(session=sqlite_session)
    repo.remove(uuid=uuid1)
    sqlite_session.commit()
    
    rows = tuple(sqlite_session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == (('python@example.com', uuid2),)
