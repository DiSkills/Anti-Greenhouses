from uuid import uuid4

from src.auth.domain import model
from tests.conftest import TestData


def test_verifications_are_equal_by_uuid():
    uuid = f'{uuid4()}'
    first_verification = model.Verification(email=TestData.email.user, uuid=uuid)
    second_verification = model.Verification(email=TestData.email.python, uuid=uuid)

    assert first_verification == second_verification


def test_verifications_are_not_equal_by_uuid():
    first_verification = model.Verification(email=TestData.email.user, uuid=f'{uuid4()}')
    second_verification = model.Verification(email=TestData.email.python, uuid=f'{uuid4()}')

    assert (first_verification == second_verification) is False


def test_verification_is_not_equal_another_object():

    class AnotherObject:
        pass

    verification = model.Verification(email=TestData.email.user, uuid=f'{uuid4()}')
    another_object = AnotherObject()

    assert (verification == another_object) is False


def test_verification_the_represent_method():
    verification = model.Verification(email=TestData.email.user, uuid=f'{uuid4()}')

    assert verification.__repr__() == f'<Verification {verification.uuid}>'
    assert f'{verification}' == f'<Verification {verification.uuid}>'


def test_verification_the_dict_method():
    verification = model.Verification(email=TestData.email.user, uuid=f'{uuid4()}')

    assert verification.dict() == {'uuid': verification.uuid, 'email': TestData.email.user}
