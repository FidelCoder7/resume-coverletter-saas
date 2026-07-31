from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.common.constants import (
    AccountStatus,
    AdminAuditAction,
    SubscriptionPlan,
    UserRole,
)


class AdminUserListItem(BaseModel):
    """
    User representation returned in the admin user list.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    email: EmailStr
    full_name: str
    role: UserRole
    subscription_plan: SubscriptionPlan
    status: AccountStatus
    is_email_verified: bool
    last_login_at: datetime | None
    created_at: datetime


class AdminUserDetailResponse(AdminUserListItem):
    """
    Detailed user representation returned to administrators.
    """

    updated_at: datetime
    deleted_at: datetime | None


class AdminUserListResponse(BaseModel):
    """
    Paginated response containing users visible to administrators.
    """

    items: list[AdminUserListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


class AdminUserListQuery(BaseModel):
    """
    Query parameters used when listing users in the admin dashboard.
    """

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )

    search: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    role: UserRole | None = None

    status: AccountStatus | None = None

    subscription_plan: SubscriptionPlan | None = None


class AdminAuditLogCreate(BaseModel):
    """
    Input required to record an administrative audit event.
    """

    target_user_id: UUID
    action: AdminAuditAction

    reason: str | None = Field(
        default=None,
        max_length=2000,
    )

    event_metadata: dict | None = None


class AdminAuditLogResponse(BaseModel):
    """
    Administrative audit log representation.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    admin_id: UUID
    target_user_id: UUID
    action: AdminAuditAction
    reason: str | None
    event_metadata: dict | None
    created_at: datetime


class AdminAuditLogListResponse(BaseModel):
    """
    Paginated administrative audit log response.
    """

    items: list[AdminAuditLogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AdminUserActionRequest(BaseModel):
    """
    Request body for an administrative user account action.
    """

    reason: str | None = Field(
        default=None,
        max_length=2000,
    )


class AdminAuditLogListQuery(BaseModel):
    """
    Query parameters used when listing administrative audit logs.
    """

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )

    action: AdminAuditAction | None = None

    admin_id: UUID | None = None

    target_user_id: UUID | None = None

    created_after: datetime | None = None

    created_before: datetime | None = None

    @model_validator(mode="after")
    def validate_date_range(self):
        """
        Ensure the audit log date range is logically valid.
        """

        if (
            self.created_after is not None
            and self.created_before is not None
            and self.created_after > self.created_before
        ):
            raise ValueError(
                "created_after must be earlier than or equal to "
                "created_before.",
            )

        return self


class AdminUserMetrics(BaseModel):
    """
    Aggregated user metrics for the administrative dashboard.
    """

    total_users: int
    active_users: int
    suspended_users: int
    deleted_users: int
    verified_users: int
    unverified_users: int
    total_admins: int


class AdminSubscriptionMetrics(BaseModel):
    """
    Subscription distribution and active subscription metrics.
    """

    free_users: int
    pro_users: int
    active_subscriptions: int
    

class AdminRevenueMetrics(BaseModel):
    """
    Revenue and payment transaction metrics for the dashboard.

    Revenue is calculated from completed payment transactions only.
    Currency totals are kept separate to avoid combining amounts
    denominated in different currencies.
    """

    total_transactions: int
    completed_transactions: int
    pending_transactions: int
    failed_transactions: int
    cancelled_transactions: int
    expired_transactions: int
    total_revenue_by_currency: dict[str, Decimal]

class AdminAIUsageMetrics(BaseModel):
    """
    Aggregated platform-wide AI usage metrics.
    """

    total_requests: int
    successful_requests: int
    failed_requests: int
    total_tokens: int
    estimated_cost: Decimal
    average_latency_ms: float | None

class AdminContentMetrics(BaseModel):
    """
    Aggregated resume and cover letter generation statistics.
    """

    total_resumes: int
    generated_resumes: int
    total_cover_letters: int


class AdminPlatformActivityMetrics(BaseModel):
    """
    Aggregated platform activity totals.
    """

    total_users: int
    total_resumes: int
    total_cover_letters: int
    total_ai_requests: int
    total_payment_transactions: int
    total_audit_logs: int

class AdminDashboardMetricsResponse(BaseModel):
    """
    Aggregated metrics displayed on the administrative dashboard.
    """

    users: AdminUserMetrics
    subscriptions: AdminSubscriptionMetrics
    revenue: AdminRevenueMetrics
    ai_usage: AdminAIUsageMetrics
    content: AdminContentMetrics
    platform: AdminPlatformActivityMetrics
    total_audit_logs: int

class AdminTimeSeriesPoint(BaseModel):
    """
    A single daily time-series data point.
    """

    date: date
    count: int


class AdminDashboardTimeSeriesResponse(BaseModel):
    """
    Historical metrics used for administrative dashboard charts.
    """

    days: int
    registrations: list[AdminTimeSeriesPoint]
    audit_activity: list[AdminTimeSeriesPoint]


class AdminDashboardTimeSeriesQuery(BaseModel):
    """
    Query parameters for dashboard historical metrics.
    """

    days: int = Field(
        default=30,
        ge=7,
        le=90,
    )