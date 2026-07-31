import math
from uuid import UUID

from app.admin.exceptions import (
    AdminAuditLogNotFound,
    AdminUserActionNotAllowed,
    AdminUserNotFound,
)
from app.admin.repository import (
    AdminAuditLogRepository,
    AdminUserRepository,
)
from app.admin.schemas import (
    AdminAuditLogCreate,
    AdminAuditLogListQuery,
    AdminAuditLogListResponse,
    AdminAuditLogResponse,
    AdminUserDetailResponse,
    AdminUserListQuery,
    AdminUserListResponse,
)
from app.common.constants import (
    AccountStatus,
    AdminAuditAction,
    UserRole,
)
from app.users.models import User


class AdminUserService:
    """
    Business logic for administrative user management.
    """

    def __init__(
        self,
        repository: AdminUserRepository,
        audit_repository: AdminAuditLogRepository,
    ) -> None:
        self.repository = repository
        self.audit_repository = audit_repository

    def list_users(
        self,
        *,
        query: AdminUserListQuery,
    ) -> AdminUserListResponse:
        """
        Return a filtered and paginated list of users.
        """

        users, total = self.repository.list_users(
            page=query.page,
            page_size=query.page_size,
            search=query.search,
            role=query.role,
            status=query.status,
            subscription_plan=query.subscription_plan,
        )

        total_pages = math.ceil(total / query.page_size) if total > 0 else 0

        return AdminUserListResponse(
            items=users,
            total=total,
            page=query.page,
            page_size=query.page_size,
            total_pages=total_pages,
        )

    def get_user(
        self,
        *,
        user_id: UUID,
    ) -> AdminUserDetailResponse:
        """
        Return detailed information about a user.
        """

        user = self.repository.get_by_id(
            user_id,
        )

        if user is None:
            raise AdminUserNotFound(
                "User not found.",
            )

        return AdminUserDetailResponse.model_validate(
            user,
        )

    def suspend_user(
        self,
        *,
        user_id: UUID,
        current_admin: User,
        reason: str | None = None,
    ) -> AdminUserDetailResponse:
        """
        Suspend a user account and record the administrative action
        atomically.
        """

        user = self.repository.get_by_id(
            user_id,
        )

        if user is None:
            raise AdminUserNotFound(
                "User not found.",
            )

        if user.id == current_admin.id:
            raise AdminUserActionNotAllowed(
                "Administrators cannot suspend their own account.",
            )

        if user.status == AccountStatus.SUSPENDED:
            raise AdminUserActionNotAllowed(
                "User account is already suspended.",
            )

        if user.status == AccountStatus.DELETED:
            raise AdminUserActionNotAllowed(
                "Deleted user accounts cannot be suspended.",
            )

        previous_status = user.status.value

        try:
            user = self.repository.suspend(
                user,
            )

            self.audit_repository.create(
                admin_id=current_admin.id,
                target_user_id=user.id,
                action=AdminAuditAction.USER_SUSPENDED,
                reason=reason,
                event_metadata={
                    "previous_status": previous_status,
                    "new_status": user.status.value,
                },
            )

            self.repository.commit()

        except Exception:
            self.repository.rollback()
            raise

        return AdminUserDetailResponse.model_validate(
            user,
        )

    def reactivate_user(
        self,
        *,
        user_id: UUID,
        current_admin: User,
        reason: str | None = None,
    ) -> AdminUserDetailResponse:
        """
        Reactivate a suspended user account and record the administrative
        action atomically.
        """

        user = self.repository.get_by_id(
            user_id,
        )

        if user is None:
            raise AdminUserNotFound(
                "User not found.",
            )

        if user.id == current_admin.id:
            raise AdminUserActionNotAllowed(
                "Administrators cannot reactivate their own account.",
            )

        if user.status == AccountStatus.ACTIVE:
            raise AdminUserActionNotAllowed(
                "User account is already active.",
            )

        if user.status == AccountStatus.DELETED:
            raise AdminUserActionNotAllowed(
                "Deleted user accounts cannot be reactivated.",
            )

        previous_status = user.status.value

        try:
            user = self.repository.reactivate(
                user,
            )

            self.audit_repository.create(
                admin_id=current_admin.id,
                target_user_id=user.id,
                action=AdminAuditAction.USER_ACTIVATED,
                reason=reason,
                event_metadata={
                    "previous_status": previous_status,
                    "new_status": user.status.value,
                },
            )

            self.repository.commit()

        except Exception:
            self.repository.rollback()
            raise

        return AdminUserDetailResponse.model_validate(
            user,
        )


