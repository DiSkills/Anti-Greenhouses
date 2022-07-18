import uuid
from datetime import datetime

import config
from src.auth.domain import model
from tests.conftest import TestData


def test_user_can_add_action():
    user = model.User(username=TestData.username.test, email=TestData.email.user, password=TestData.password.password)
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
