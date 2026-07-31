from app.common.constants import AccountStatus
from tests.factories.user_factory import create_user


def test_admin_can_get_dashboard_metrics(
    admin_client,
    db_session,
):
    client, admin = admin_client

    create_user(
        db_session,
        verified=True,
    )

    suspended_user = create_user(
        db_session,
        verified=True,
    )

    suspended_user.status = AccountStatus.SUSPENDED

    create_user(
        db_session,
        verified=False,
    )

    db_session.commit()

    response = client.get(
        "/api/admin/metrics",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["users"]["total_users"] >= 4
    assert data["users"]["active_users"] >= 1
    assert data["users"]["suspended_users"] >= 1
    assert data["users"]["verified_users"] >= 2
    assert data["users"]["unverified_users"] >= 1
    assert data["users"]["total_admins"] >= 1
    assert "subscriptions" in data
    assert "total_audit_logs" in data


def test_non_admin_cannot_get_dashboard_metrics(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        "/api/admin/metrics",
    )

    assert response.status_code == 403


def test_unauthenticated_user_cannot_get_dashboard_metrics(
    client,
):
    response = client.get(
        "/api/admin/metrics",
    )

    assert response.status_code == 401


def test_admin_dashboard_metrics_returns_zero_for_empty_audit_logs(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/metrics",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_audit_logs"] == 0