import uuid

from fastapi import status

from main import app


def test_registration_request_return_201_and_create_a_verification(e2e):
    rows = tuple(e2e.session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == ()

    data = {'email': 'user@example.com'}

    response = e2e.client.post(url=f'{app.url_path_for("registration_request")}', json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'msg': 'Please check your email, copy the sent code, you will need it to continue registration.',
    }

    rows = tuple(e2e.session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == (('user@example.com', rows[0][1]),)


def test_registration_request_return_400_when_verification_with_this_email_exists(e2e):
    email = 'user@example.com'
    _uuid = f'{uuid.uuid4()}'
    e2e.session.execute(
        'INSERT INTO verifications (email, uuid) VALUES (:email, :uuid)', {'email': email, 'uuid': _uuid},
    )
    e2e.session.commit()

    rows = tuple(e2e.session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == (('user@example.com', _uuid),)

    response = e2e.client.post(url=f'{app.url_path_for("registration_request")}', json={'email': email})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'Verification with this email already exists, we sent you another email with a code.',
    }

    rows = tuple(e2e.session.execute('SELECT email, uuid FROM "verifications"'))
    assert rows == (('user@example.com', _uuid),)
