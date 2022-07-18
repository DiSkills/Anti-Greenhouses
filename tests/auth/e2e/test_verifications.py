from datetime import datetime
from uuid import uuid4

from fastapi import status

from main import app
from tests.conftest import TestData


def test_registration_request_return_201_and_create_a_verification(mocker, e2e):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    rows = tuple(e2e.session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ()

    data = {'email': TestData.email.user}

    response = e2e.client.post(url=f'{app.url_path_for("registration_request")}', json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'msg': 'Please check your email, copy the sent code, you will need it to continue registration.',
    }

    rows = tuple(e2e.session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ((TestData.email.user, rows[0][1]),)


def test_registration_request_return_400_when_verification_with_this_email_exists(mocker, e2e):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    email = TestData.email.user
    uuid = f'{uuid4()}'
    e2e.session.execute(
        'INSERT INTO verifications (email, uuid) VALUES (:email, :uuid)', {'email': email, 'uuid': uuid},
    )
    e2e.session.commit()

    rows = tuple(e2e.session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ((TestData.email.user, uuid),)

    response = e2e.client.post(url=f'{app.url_path_for("registration_request")}', json={'email': email})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'Verification with this email already exists, we sent you another email with a code.',
    }

    rows = tuple(e2e.session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ((TestData.email.user, uuid),)


def test_registration_request_return_400_when_user_with_this_email_exists(mocker, e2e):
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    email = TestData.email.user
    date_joined = datetime.utcnow()
    e2e.session.execute(
        'INSERT INTO users (username, email, password, otp_secret, otp, is_superuser, avatar, date_joined) VALUES '
        '(:username, :email, :password, :otp_secret, FALSE, FALSE, NULL, :date_joined)',
        {
            'username': TestData.username.test,
            'email': email,
            'password': 'hashed_password',
            'otp_secret': 'otp_secret',
            'date_joined': date_joined,
        },
    )
    e2e.session.commit()

    rows = tuple(
        e2e.session.execute(
            'SELECT username, email, password, otp_secret, otp, is_superuser, avatar, date_joined FROM "users"',
        ),
    )
    assert rows == ((TestData.username.test, email, 'hashed_password', 'otp_secret', False, False, None, date_joined),)

    rows = tuple(e2e.session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ()

    response = e2e.client.post(url=f'{app.url_path_for("registration_request")}', json={'email': email})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'User with this email exists.'}

    rows = tuple(e2e.session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ()
