from tests.utils import (
    auth_headers,
    authenticated_user,
)


def test_me_returns_current_user(
    client,
    db_session,
):
    user, token = authenticated_user(
        client,
        db_session,
    )

    response = client.get(
        "/auth/me",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(user.id)
    assert data["email"] == user.email
    assert data["full_name"] == user.full_name


def test_me_requires_authentication(client):
    response = client.get("/auth/me")

    assert response.status_code == 401
