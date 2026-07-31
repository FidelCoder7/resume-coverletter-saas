import pytest

from app.admin.repository import AdminAuditLogRepository
from app.admin.schemas import AdminAuditLogCreate
from app.admin.service import AdminAuditLogService
from app.common.constants import (
    AdminAuditAction,
    UserRole,
)
from tests.factories.user_factory import create_user


def test_service_can_record_admin_action(
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
    )

    repository = AdminAuditLogRepository(
        db_session,
    )

    service = AdminAuditLogService(
        repository,
    )

    result = service.record(
        current_admin=admin,
        data=AdminAuditLogCreate(
            target_user_id=target_user.id,
            action=AdminAuditAction.USER_SUSPENDED,
            reason="Suspicious account activity.",
            event_metadata={
                "previous_status": "active",
                "new_status": "suspended",
            },
        ),
    )

    assert result.id is not None
    assert result.admin_id == admin.id
    assert result.target_user_id == target_user.id
    assert result.action == AdminAuditAction.USER_SUSPENDED
    assert result.reason == "Suspicious account activity."
    assert result.event_metadata == {
        "previous_status": "active",
        "new_status": "suspended",
    }


def test_non_admin_cannot_record_admin_action(
    db_session,
):
    regular_user = create_user(
        db_session,
        role=UserRole.USER,
    )

    target_user = create_user(
        db_session,
    )

    repository = AdminAuditLogRepository(
        db_session,
    )

    service = AdminAuditLogService(
        repository,
    )

    with pytest.raises(
        PermissionError,
        match="Only administrators can create audit logs.",
    ):
        service.record(
            current_admin=regular_user,
            data=AdminAuditLogCreate(
                target_user_id=target_user.id,
                action=AdminAuditAction.USER_SUSPENDED,
            ),
        )


def test_service_lists_target_user_audit_history(
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
    )

    repository = AdminAuditLogRepository(
        db_session,
    )

    service = AdminAuditLogService(
        repository,
    )

    service.record_action(
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_SUSPENDED,
    )

    service.record_action(
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_ACTIVATED,
    )

    result = service.list_for_target_user(
        target_user_id=target_user.id,
        page=1,
        page_size=20,
    )

    assert result.total == 2
    assert result.total_pages == 1
    assert len(result.items) == 2


def test_service_lists_admin_actions(
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
    )

    repository = AdminAuditLogRepository(
        db_session,
    )

    service = AdminAuditLogService(
        repository,
    )

    service.record_action(
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_SUSPENDED,
    )

    result = service.list_for_admin(
        admin_id=admin.id,
        page=1,
        page_size=20,
    )

    assert result.total == 1
    assert result.total_pages == 1
    assert len(result.items) == 1
    assert result.items[0].admin_id == admin.id


def test_service_lists_recent_audit_actions(
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
    )

    repository = AdminAuditLogRepository(
        db_session,
    )

    service = AdminAuditLogService(
        repository,
    )

    for _ in range(3):
        service.record_action(
            admin_id=admin.id,
            target_user_id=target_user.id,
            action=AdminAuditAction.USER_SUSPENDED,
        )

    result = service.list_recent(
        page=1,
        page_size=2,
    )

    assert result.total == 3
    assert result.total_pages == 2
    assert len(result.items) == 2
