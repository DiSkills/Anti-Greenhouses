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
