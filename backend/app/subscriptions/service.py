from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)
from app.subscriptions.exceptions import PlanLimitNotFound
from app.subscriptions.models import PlanLimit
from app.subscriptions.repository import PlanLimitRepository


class SubscriptionService:
    """
    Business logic for subscription plans and plan limits.

    This service defines subscription policy access but does not enforce
    usage quotas. Usage enforcement is introduced in a later phase.
    """

    def __init__(
        self,
        repository: PlanLimitRepository,
    ) -> None:
        self.repository = repository

    def get_plan_limit(
        self,
        *,
        subscription_plan: SubscriptionPlan,
        feature: AIFeature,
        period: SubscriptionLimitPeriod = SubscriptionLimitPeriod.MONTHLY,
    ) -> PlanLimit:
        """
        Return the configured limit for a subscription plan and AI feature.
        """

        plan_limit = self.repository.get_by_plan_and_feature(
            subscription_plan=subscription_plan,
            feature=feature,
            period=period,
        )

        if plan_limit is None:
            raise PlanLimitNotFound(
                "No subscription limit is configured for "
                f"plan={subscription_plan.value}, "
                f"feature={feature.value}, "
                f"period={period.value}.",
            )

        return plan_limit

    def list_plan_limits(
        self,
        *,
        subscription_plan: SubscriptionPlan,
    ) -> list[PlanLimit]:
        """
        Return all configured limits for a subscription plan.
        """

        return self.repository.list_by_plan(
            subscription_plan=subscription_plan,
        )