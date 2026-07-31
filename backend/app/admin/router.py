from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.admin.dashboard_service import AdminDashboardService
from app.admin.dependencies import (
    get_admin_audit_log_service,
    get_admin_dashboard_service,
    require_admin,
)
from app.admin.repository import (
    AdminAuditLogRepository,
    AdminUserRepository,
)
from app.admin.schemas import (
    AdminAuditLogListQuery,
    AdminAuditLogListResponse,
    AdminAuditLogResponse,
    AdminDashboardMetricsResponse,
    AdminDashboardTimeSeriesQuery,
    AdminDashboardTimeSeriesResponse,
    AdminUserActionRequest,
    AdminUserDetailResponse,
    AdminUserListQuery,
    AdminUserListResponse,
)
from app.admin.service import (
    AdminAuditLogService,
    AdminUserService,
)
from app.database.session import get_db
from app.users.models import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


def get_admin_user_service(
    db: Session = Depends(get_db),
) -> AdminUserService:
    user_repository = AdminUserRepository(
        db,
    )

    audit_repository = AdminAuditLogRepository(
        db,
    )

    return AdminUserService(
        repository=user_repository,
        audit_repository=audit_repository,
    )



@router.get(
    "/access",
)
def verify_admin_access(
    current_admin: User = Depends(require_admin),
) -> dict[str, str]:
    """
    Verify that the authenticated user has administrator access.
    """

    return {
        "message": "Administrator access granted.",
        "role": current_admin.role.value,
    }


@router.get(
    "/users",
    response_model=AdminUserListResponse,
)
def list_users(
    query: AdminUserListQuery = Depends(),
    _: User = Depends(require_admin),
    service: AdminUserService = Depends(
        get_admin_user_service,
    ),
) -> AdminUserListResponse:
    """
    List users for administrative management.
    """

    return service.list_users(
        query=query,
    )


@router.get(
    "/users/{user_id}",
    response_model=AdminUserDetailResponse,
)
def get_user(
    user_id: UUID,
    _: User = Depends(require_admin),
    service: AdminUserService = Depends(
        get_admin_user_service,
    ),
) -> AdminUserDetailResponse:
    """
    Return detailed information about a specific user.
    """

    return service.get_user(
        user_id=user_id,
    )


@router.post(
    "/users/{user_id}/suspend",
    response_model=AdminUserDetailResponse,
)
def suspend_user(
    user_id: UUID,
    payload: AdminUserActionRequest | None = None,
    current_admin: User = Depends(require_admin),
    service: AdminUserService = Depends(
        get_admin_user_service,
    ),
):
    return service.suspend_user(
        user_id=user_id,
        current_admin=current_admin,
        reason=payload.reason if payload else None,
    )

@router.post(
    "/users/{user_id}/reactivate",
    response_model=AdminUserDetailResponse,
)
def reactivate_user(
    user_id: UUID,
    payload: AdminUserActionRequest | None = None,
    current_admin: User = Depends(require_admin),
    service: AdminUserService = Depends(
        get_admin_user_service,
    ),
):
    return service.reactivate_user(
        user_id=user_id,
        current_admin=current_admin,
        reason=payload.reason if payload else None,
    )


@router.get(
    "/audit-logs",
    response_model=AdminAuditLogListResponse,
)
def list_audit_logs(
    query: AdminAuditLogListQuery = Depends(),
    _: User = Depends(require_admin),
    service: AdminAuditLogService = Depends(
        get_admin_audit_log_service,
    ),
) -> AdminAuditLogListResponse:
    """
    List administrative audit logs with optional filtering.
    """

    return service.list_filtered(
        query=query,
    )


@router.get(
    "/audit-logs/{audit_log_id}",
    response_model=AdminAuditLogResponse,
)
def get_audit_log(
    audit_log_id: UUID,
    _: User = Depends(require_admin),
    service: AdminAuditLogService = Depends(
        get_admin_audit_log_service,
    ),
) -> AdminAuditLogResponse:
    """
    Return a single administrative audit log.
    """

    return service.get_by_id(
        audit_log_id=audit_log_id,
    )


@router.get(
    "/users/{user_id}/audit-logs",
    response_model=AdminAuditLogListResponse,
)
def list_user_audit_logs(
    user_id: UUID,
    page: int = 1,
    page_size: int = 20,
    _: User = Depends(require_admin),
    service: AdminAuditLogService = Depends(
        get_admin_audit_log_service,
    ),
) -> AdminAuditLogListResponse:
    """
    Return administrative audit history for a target user.
    """

    return service.list_for_target_user(
        target_user_id=user_id,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/admins/{admin_id}/audit-logs",
    response_model=AdminAuditLogListResponse,
)
def list_admin_audit_logs(
    admin_id: UUID,
    page: int = 1,
    page_size: int = 20,
    _: User = Depends(require_admin),
    service: AdminAuditLogService = Depends(
        get_admin_audit_log_service,
    ),
) -> AdminAuditLogListResponse:
    """
    Return administrative audit history generated by a specific admin.
    """

    return service.list_for_admin(
        admin_id=admin_id,
        page=page,
        page_size=page_size,
    )



@router.get(
    "/metrics",
    response_model=AdminDashboardMetricsResponse,
)
def get_admin_dashboard_metrics(
    _: User = Depends(require_admin),
    service: AdminDashboardService = Depends(
        get_admin_dashboard_service,
    ),
) -> AdminDashboardMetricsResponse:
    """
    Return aggregated metrics for the administrative dashboard.
    """

    return service.get_metrics()


@router.get(
    "/metrics/timeseries",
    response_model=AdminDashboardTimeSeriesResponse,
)
def get_admin_dashboard_time_series(
    query: AdminDashboardTimeSeriesQuery = Depends(),
    _: User = Depends(require_admin),
    service: AdminDashboardService = Depends(
        get_admin_dashboard_service,
    ),
) -> AdminDashboardTimeSeriesResponse:
    """
    Return historical metrics for administrative dashboard charts.
    """

    return service.get_time_series(
        days=query.days,
    )