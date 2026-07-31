from app.admin.models import AdminAuditLog
from app.admin.repository import AdminAuditLogRepository
from app.common.constants import AdminAuditAction, UserRole
from tests.factories.user_factory import create_user


def test_repository_can_create_audit_log(
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

    audit_log = repository.create(
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_SUSPENDED,
        reason="Suspicious account activity.",
        event_metadata={
            "previous_status": "active",
            "new_status": "suspended",
        },
    )

    assert audit_log.id is not None
    assert audit_log.admin_id == admin.id
    assert audit_log.target_user_id == target_user.id
    assert audit_log.action == AdminAuditAction.USER_SUSPENDED
    assert audit_log.reason == "Suspicious account activity."
    assert audit_log.event_metadata == {
        "previous_status": "active",
        "new_status": "suspended",
    }


def test_repository_can_get_audit_log_by_id(
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

    repository = AdminAuditLogRepository(
        db_session,
    )

    result = repository.get_by_id(
        audit_log.id,
    )

    assert result is not None
    assert result.id == audit_log.id


def test_repository_lists_audit_logs_for_target_user(
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
    )

    other_user = create_user(
        db_session,
    )

    repository = AdminAuditLogRepository(
        db_session,
    )

    repository.create(
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_SUSPENDED,
    )

    repository.create(
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_ACTIVATED,
    )

    repository.create(
        admin_id=admin.id,
        target_user_id=other_user.id,
        action=AdminAuditAction.USER_DELETED,
    )

    logs, total = repository.list_by_target_user(
        target_user_id=target_user.id,
        page=1,
        page_size=20,
    )

    assert total == 2
    assert len(logs) == 2
    assert all(log.target_user_id == target_user.id for log in logs)


def test_repository_lists_audit_logs_for_admin(
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    other_admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    target_user = create_user(
        db_session,
    )

    repository = AdminAuditLogRepository(
        db_session,
    )

    repository.create(
        admin_id=admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_SUSPENDED,
    )

    repository.create(
        admin_id=other_admin.id,
        target_user_id=target_user.id,
        action=AdminAuditAction.USER_ACTIVATED,
    )

    logs, total = repository.list_by_admin(
        admin_id=admin.id,
        page=1,
        page_size=20,
    )

    assert total == 1
    assert len(logs) == 1
    assert logs[0].admin_id == admin.id


def test_repository_lists_recent_audit_logs(
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

    for _ in range(3):
        repository.create(
            admin_id=admin.id,
            target_user_id=target_user.id,
            action=AdminAuditAction.USER_SUSPENDED,
        )

    logs, total = repository.list_recent(
        page=1,
        page_size=2,
    )

    assert total == 3
    assert len(logs) == 2
