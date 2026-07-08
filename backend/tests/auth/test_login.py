from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_login_success(client, db_session):
    create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "john@example.com",
            "password": DEFAULT_PASSWORD,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert "refresh_token" in body
    assert body["user"]["email"] == "john@example.com"


def test_login_wrong_password(client, db_session):
    create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "john@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401


def test_login_unknown_email(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "missing@example.com",
            "password": DEFAULT_PASSWORD,
        },
    )

    assert response.status_code == 401
