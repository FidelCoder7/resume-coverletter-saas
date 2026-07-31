from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.common.constants import UserRole
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_admin_endpoint_requires_authentication(
    client: TestClient,
):
    response = client.get(
        "/api/admin/access",
    )

    assert response.status_code == 401


def test_admin_endpoint_rejects_regular_user(
    authenticated_client,
):
    client, user = authenticated_client

    response = client.get(
        "/api/admin/access",
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Administrator access required.",
    }

    assert user.role == UserRole.USER


def test_admin_endpoint_allows_admin_user(
    client: TestClient,
    db_session: Session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    response = client.post(
        "/auth/login",
        data={
            "username": admin.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    assert response.status_code == 200

    access_token = response.json()["access_token"]

    response = client.get(
        "/api/admin/access",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Administrator access granted.",
        "role": UserRole.ADMIN.value,
    }


def test_admin_can_get_dashboard_metrics(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/metrics",
    )

    assert response.status_code == 200



def test_admin_can_get_dashboard_time_series(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/metrics/timeseries",
        params={
            "days": 7,
        },
    )

    assert response.status_code == 200


def test_non_admin_cannot_get_dashboard_metrics(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        "/api/admin/metrics",
    )

    assert response.status_code == 403


def test_non_admin_cannot_get_dashboard_time_series(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        "/api/admin/metrics/timeseries",
    )

    assert response.status_code == 403