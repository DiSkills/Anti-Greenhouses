from sqlalchemy.orm import Session

from src.auth.adapters.repositories.user.repository import UserRepository
from src.auth.domain import model
from tests.conftest import TestData


def _create_user(session: Session, username: str, email: str, password: str = 'hashed_password') -> None:
    user = model.User(username=username, email=email, password=password)
    session.add(user)
    session.commit()


def test_repository_can_save_a_user(sqlite_session):
    rows = tuple(
        sqlite_session.execute(
            'SELECT username, email, password, otp_secret, otp, is_superuser, avatar, date_joined FROM "users"',
        ),
    )
    assert rows == ()

    user = model.User(username=TestData.username.test, email=TestData.email.user, password='hashed_password')

    repo = UserRepository(session=sqlite_session)
    repo.add(user=user)
    sqlite_session.commit()

    rows = tuple(
        sqlite_session.execute(
            'SELECT username, email, password, otp_secret, otp, is_superuser, avatar, date_joined FROM "users"',
        ),
    )
    assert rows == (
        (
            TestData.username.test,
            TestData.email.user,
            'hashed_password',
            '',
            False,
            False,
            None,
            f'{user.date_joined}',
        ),
    )


def test_repository_can_retrieve_a_user(sqlite_session):
    _create_user(session=sqlite_session, username=TestData.username.test, email=TestData.email.user)
    _create_user(session=sqlite_session, username=TestData.username.user, email=TestData.email.user2)

    expected = model.User(
        username=TestData.username.test,
        email=TestData.email.user,
        password='hashed_password',
    )
    repo = UserRepository(session=sqlite_session)

    # Get by username
    retrieved = repo.get(username=TestData.username.test)
    assert retrieved == expected

    # Get by email
    retrieved = repo.get(email=TestData.email.user)
    assert retrieved == expected


def test_repository_can_not_retrieve_a_user(sqlite_session):
    _create_user(session=sqlite_session, username=TestData.username.test, email=TestData.email.user)
    _create_user(session=sqlite_session, username=TestData.username.user, email=TestData.email.user2)

    repo = UserRepository(session=sqlite_session)

    retrieved = repo.get(email=TestData.email.bot)
    assert retrieved is None
