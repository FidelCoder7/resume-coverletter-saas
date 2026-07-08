from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_get_profile(client, db_session):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.get(
        "api/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == user.email
    assert data["full_name"] == user.full_name
    assert data["is_email_verified"] is True


def test_update_profile(client, db_session):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )
    print(login.status_code)
    print(login.text)

    token = login.json()["access_token"]

    response = client.patch(
        "api/users/me",
        json={
            "full_name": "John Smith",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["full_name"] == "John Smith"


def test_get_profile_requires_authentication(client):
    response = client.get("api/users/me")

    assert response.status_code == 401


def test_delete_account(client, db_session):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )
    print(login.status_code)
    print(login.text)
    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.delete(
        "api/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204
