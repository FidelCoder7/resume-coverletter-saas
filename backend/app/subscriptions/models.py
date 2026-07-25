from typing import TYPE_CHECKING

from sqlalchemy import Index, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)
from app.database.base import Base
from app.database.enums import (
    ai_feature_enum,
    subscription_limit_period_enum,
    subscription_plan_enum,
)

if TYPE_CHECKING:
    pass


class PlanLimit(Base):
    """
    Defines the usage limit for an AI feature under a subscription plan.

    Plan limits are stored as data so subscription policies can be changed
    without modifying AI business logic.
    """

    __tablename__ = "plan_limits"

    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        subscription_plan_enum,
        nullable=False,
    )

    feature: Mapped[AIFeature] = mapped_column(
        ai_feature_enum,
        nullable=False,
    )

    limit_value: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    period: Mapped[SubscriptionLimitPeriod] = mapped_column(
        subscription_limit_period_enum,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "subscription_plan",
            "feature",
            "period",
            name="uq_plan_limit_plan_feature_period",
        ),
        Index(
            "ix_plan_limits_subscription_plan",
            "subscription_plan",
        ),
        Index(
            "ix_plan_limits_feature",
            "feature",
        ),
        Index(
            "ix_plan_limits_plan_period",
            "subscription_plan",
            "period",
        ),
    )