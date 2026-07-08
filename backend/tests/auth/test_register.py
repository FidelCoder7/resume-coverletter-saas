from tests.factories.user_factory import create_user


def test_register_success(client, db_session):
    payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "password": "Password123!",
    }

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert data["is_email_verified"] is False


def test_register_duplicate_email(client, db_session):
    create_user(
        db_session,
        email="john@example.com",
    )

    payload = {
        "full_name": "Another User",
        "email": "john@example.com",
        "password": "Password123!",
    }

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 409

    assert response.json()["detail"]
