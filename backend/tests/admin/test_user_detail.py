from uuid import uuid4

from app.common.constants import UserRole
from tests.factories.user_factory import create_user


def test_admin_can_get_user_details(
    client,
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
        email="target@example.com",
        full_name="Target User",
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": admin.email,
            "password": "Password123!",
        },
    )

    client.headers.update(
        {
            "Authorization": (f"Bearer {login_response.json()['access_token']}"),
        }
    )

    response = client.get(
        f"/api/admin/users/{target_user.id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(target_user.id)
    assert data["email"] == "target@example.com"
    assert data["full_name"] == "Target User"
    assert "created_at" in data
    assert "updated_at" in data
    assert "deleted_at" in data


def test_regular_user_cannot_get_user_details(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        f"/api/admin/users/{uuid4()}",
    )

    assert response.status_code == 403


def test_admin_getting_nonexistent_user_returns_404(
    client,
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": admin.email,
            "password": "Password123!",
        },
    )

    client.headers.update(
        {
            "Authorization": (f"Bearer {login_response.json()['access_token']}"),
        }
    )

    response = client.get(
        f"/api/admin/users/{uuid4()}",
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "User not found.",
    }
