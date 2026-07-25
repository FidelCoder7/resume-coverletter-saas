from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)
from app.subscriptions.models import PlanLimit


class PlanLimitRepository:
    """
    Repository responsible for subscription plan limit persistence.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def get_by_id(
        self,
        limit_id: UUID,
    ) -> PlanLimit | None:
        """
        Retrieve a plan limit by identifier.
        """

        return self.db.get(
            PlanLimit,
            limit_id,
        )

    def get_by_plan_and_feature(
        self,
        *,
        subscription_plan: SubscriptionPlan,
        feature: AIFeature,
        period: SubscriptionLimitPeriod,
    ) -> PlanLimit | None:
        """
        Retrieve the configured limit for a plan, feature, and period.
        """

        statement = select(
            PlanLimit,
        ).where(
            PlanLimit.subscription_plan == subscription_plan,
            PlanLimit.feature == feature,
            PlanLimit.period == period,
        )

        return self.db.scalar(
            statement,
        )

    def list_by_plan(
        self,
        *,
        subscription_plan: SubscriptionPlan,
    ) -> list[PlanLimit]:
        """
        Return all configured limits for a subscription plan.
        """

        statement = (
            select(
                PlanLimit,
            )
            .where(
                PlanLimit.subscription_plan == subscription_plan,
            )
            .order_by(
                PlanLimit.feature,
            )
        )

        return list(
            self.db.scalars(
                statement,
            )
        )

    def create(
        self,
        plan_limit: PlanLimit,
    ) -> PlanLimit:
        """
        Persist a new plan limit.
        """

        self.db.add(
            plan_limit,
        )

        self.db.commit()

        self.db.refresh(
            plan_limit,
        )

        return plan_limit