class AdminAuditLogService:
    """
    Business logic for administrative audit logging.
    """

    def __init__(
        self,
        repository: AdminAuditLogRepository,
    ) -> None:
        self.repository = repository

    def record(
        self,
        *,
        current_admin: User,
        data: AdminAuditLogCreate,
    ) -> AdminAuditLogResponse:
        """
        Record an administrative action in the audit log.

        Audit events can only be created by administrators.
        """

        if current_admin.role != UserRole.ADMIN:
            raise PermissionError(
                "Only administrators can create audit logs.",
            )

        audit_log = self.repository.create(
            admin_id=current_admin.id,
            target_user_id=data.target_user_id,
            action=data.action,
            reason=data.reason,
            event_metadata=data.event_metadata,
        )

        return AdminAuditLogResponse.model_validate(
            audit_log,
        )

    def record_action(
        self,
        *,
        admin_id: UUID,
        target_user_id: UUID,
        action: AdminAuditAction,
        reason: str | None = None,
        event_metadata: dict | None = None,
    ) -> AdminAuditLogResponse:
        """
        Record an administrative action using explicit identifiers.

        This method is intended for internal service-to-service use
        when the calling service has already validated the administrator.
        """

        audit_log = self.repository.create(
            admin_id=admin_id,
            target_user_id=target_user_id,
            action=action,
            reason=reason,
            event_metadata=event_metadata,
        )

        return AdminAuditLogResponse.model_validate(
            audit_log,
        )



    
    def get_by_id(
        self,
        *,
        audit_log_id: UUID,
    ) -> AdminAuditLogResponse:
        """
        Return a single administrative audit log by ID.
        """

        audit_log = self.repository.get_by_id(
            audit_log_id,
        )

        if audit_log is None:
            raise AdminAuditLogNotFound(
                "Audit log not found.",
            )

        return AdminAuditLogResponse.model_validate(
            audit_log,
        )



    def list_for_target_user(
        self,
        *,
        target_user_id: UUID,
        page: int,
        page_size: int,
    ) -> AdminAuditLogListResponse:
        """
        Return audit history for a target user.
        """

        logs, total = self.repository.list_by_target_user(
            target_user_id=target_user_id,
            page=page,
            page_size=page_size,
        )

        total_pages = math.ceil(total / page_size) if total > 0 else 0

        return AdminAuditLogListResponse(
            items=logs,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def list_for_admin(
        self,
        *,
        admin_id: UUID,
        page: int,
        page_size: int,
    ) -> AdminAuditLogListResponse:
        """
        Return administrative actions performed by a specific admin.
        """

        logs, total = self.repository.list_by_admin(
            admin_id=admin_id,
            page=page,
            page_size=page_size,
        )

        total_pages = math.ceil(total / page_size) if total > 0 else 0

        return AdminAuditLogListResponse(
            items=logs,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def list_recent(
        self,
        *,
        page: int,
        page_size: int,
    ) -> AdminAuditLogListResponse:
        """
        Return the most recent administrative actions.
        """

        logs, total = self.repository.list_recent(
            page=page,
            page_size=page_size,
        )

        total_pages = math.ceil(total / page_size) if total > 0 else 0

        return AdminAuditLogListResponse(
            items=logs,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )


    
    def list_filtered(
        self,
        *,
        query: AdminAuditLogListQuery,
    ) -> AdminAuditLogListResponse:
        """
        Return filtered and paginated administrative audit logs.
        """

        logs, total = self.repository.list_filtered(
            page=query.page,
            page_size=query.page_size,
            action=query.action,
            admin_id=query.admin_id,
            target_user_id=query.target_user_id,
            created_after=query.created_after,
            created_before=query.created_before,
        )

        total_pages = (
            math.ceil(total / query.page_size)
            if total > 0
            else 0
        )

        return AdminAuditLogListResponse(
            items=logs,
            total=total,
            page=query.page,
            page_size=query.page_size,
            total_pages=total_pages,
        )


