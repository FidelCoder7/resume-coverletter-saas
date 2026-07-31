from app.admin.dashboard_service import AdminDashboardService
from app.admin.repository import (
    AdminAuditLogRepository,
    AdminContentRepository,
    AdminUserRepository,
)
from app.ai_usage.repository import AIUsageRepository
from app.billing.repository import PaymentTransactionRepository


def test_dashboard_service_returns_metrics(
    db_session,
):
    user_repository = AdminUserRepository(
        db_session,
    )

    audit_repository = AdminAuditLogRepository(
        db_session,
    )

    payment_repository = PaymentTransactionRepository(
            db_session,
    )

    ai_usage_repository = AIUsageRepository(
        db_session,
    )

    content_repository = AdminContentRepository(
        db_session,
    )
    

    service = AdminDashboardService(
        user_repository=user_repository,
        audit_repository=audit_repository,
        payment_repository=payment_repository,
        ai_usage_repository=ai_usage_repository,
        content_repository=content_repository,
    )

    

    result = service.get_metrics()

    assert result.users.total_users >= 0
    assert result.users.active_users >= 0
    assert result.users.suspended_users >= 0
    assert result.users.deleted_users >= 0
    assert result.users.verified_users >= 0
    assert result.users.unverified_users >= 0
    assert result.users.total_admins >= 0

    assert result.subscriptions.free_users >= 0
    assert result.subscriptions.pro_users >= 0
    assert result.subscriptions.active_subscriptions >= 0 

    assert result.revenue.total_transactions >= 0 
    assert result.revenue.completed_transactions >= 0 
    assert result.revenue.pending_transactions >= 0 
    assert result.revenue.failed_transactions >= 0 
    assert result.revenue.cancelled_transactions >= 0 
    assert result.revenue.expired_transactions >= 0 

    for amount in result.revenue.total_revenue_by_currency.values(): 
        assert amount >= 0 

    assert result.ai_usage.total_requests >= 0 
    assert result.ai_usage.successful_requests >= 0 
    assert result.ai_usage.failed_requests >= 0 
    assert result.ai_usage.total_tokens >= 0 
    assert result.ai_usage.estimated_cost >= 0 

    if result.ai_usage.average_latency_ms is not None: 
        assert result.ai_usage.average_latency_ms >= 0 

    assert result.content.total_resumes >= 0 
    assert result.content.generated_resumes >= 0 
    assert result.content.total_cover_letters >= 0 

    assert result.platform.total_users >= 0 
    assert result.platform.total_resumes >= 0 
    assert result.platform.total_cover_letters >= 0 
    assert result.platform.total_ai_requests >= 0 
    assert result.platform.total_payment_transactions >= 0 
    assert result.platform.total_audit_logs >= 0
    

    assert result.total_audit_logs >= 0


def test_dashboard_service_returns_time_series(
    db_session,
):
    user_repository = AdminUserRepository(
        db_session,
    )

    audit_repository = AdminAuditLogRepository(
        db_session,
    )

    payment_repository = PaymentTransactionRepository(
        db_session,
    )

    ai_usage_repository = AIUsageRepository(
        db_session,
    )

    content_repository = AdminContentRepository(
        db_session,
    )

    service = AdminDashboardService(
        user_repository=user_repository,
        audit_repository=audit_repository,
        payment_repository=payment_repository,
        ai_usage_repository=ai_usage_repository,
        content_repository=content_repository,
    )

    result = service.get_time_series(
        days=7,
    )

    assert result.days == 7
    assert len(result.registrations) == 7
    assert len(result.audit_activity) == 7

    for point in result.registrations:
        assert point.count >= 0

    for point in result.audit_activity:
        assert point.count >= 0