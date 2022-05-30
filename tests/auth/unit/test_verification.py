import uuid

from src.auth.domain import model


def test_verifications_are_equal_by_uuid():
    _uuid = f'{uuid.uuid4()}'
    first_verification = model.Verification(email='user@example.com', uuid=_uuid)
    second_verification = model.Verification(email='python@example.com', uuid=_uuid)

    assert first_verification == second_verification


def test_verifications_are_not_equal_by_uuid():
    first_verification = model.Verification(email='user@example.com', uuid=f'{uuid.uuid4()}')
    second_verification = model.Verification(email='python@example.com', uuid=f'{uuid.uuid4()}')

    assert (first_verification == second_verification) is False


def test_verification_is_not_equal_another_object():

    class AnotherObject:
        pass

    verification = model.Verification(email='user@example.com', uuid=f'{uuid.uuid4()}')
    another_object = AnotherObject()

    assert (verification == another_object) is False


def test_verification_the_represent_method():
    verification = model.Verification(email='user@example.com', uuid=f'{uuid.uuid4()}')

    assert verification.__repr__() == f'<Verification {verification.uuid}>'
    assert f'{verification}' == f'<Verification {verification.uuid}>'
