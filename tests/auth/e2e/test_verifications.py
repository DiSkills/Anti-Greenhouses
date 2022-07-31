from datetime import datetime
from uuid import uuid4

from fastapi import status

from config import MongoTables
from main import app
from tests.conftest import TestData


def test_registration_request_return_201_and_create_a_verification(mocker, e2e):
    mongo_verifications = e2e.mongo[MongoTables.verifications.name]
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ()

    data = {'email': TestData.email.user}

    response = e2e.client.post(url=f'{app.url_path_for("registration_request")}', json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'msg': 'Please check your email, copy the sent code, you will need it to continue registration.',
    }

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ({'email': TestData.email.user, 'uuid': rows[0]['uuid']},)


def test_registration_request_return_400_when_verification_with_this_email_exists(mocker, e2e):
    mongo_verifications = e2e.mongo[MongoTables.verifications.name]
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    email = TestData.email.user
    uuid = f'{uuid4()}'
    mongo_verifications.insert_one({'email': email, 'uuid': uuid})

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ({'email': TestData.email.user, 'uuid': uuid},)

    response = e2e.client.post(url=f'{app.url_path_for("registration_request")}', json={'email': email})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'Verification with this email already exists, we sent you another email with a code.',
    }

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ({'email': TestData.email.user, 'uuid': uuid},)


def test_registration_request_return_400_when_user_with_this_email_exists(mocker, e2e):
    mongo_verifications = e2e.mongo[MongoTables.verifications.name]
    mocker.patch('src.base.send_email.send_email', return_value=None)
    mocker.patch('worker.send_email_task', return_value=None)

    email = TestData.email.user
    date_joined = datetime.utcnow()
    e2e.session.execute(
        'INSERT INTO users (username, email, password, otp_secret, otp, is_superuser, avatar, date_joined, uuid)'
        ' VALUES (:username, :email, :password, :otp_secret, FALSE, FALSE, NULL, :date_joined, :uuid)',
        {
            'username': TestData.username.test,
            'email': email,
            'password': 'hashed_password',
            'otp_secret': 'otp_secret',
            'date_joined': date_joined,
            'uuid': f'{uuid4()}',
        },
    )
    e2e.session.commit()

    rows = tuple(
        e2e.session.execute(
            'SELECT username, email, password, otp_secret, otp, is_superuser, avatar, date_joined FROM "users"',
        ),
    )
    assert rows == ((TestData.username.test, email, 'hashed_password', 'otp_secret', False, False, None, date_joined),)

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ()

    response = e2e.client.post(url=f'{app.url_path_for("registration_request")}', json={'email': email})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'User with this email exists.'}

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ()
