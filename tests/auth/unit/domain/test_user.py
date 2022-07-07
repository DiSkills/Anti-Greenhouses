import uuid
from datetime import datetime

import config
from src.auth.domain import model


def test_users_are_equal_by_username():
    first_user = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    second_user = model.User(username='test', email='python@example.com', password='password', otp_secret='secret')

    assert first_user == second_user


def test_users_are_not_equal_by_username():
    first_user = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    second_user = model.User(username='user', email='python@example.com', password='password', otp_secret='secret')

    assert (first_user == second_user) is False


def test_user_is_not_equal_another_object():

    class AnotherObject:
        pass

    user = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    another_object = AnotherObject()

    assert (user == another_object) is False


def test_user_the_represent_method():
    user = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')

    assert user.__repr__() == f'<User {user.username}>'
    assert f'{user}' == f'<User {user.username}>'


def test_user_can_add_action():
    user = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    action = model.UserAction(
        uuid=f'{uuid.uuid4()}',
        type=config.UserActionType.registered,
        created_at=datetime.utcnow(),
        ip_address='0.0.0.0',
    )

    assert len(user._actions) == 0

    user.add_action(action=action)
    assert len(user._actions) == 1

    user.add_action(action=action)
    assert len(user._actions) == 1


def test_user_can_remove_action():
    user = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    action = model.UserAction(
        uuid=f'{uuid.uuid4()}',
        type=config.UserActionType.registered,
        created_at=datetime.utcnow(),
        ip_address='0.0.0.0',
    )

    assert len(user._actions) == 0

    user.remove_action(action=action)
    assert len(user._actions) == 0

    # Add
    user.add_action(action=action)

    # Remove
    assert len(user._actions) == 1

    user.remove_action(action=action)
    assert len(user._actions) == 0


def test_user_can_get_count_actions():
    user = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    action = model.UserAction(
        uuid=f'{uuid.uuid4()}',
        type=config.UserActionType.registered,
        created_at=datetime.utcnow(),
        ip_address='0.0.0.0',
    )

    assert user.count_actions == 0
    user.add_action(action=action)
    assert user.count_actions == 1

    user.add_action(
        action=model.UserAction(
            uuid=f'{uuid.uuid4()}',
            type=config.UserActionType.registered,
            created_at=datetime.utcnow(),
            ip_address='0.0.0.0',
        ),
    )
    assert user.count_actions == 2

    user.remove_action(action=action)
    assert user.count_actions == 1


def test_user_can_get_actions():
    user = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    action = model.UserAction(
        uuid=f'{uuid.uuid4()}',
        type=config.UserActionType.registered,
        created_at=datetime.utcnow(),
        ip_address='0.0.0.0',
    )
    action2 = model.UserAction(
        uuid=f'{uuid.uuid4()}',
        type=config.UserActionType.registered,
        created_at=datetime.utcnow(),
        ip_address='0.0.0.0',
    )

    assert user.actions == []

    user.add_action(action=action)
    user.add_action(action=action2)
    assert sorted(user.actions, key=lambda _action: _action.created_at) == [action, action2]

    user.remove_action(action=action)
    assert user.actions == [action2]
