
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.admin.models import AdminAuditLog
from app.common.constants import AdminAuditAction, UserRole
from tests.factories.user_factory import create_user


def create_audit_log(
    db_session,
    *,
    admin_id,
    target_user_id,
    action=AdminAuditAction.USER_SUSPENDED,
    reason=None,
    event_metadata=None,
):
    """
    Create and persist an administrative audit log for testing.
    """

    audit_log = AdminAuditLog(
        admin_id=admin_id,
        target_user_id=target_user_id,
        action=action,
        reason=reason,
        event_metadata=event_metadata,
    )

    db_session.add(audit_log)
    db_session.commit()
    db_session.refresh(audit_log)

    return audit_log


def test_admin_audit_log_can_be_created(
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
    )

    audit_log = AdminAuditLog(
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_SUSPENDED,
        reason="Suspicious account activity.",
        event_metadata={
            "previous_status": "active",
            "new_status": "suspended",
        },
    )

    db_session.add(audit_log)
    db_session.commit()
    db_session.refresh(audit_log)

    assert audit_log.id is not None
    assert audit_log.admin_id == admin.id
    assert audit_log.target_user_id == target_user.id
    assert audit_log.action == AdminAuditAction.USER_SUSPENDED
    assert audit_log.reason == "Suspicious account activity."
    assert audit_log.event_metadata == {
        "previous_status": "active",
        "new_status": "suspended",
    }


def test_admin_audit_log_relationships(
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
    )

    audit_log = AdminAuditLog(
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_DELETED,
    )

    db_session.add(audit_log)
    db_session.commit()
    db_session.refresh(audit_log)

    assert audit_log.admin.id == admin.id
    assert audit_log.target_user.id == target_user.id


