from datetime import datetime
from uuid import uuid4

import config
from src.auth.domain import model
from tests.conftest import TestData


def test_user_actions_are_equal_by_uuid():
    uuid = f'{uuid4()}'
    first_user_action = model.UserAction(
        uuid=uuid, type=config.UserActionType.registered, created_at=datetime.utcnow(), ip_address=TestData.ip_address,
    )
    second_user_action = model.UserAction(
        uuid=uuid, type=config.UserActionType.registered, created_at=datetime.utcnow(),
    )

    assert first_user_action == second_user_action


def test_user_actions_are_not_equal_by_uuid():
    uuid = f'{uuid4()}'
    first_user_action = model.UserAction(
        uuid=uuid, type=config.UserActionType.registered, created_at=datetime.utcnow(), ip_address=TestData.ip_address,
    )
    second_user_action = model.UserAction(
        uuid=f'{uuid4()}', type=config.UserActionType.registered, created_at=datetime.utcnow(),
    )

    assert (first_user_action == second_user_action) is False


def test_user_action_is_not_equal_another_object():

    class AnotherObject:
        pass

    uuid = f'{uuid4()}'
    user_action = model.UserAction(
        uuid=uuid, type=config.UserActionType.registered, created_at=datetime.utcnow(), ip_address=TestData.ip_address,
    )
    another_object = AnotherObject()

    assert (user_action == another_object) is False


def test_user_action_the_represent_method():
    user_action = model.UserAction(
        uuid=f'{uuid4()}',
        type=config.UserActionType.registered,
        created_at=datetime.utcnow(),
        ip_address=TestData.ip_address,
    )

    assert user_action.__repr__() == f'<UserAction {user_action.uuid}>'
    assert f'{user_action}' == f'<UserAction {user_action.uuid}>'
