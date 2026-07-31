from app.admin.repository import (
    AdminAuditLogRepository,
    AdminContentRepository,
    AdminUserRepository,
)
from app.admin.schemas import (
    AdminAIUsageMetrics,
    AdminContentMetrics,
    AdminDashboardMetricsResponse,
    AdminDashboardTimeSeriesResponse,
    AdminPlatformActivityMetrics,
    AdminRevenueMetrics,
    AdminSubscriptionMetrics,
    AdminTimeSeriesPoint,
    AdminUserMetrics,
)
from app.ai_usage.repository import AIUsageRepository
from app.billing.repository import PaymentTransactionRepository
from app.common.constants import (
    AccountStatus,
    AIRequestStatus,
    PaymentStatus,
    SubscriptionPlan,
    UserRole,
)


class AdminDashboardService:
    """
    Business logic for administrative dashboard metrics.

    ```
    This service aggregates read-only metrics from the relevant
    application repositories and exposes dashboard-specific
    response models.
    """

    def __init__(
        self,
        user_repository: AdminUserRepository,
        audit_repository: AdminAuditLogRepository,
        payment_repository: PaymentTransactionRepository,
        ai_usage_repository: AIUsageRepository,
        content_repository: AdminContentRepository,
    ) -> None:
        self.user_repository = user_repository
        self.audit_repository = audit_repository
        self.payment_repository = payment_repository
        self.ai_usage_repository = ai_usage_repository
        self.content_repository = content_repository

    def get_metrics(
        self,
    ) -> AdminDashboardMetricsResponse:
        """
        Return aggregated metrics for the administrative dashboard.
        """

        # --------------------------------------------------------------
        # User Metrics
        # --------------------------------------------------------------

        total_users = self.user_repository.count_users()

        active_users = self.user_repository.count_users(
            status=AccountStatus.ACTIVE,
        )

        suspended_users = self.user_repository.count_users(
            status=AccountStatus.SUSPENDED,
        )

        deleted_users = self.user_repository.count_users(
            status=AccountStatus.DELETED,
        )

        verified_users = self.user_repository.count_users(
            email_verified=True,
        )

        unverified_users = self.user_repository.count_users(
            email_verified=False,
        )

        total_admins = self.user_repository.count_users(
            role=UserRole.ADMIN,
        )

        # --------------------------------------------------------------
        # Subscription Metrics
        # --------------------------------------------------------------

        subscription_counts = (
            self.user_repository.count_users_by_subscription_plan()
        )

        free_users = subscription_counts.get(
            SubscriptionPlan.FREE,
            0,
        )

        pro_users = subscription_counts.get(
            SubscriptionPlan.PRO,
            0,
        )

        active_subscriptions = pro_users

        # --------------------------------------------------------------
        # Revenue and Payment Metrics
        # --------------------------------------------------------------

        total_transactions = (
            self.payment_repository.count_all()
        )

        completed_transactions = (
            self.payment_repository.count_by_status(
                status=PaymentStatus.COMPLETED,
            )
        )

        pending_transactions = (
            self.payment_repository.count_by_status(
                status=PaymentStatus.PENDING,
            )
        )

        failed_transactions = (
            self.payment_repository.count_by_status(
                status=PaymentStatus.FAILED,
            )
        )

        cancelled_transactions = (
            self.payment_repository.count_by_status(
                status=PaymentStatus.CANCELLED,
            )
        )

        expired_transactions = (
            self.payment_repository.count_by_status(
                status=PaymentStatus.EXPIRED,
            )
        )

        total_revenue_by_currency = (
            self.payment_repository.sum_completed_amounts_by_currency()
        )

        # --------------------------------------------------------------
        # AI Usage Metrics
        # --------------------------------------------------------------

        total_ai_requests = (
            self.ai_usage_repository.count_all()
        )

        successful_ai_requests = (
            self.ai_usage_repository.count_by_status(
                status=AIRequestStatus.SUCCESS,
            )
        )

        failed_ai_requests = (
            self.ai_usage_repository.count_by_status(
                status=AIRequestStatus.FAILED,
            )
        )

        total_ai_tokens = (
            self.ai_usage_repository.sum_total_tokens()
        )

        estimated_ai_cost = (
            self.ai_usage_repository.sum_estimated_cost()
        )

        average_ai_latency = (
            self.ai_usage_repository.average_latency()
        )

        # --------------------------------------------------------------
        # Content Metrics
        # --------------------------------------------------------------

        total_resumes = (
            self.content_repository.count_resumes()
        )

        generated_resumes = (
            self.content_repository.count_generated_resumes()
        )

        total_cover_letters = (
            self.content_repository.count_cover_letters()
        )

        # --------------------------------------------------------------
        # Audit Metrics
        # --------------------------------------------------------------

        total_audit_logs = (
            self.audit_repository.count_all()
        )

        # --------------------------------------------------------------
        # Response
        # --------------------------------------------------------------

        return AdminDashboardMetricsResponse(
            users=AdminUserMetrics(
                total_users=total_users,
                active_users=active_users,
                suspended_users=suspended_users,
                deleted_users=deleted_users,
                verified_users=verified_users,
                unverified_users=unverified_users,
                total_admins=total_admins,
            ),
            subscriptions=AdminSubscriptionMetrics(
                free_users=free_users,
                pro_users=pro_users,
                active_subscriptions=active_subscriptions,
            ),
            revenue=AdminRevenueMetrics(
                total_transactions=total_transactions,
                completed_transactions=completed_transactions,
                pending_transactions=pending_transactions,
                failed_transactions=failed_transactions,
                cancelled_transactions=cancelled_transactions,
                expired_transactions=expired_transactions,
                total_revenue_by_currency=total_revenue_by_currency,
            ),
            ai_usage=AdminAIUsageMetrics(
                total_requests=total_ai_requests,
                successful_requests=successful_ai_requests,
                failed_requests=failed_ai_requests,
                total_tokens=total_ai_tokens,
                estimated_cost=estimated_ai_cost,
                average_latency_ms=average_ai_latency,
            ),
            content=AdminContentMetrics(
                total_resumes=total_resumes,
                generated_resumes=generated_resumes,
                total_cover_letters=total_cover_letters,
            ),
            platform=AdminPlatformActivityMetrics(
                total_users=total_users,
                total_resumes=total_resumes,
                total_cover_letters=total_cover_letters,
                total_ai_requests=total_ai_requests,
                total_payment_transactions=total_transactions,
                total_audit_logs=total_audit_logs,
            ),
            total_audit_logs=total_audit_logs,
        )

    def get_time_series(
        self,
        *,
        days: int,
    ) -> AdminDashboardTimeSeriesResponse:
        """
        Return historical dashboard metrics grouped by day.
        """

        from datetime import UTC, datetime, timedelta

        end_date = datetime.now(
            UTC,
        ).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        ) + timedelta(
            days=1,
        )

        start_date = end_date - timedelta(
            days=days,
        )

        registration_results = (
            self.user_repository.count_registrations_by_day(
                start_date=start_date,
                end_date=end_date,
            )
        )

        audit_results = (
            self.audit_repository.count_audit_activity_by_day(
                start_date=start_date,
                end_date=end_date,
            )
        )

        registration_counts = dict(
            registration_results,
        )

        audit_counts = dict(
            audit_results,
        )

        registration_series = []
        audit_series = []

        for offset in range(days):
            current_date = (
                start_date.date()
                + timedelta(
                    days=offset,
                )
            )

            registration_series.append(
                AdminTimeSeriesPoint(
                    date=current_date,
                    count=registration_counts.get(
                        current_date,
                        0,
                    ),
                )
            )

            audit_series.append(
                AdminTimeSeriesPoint(
                    date=current_date,
                    count=audit_counts.get(
                        current_date,
                        0,
                    ),
                )
            )

        return AdminDashboardTimeSeriesResponse(
            days=days,
            registrations=registration_series,
            audit_activity=audit_series,
        )
