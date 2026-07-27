from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)


class PlanLimitResponse(BaseModel):
    """
    API representation of a subscription plan limit.
    """

    id: UUID
    subscription_plan: SubscriptionPlan
    feature: AIFeature
    limit_value: int
    period: SubscriptionLimitPeriod

    model_config = ConfigDict(
        from_attributes=True,
    )


class PlanLimitListResponse(BaseModel):
    """
    Response containing the configured limits for a subscription plan.
    """

    subscription_plan: SubscriptionPlan
    limits: list[PlanLimitResponse]


class UsageStatusResponse(BaseModel):
    """
    Current usage and remaining quota for one AI feature.
    """

    subscription_plan: SubscriptionPlan
    feature: AIFeature
    limit_value: int
    usage: int
    remaining: int
    period: SubscriptionLimitPeriod
    period_start: datetime
    period_end: datetime


class FeatureUsageResponse(BaseModel):
    """
    Usage summary for one AI feature.

    Used when returning usage for all configured features.
    """

    feature: AIFeature
    limit_value: int
    usage: int
    remaining: int
    period: SubscriptionLimitPeriod


class UsageSummaryResponse(BaseModel):
    """
    Complete AI usage summary for the authenticated user.
    """

    subscription_plan: SubscriptionPlan
    period_start: datetime
    period_end: datetime
    features: list[FeatureUsageResponse]
