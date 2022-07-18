import uuid
from datetime import datetime

import config
from src.auth.domain import model
from tests.conftest import TestData


def test_user_can_remove_action():
    user = model.User(username=TestData.username.test, email=TestData.email.user, password=TestData.password.password)
    action = model.UserAction(
        uuid=f'{uuid.uuid4()}',
        type=config.UserActionType.registered,
        created_at=datetime.utcnow(),
        ip_address=TestData.ip_address,
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
