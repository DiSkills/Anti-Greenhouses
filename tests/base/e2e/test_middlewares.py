from uuid import uuid4

from fastapi import status

from config import MongoTables
from main import app
from tests.conftest import TestData


def test_bad_logins_middleware_return_403_when_user_ip_is_blocked(e2e):
    mongo_verifications = e2e.mongo[MongoTables.verifications.name]
    mongo_bad_logins = e2e.mongo[MongoTables.bad_logins.name]

    mongo_bad_logins.insert_many(
        [
            {'uuid': f'{uuid4()}', 'ip_address': TestData.ip_address},
            {'uuid': f'{uuid4()}', 'ip_address': TestData.ip_address},
            {'uuid': f'{uuid4()}', 'ip_address': TestData.ip_address},
        ],
    )

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ()

    data = {'email': TestData.email.user}
    headers = {'x-forwarded-for': TestData.ip_address}

    response = e2e.client.post(url=f'{app.url_path_for("registration_request")}', headers=headers, json=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Many bad login attempts, your ip is temporarily blocked.'}

    rows = tuple(mongo_verifications.find({}, {'_id': False}))
    assert rows == ()
