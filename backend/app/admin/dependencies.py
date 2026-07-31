"""Dependencies for administrative authorization."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.admin.dashboard_service import AdminDashboardService
from app.admin.exceptions import AdminAccessDenied
from app.admin.repository import (
    AdminAuditLogRepository,
    AdminContentRepository,
    AdminUserRepository,
)
from app.admin.service import AdminAuditLogService
from app.ai_usage.repository import AIUsageRepository
from app.auth.dependencies import get_current_user
from app.billing.repository import PaymentTransactionRepository
from app.common.constants import UserRole
from app.database.session import get_db
from app.users.models import User


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Require the authenticated user to have administrator privileges.

    Args:
        current_user: The currently authenticated user.

    Returns:
        The authenticated administrator.

    Raises:
        AdminAccessDenied: If the authenticated user is not an administrator.
    """

    if current_user.role != UserRole.ADMIN:
        raise AdminAccessDenied(
            "Administrator access required.",
        )

    return current_user



def get_admin_audit_log_service(
    db: Session = Depends(get_db),
) -> AdminAuditLogService:
    """
    Build the administrative audit log service.
    """

    return AdminAuditLogService(
        repository=AdminAuditLogRepository(
            db,
        ),
    )


def get_admin_dashboard_service(
    db: Session = Depends(get_db),
) -> AdminDashboardService:
    """
    Provide the administrative dashboard service.
    """

    user_repository = AdminUserRepository(
        db,
    )

    audit_repository = AdminAuditLogRepository(
        db,
    )

    payment_repository = PaymentTransactionRepository( 
        db, 
    )
     
    ai_usage_repository = AIUsageRepository( 
        db, 
    )

    content_repository = AdminContentRepository( 
        db, 
    )

    return AdminDashboardService(
        user_repository=user_repository,
        audit_repository=audit_repository,
        payment_repository=payment_repository, 
        ai_usage_repository=ai_usage_repository, 
        content_repository=content_repository,
    )