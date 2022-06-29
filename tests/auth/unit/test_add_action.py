import uuid
from datetime import datetime

import config
from src.auth.domain import model


def test_user_can_add_action():
    user = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    action = model.UserAction(
        uuid=f'{uuid.uuid4()}', type=config.UserActionType.registered, created_at=datetime.utcnow(),
    )
    action2 = model.UserAction(
        uuid=f'{uuid.uuid4()}', type=config.UserActionType.registered, created_at=datetime.utcnow(),
    )

    assert user.count_actions == 0
    assert user.actions == []

    model.add_action(action=action, user=user)
    assert user.count_actions == 1
    assert user.actions == [action]

    model.add_action(action=action2, user=user)
    assert user.count_actions == 2
    assert sorted(user.actions, key=lambda _action: _action.created_at) == [action, action2]

    # Add an existing one
    model.add_action(action=action, user=user)
    assert user.count_actions == 2
    assert sorted(user.actions, key=lambda _action: _action.created_at) == [action, action2]


def test_user_can_remove_action():
    user = model.User(username='test', email='user@example.com', password='password', otp_secret='secret')
    action = model.UserAction(
        uuid=f'{uuid.uuid4()}',
        type=config.UserActionType.registered,
        created_at=datetime.utcnow(),
        ip_address='0.0.0.0',
    )
    action2 = model.UserAction(
        uuid=f'{uuid.uuid4()}', type=config.UserActionType.registered, created_at=datetime.utcnow(),
    )

    model.add_action(action=action, user=user)
    model.add_action(action=action2, user=user)
    assert user.count_actions == 2
    assert sorted(user.actions, key=lambda _action: _action.created_at) == [action, action2]

    model.remove_action(action=action, user=user)
    assert user.count_actions == 1
    assert user.actions == [action2]

    # Delete non-existent
    model.remove_action(action=action, user=user)
    assert user.count_actions == 1
    assert user.actions == [action2]

    model.remove_action(action=action2, user=user)
    assert user.count_actions == 0
    assert user.actions == []
