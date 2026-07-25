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