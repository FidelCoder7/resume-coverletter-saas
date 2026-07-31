from uuid import uuid4

from app.admin.models import AdminAuditLog
from app.common.constants import (
    AccountStatus,
    AdminAuditAction,
)
from tests.factories.user_factory import create_user


def test_admin_can_suspend_active_user(
    admin_client,
    db_session,
):
    client, _ = admin_client

    target_user = create_user(
        db_session,
        status=AccountStatus.ACTIVE,
    )

    response = client.post(
        f"/api/admin/users/{target_user.id}/suspend",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(target_user.id)
    assert data["status"] == AccountStatus.SUSPENDED.value

    db_session.refresh(target_user)

    assert target_user.status == AccountStatus.SUSPENDED
    assert target_user.deleted_at is None


def test_admin_can_reactivate_suspended_user(
    admin_client,
    db_session,
):
    client, _ = admin_client

    target_user = create_user(
        db_session,
        status=AccountStatus.SUSPENDED,
    )

    response = client.post(
        f"/api/admin/users/{target_user.id}/reactivate",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(target_user.id)
    assert data["status"] == AccountStatus.ACTIVE.value

    db_session.refresh(target_user)

    assert target_user.status == AccountStatus.ACTIVE
    assert target_user.deleted_at is None


def test_regular_user_cannot_suspend_user(
    authenticated_client,
    db_session,
):
    client, _ = authenticated_client

    target_user = create_user(
        db_session,
    )

    response = client.post(
        f"/api/admin/users/{target_user.id}/suspend",
    )

    assert response.status_code == 403


def test_regular_user_cannot_reactivate_user(
    authenticated_client,
    db_session,
):
    client, _ = authenticated_client

    target_user = create_user(
        db_session,
        status=AccountStatus.SUSPENDED,
    )

    response = client.post(
        f"/api/admin/users/{target_user.id}/reactivate",
    )

    assert response.status_code == 403


def test_admin_cannot_suspend_themselves(
    admin_client,
):
    client, admin = admin_client

    response = client.post(
        f"/api/admin/users/{admin.id}/suspend",
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": ("Administrators cannot suspend their own account."),
    }


def test_admin_cannot_reactivate_themselves(
    admin_client,
    db_session,
):
    client, admin = admin_client

    admin.status = AccountStatus.SUSPENDED
    db_session.commit()
    db_session.refresh(admin)

    response = client.post(
        f"/api/admin/users/{admin.id}/reactivate",
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": ("Administrators cannot reactivate their own account."),
    }


def test_admin_cannot_suspend_already_suspended_user(
    admin_client,
    db_session,
):
    client, _ = admin_client

    target_user = create_user(
        db_session,
        status=AccountStatus.SUSPENDED,
    )

    response = client.post(
        f"/api/admin/users/{target_user.id}/suspend",
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": "User account is already suspended.",
    }


def test_admin_cannot_reactivate_already_active_user(
    admin_client,
    db_session,
):
    client, _ = admin_client

    target_user = create_user(
        db_session,
        status=AccountStatus.ACTIVE,
    )

    response = client.post(
        f"/api/admin/users/{target_user.id}/reactivate",
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": "User account is already active.",
    }


def test_admin_cannot_suspend_deleted_user(
    admin_client,
    db_session,
):
    client, _ = admin_client

    target_user = create_user(
        db_session,
        status=AccountStatus.DELETED,
    )

    response = client.post(
        f"/api/admin/users/{target_user.id}/suspend",
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": ("Deleted user accounts cannot be suspended."),
    }


def test_admin_cannot_reactivate_deleted_user(
    admin_client,
    db_session,
):
    client, _ = admin_client

    target_user = create_user(
        db_session,
        status=AccountStatus.DELETED,
    )

    response = client.post(
        f"/api/admin/users/{target_user.id}/reactivate",
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": ("Deleted user accounts cannot be reactivated."),
    }


def test_suspend_nonexistent_user_returns_404(
    admin_client,
):
    client, _ = admin_client

    response = client.post(
        f"/api/admin/users/{uuid4()}/suspend",
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "User not found.",
    }



def test_reactivate_nonexistent_user_returns_404(
    admin_client,
):
    client, _ = admin_client

    response = client.post(
        f"/api/admin/users/{uuid4()}/reactivate",
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "User not found.",
    }


def test_admin_suspend_creates_audit_log(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
        status=AccountStatus.ACTIVE,
    )

    response = client.post(
        f"/api/admin/users/{target_user.id}/suspend",
        json={
            "reason": "Suspicious account activity.",
        },
    )

    assert response.status_code == 200

    audit_log = (
        db_session.query(AdminAuditLog)
        .filter(
            AdminAuditLog.admin_id == admin.id,
            AdminAuditLog.target_user_id == target_user.id,
            AdminAuditLog.action
            == AdminAuditAction.USER_SUSPENDED,
        )
        .one()
    )

    assert audit_log.reason == (
        "Suspicious account activity."
    )

    assert audit_log.event_metadata == {
        "previous_status": "active",
        "new_status": "suspended",
    }


def test_admin_reactivate_creates_audit_log(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
        status=AccountStatus.SUSPENDED,
    )

    response = client.post(
        f"/api/admin/users/{target_user.id}/reactivate",
        json={
            "reason": "Account suspension reviewed.",
        },
    )

    assert response.status_code == 200

    audit_log = (
        db_session.query(AdminAuditLog)
        .filter(
            AdminAuditLog.admin_id == admin.id,
            AdminAuditLog.target_user_id == target_user.id,
            AdminAuditLog.action
            == AdminAuditAction.USER_ACTIVATED,
        )
        .one()
    )

    assert audit_log.reason == (
        "Account suspension reviewed."
    )

    assert audit_log.event_metadata == {
        "previous_status": "suspended",
        "new_status": "active",
    }
 