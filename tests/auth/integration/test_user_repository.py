from sqlalchemy.orm import Session

from src.auth.adapters.repositories.user import UserRepository
from src.auth.domain import model


def _create_user(
    session: Session, username: str, email: str, password: str = 'hashed_password', otp_secret: str = 'otp_secret',
) -> None:
    user = model.User(username=username, email=email, password=password, otp_secret=otp_secret)
    session.add(user)
    session.commit()


def test_repository_can_save_a_user(sqlite_session):
    rows = tuple(
        sqlite_session.execute(
            'SELECT username, email, password, otp_secret, otp, is_superuser, avatar, date_joined FROM "users"',
        ),
    )
    assert rows == ()

    user = model.User(username='test', email='user@example.com', password='hashed_password', otp_secret='otp_secret')

    repo = UserRepository(session=sqlite_session)
    repo.add(user=user)
    sqlite_session.commit()

    rows = tuple(
        sqlite_session.execute(
            'SELECT username, email, password, otp_secret, otp, is_superuser, avatar, date_joined FROM "users"',
        ),
    )
    assert rows == (
        ('test', 'user@example.com', 'hashed_password', 'otp_secret', False, False, None, f'{user.date_joined}'),
    )


def test_repository_can_retrieve_a_user(sqlite_session):
    _create_user(session=sqlite_session, username='test', email='user@example.com')
    _create_user(session=sqlite_session, username='test2', email='user2@example.com')

    expected = model.User(
        username='test',
        email='user@example.com',
        password='hashed_password',
        otp_secret='otp_secret',
    )
    repo = UserRepository(session=sqlite_session)

    # Get by username
    retrieved = repo.get(username='test')
    assert retrieved == expected

    # Get by email
    retrieved = repo.get(email='user@example.com')
    assert retrieved == expected


def test_repository_can_not_retrieve_a_user(sqlite_session):
    _create_user(session=sqlite_session, username='test', email='user@example.com')
    _create_user(session=sqlite_session, username='test2', email='user2@example.com')

    repo = UserRepository(session=sqlite_session)

    retrieved = repo.get(email='bot@example.com')
    assert retrieved is None