def test_admin_can_list_recent_audit_logs(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
    )

    create_audit_log(
        db_session,
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_SUSPENDED,
        reason="Suspicious activity.",
    )

    create_audit_log(
        db_session,
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_ACTIVATED,
        reason="Account reviewed.",
    )

    response = client.get(
        "/api/admin/audit-logs",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total_pages"] == 1
    assert len(data["items"]) == 2


def test_admin_can_paginate_recent_audit_logs(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
    )

    for _ in range(5):
        create_audit_log(
            db_session,
            admin_id=admin.id,
            target_user_id=target_user.id,
        )

    response = client.get(
        "/api/admin/audit-logs",
        params={
            "page": 1,
            "page_size": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 5
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total_pages"] == 3
    assert len(data["items"]) == 2


def test_admin_can_get_audit_log_by_id(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
    )

    audit_log = create_audit_log(
        db_session,
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_SUSPENDED,
        reason="Suspicious account activity.",
        event_metadata={
            "previous_status": "active",
            "new_status": "suspended",
        },
    )

    response = client.get(
        f"/api/admin/audit-logs/{audit_log.id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(audit_log.id)
    assert data["admin_id"] == str(admin.id)
    assert data["target_user_id"] == str(target_user.id)
    assert data["action"] == AdminAuditAction.USER_SUSPENDED.value
    assert data["reason"] == "Suspicious account activity."
    assert data["event_metadata"] == {
        "previous_status": "active",
        "new_status": "suspended",
    }


def test_admin_getting_nonexistent_audit_log_returns_404(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        f"/api/admin/audit-logs/{uuid4()}",
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Audit log not found.",
    }


def test_admin_can_list_audit_logs_for_target_user(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
    )

    other_user = create_user(
        db_session,
    )

    create_audit_log(
        db_session,
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_SUSPENDED,
    )

    create_audit_log(
        db_session,
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_ACTIVATED,
    )

    create_audit_log(
        db_session,
        admin_id=admin.id,
        target_user_id=other_user.id,
        action=AdminAuditAction.USER_DELETED,
    )

    response = client.get(
        f"/api/admin/users/{target_user.id}/audit-logs",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2

    assert all(
        item["target_user_id"] == str(target_user.id)
        for item in data["items"]
    )


def test_admin_can_paginate_target_user_audit_logs(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
    )

    for _ in range(5):
        create_audit_log(
            db_session,
            admin_id=admin.id,
            target_user_id=target_user.id,
        )

    response = client.get(
        f"/api/admin/users/{target_user.id}/audit-logs",
        params={
            "page": 1,
            "page_size": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 5
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total_pages"] == 3
    assert len(data["items"]) == 2


def test_admin_can_list_audit_logs_for_specific_admin(
    admin_client,
    db_session,
):
    client, admin = admin_client

    second_admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
    )

    create_audit_log(
        db_session,
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_SUSPENDED,
    )

    create_audit_log(
        db_session,
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_ACTIVATED,
    )

    create_audit_log(
        db_session,
        admin_id=second_admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_DELETED,
    )

    response = client.get(
        f"/api/admin/admins/{admin.id}/audit-logs",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 2

    assert all(
        item["admin_id"] == str(admin.id)
        for item in data["items"]
    )


def test_admin_can_paginate_admin_audit_logs(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
    )

    for _ in range(5):
        create_audit_log(
            db_session,
            admin_id=admin.id,
            target_user_id=target_user.id,
        )

    response = client.get(
        f"/api/admin/admins/{admin.id}/audit-logs",
        params={
            "page": 1,
            "page_size": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 5
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total_pages"] == 3
    assert len(data["items"]) == 2


def test_regular_user_cannot_list_recent_audit_logs(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        "/api/admin/audit-logs",
    )

    assert response.status_code == 403


def test_regular_user_cannot_get_audit_log(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
    )

    audit_log = create_audit_log(
        db_session,
        admin_id=admin.id,
        target_user_id=target_user.id,
    )

    response = client.get(
        f"/api/admin/audit-logs/{audit_log.id}",
    )

    assert response.status_code == 403


def test_regular_user_cannot_list_target_user_audit_logs(
    authenticated_client,
    db_session,
):
    client, _ = authenticated_client

    target_user = create_user(
        db_session,
    )

    response = client.get(
        f"/api/admin/users/{target_user.id}/audit-logs",
    )

    assert response.status_code == 403


def test_regular_user_cannot_list_admin_audit_logs(
    authenticated_client,
    db_session,
):
    client, admin = authenticated_client

    response = client.get(
        f"/api/admin/admins/{admin.id}/audit-logs",
    )

    assert response.status_code == 403


def test_recent_audit_logs_returns_empty_result(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/audit-logs",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total_pages"] == 0


def test_target_user_audit_logs_returns_empty_result(
    admin_client,
    db_session,
):
    client, _ = admin_client

    target_user = create_user(
        db_session,
    )

    response = client.get(
        f"/api/admin/users/{target_user.id}/audit-logs",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total_pages"] == 0



def test_admin_can_filter_audit_logs_by_action(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
    )

    db_session.add_all(
        [
            AdminAuditLog(
                admin_id=admin.id,
                target_user_id=target_user.id,
                action=AdminAuditAction.USER_SUSPENDED,
            ),
            AdminAuditLog(
                admin_id=admin.id,
                target_user_id=target_user.id,
                action=AdminAuditAction.USER_ACTIVATED,
            ),
        ]
    )

    db_session.commit()

    response = client.get(
        "/api/admin/audit-logs",
        params={
            "action": AdminAuditAction.USER_SUSPENDED.value,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["action"] == (
        AdminAuditAction.USER_SUSPENDED.value
    )


def test_admin_can_filter_audit_logs_by_target_user(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
    )

    other_user = create_user(
        db_session,
    )

    db_session.add_all(
        [
            AdminAuditLog(
                admin_id=admin.id,
                target_user_id=target_user.id,
                action=AdminAuditAction.USER_SUSPENDED,
            ),
            AdminAuditLog(
                admin_id=admin.id,
                target_user_id=other_user.id,
                action=AdminAuditAction.USER_ACTIVATED,
            ),
        ]
    )

    db_session.commit()

    response = client.get(
        "/api/admin/audit-logs",
        params={
            "target_user_id": str(target_user.id),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["target_user_id"] == (
        str(target_user.id)
    )


def test_admin_can_filter_audit_logs_by_admin(
    admin_client,
    db_session,
):
    client, admin = admin_client

    second_admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
    )

    db_session.add_all(
        [
            AdminAuditLog(
                admin_id=admin.id,
                target_user_id=target_user.id,
                action=AdminAuditAction.USER_SUSPENDED,
            ),
            AdminAuditLog(
                admin_id=second_admin.id,
                target_user_id=target_user.id,
                action=AdminAuditAction.USER_ACTIVATED,
            ),
        ]
    )

    db_session.commit()

    response = client.get(
        "/api/admin/audit-logs",
        params={
            "admin_id": str(admin.id),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["admin_id"] == (
        str(admin.id)
    )



def test_admin_can_filter_audit_logs_by_date_range(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
    )

    old_log = AdminAuditLog(
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_SUSPENDED,
    )

    recent_log = AdminAuditLog(
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_ACTIVATED,
    )

    db_session.add_all(
        [
            old_log,
            recent_log,
        ]
    )

    db_session.flush()

    now = datetime.now(UTC)

    old_log.created_at = now - timedelta(days=10)
    recent_log.created_at = now - timedelta(days=1)

    db_session.commit()

    response = client.get(
        "/api/admin/audit-logs",
        params={
            "created_after": (
                now - timedelta(days=3)
            ).isoformat(),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["action"] == (
        AdminAuditAction.USER_ACTIVATED.value
    )


def test_admin_can_combine_audit_log_filters(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
    )

    db_session.add_all(
        [
            AdminAuditLog(
                admin_id=admin.id,
                target_user_id=target_user.id,
                action=AdminAuditAction.USER_SUSPENDED,
            ),
            AdminAuditLog(
                admin_id=admin.id,
                target_user_id=target_user.id,
                action=AdminAuditAction.USER_ACTIVATED,
            ),
        ]
    )

    db_session.commit()

    response = client.get(
        "/api/admin/audit-logs",
        params={
            "action": AdminAuditAction.USER_SUSPENDED.value,
            "admin_id": str(admin.id),
            "target_user_id": str(target_user.id),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["action"] == (
        AdminAuditAction.USER_SUSPENDED.value
    )



def test_admin_audit_log_filter_supports_pagination(
    admin_client,
    db_session,
):
    client, admin = admin_client

    target_user = create_user(
        db_session,
    )

    for _ in range(5):
        db_session.add(
            AdminAuditLog(
                admin_id=admin.id,
                target_user_id=target_user.id,
                action=AdminAuditAction.USER_SUSPENDED,
            )
        )

    db_session.commit()

    response = client.get(
        "/api/admin/audit-logs",
        params={
            "page": 2,
            "page_size": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 5
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert data["total_pages"] == 3
    assert len(data["items"]) == 2


def test_regular_user_cannot_list_audit_logs(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        "/api/admin/audit-logs",
    )

    assert response.status_code == 403