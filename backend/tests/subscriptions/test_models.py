from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)
from app.subscriptions.models import PlanLimit
from app.subscriptions.repository import PlanLimitRepository


def make_plan_limit(
    *,
    subscription_plan: SubscriptionPlan = SubscriptionPlan.FREE,
    feature: AIFeature = AIFeature.RESUME_GENERATION,
    limit_value: int = 5,
    period: SubscriptionLimitPeriod = SubscriptionLimitPeriod.MONTHLY,
) -> PlanLimit:
    return PlanLimit(
        id=uuid4(),
        subscription_plan=subscription_plan,
        feature=feature,
        limit_value=limit_value,
        period=period,
    )


def test_seeded_plan_limit_exists(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    plan_limit = repository.get_by_plan_and_feature(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        period=SubscriptionLimitPeriod.MONTHLY,
    )

    assert plan_limit is not None
    assert plan_limit.subscription_plan == SubscriptionPlan.FREE
    assert plan_limit.feature == AIFeature.RESUME_GENERATION
    assert plan_limit.limit_value == 3
    assert plan_limit.period == SubscriptionLimitPeriod.MONTHLY


def test_plan_limit_persists_enum_values_correctly(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    persisted = repository.get_by_plan_and_feature(
        subscription_plan=SubscriptionPlan.PRO,
        feature=AIFeature.ATS_OPTIMIZATION,
        period=SubscriptionLimitPeriod.MONTHLY,
    )

    assert persisted is not None
    assert persisted.subscription_plan == SubscriptionPlan.PRO
    assert persisted.feature == AIFeature.ATS_OPTIMIZATION
    assert persisted.period == SubscriptionLimitPeriod.MONTHLY


def test_plan_limit_requires_unique_plan_feature_period_combination(
    db_session,
):
    duplicate = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
    )

    db_session.add(duplicate)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_seed_contains_expected_number_of_plan_limits(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    free = repository.list_by_plan(
        subscription_plan=SubscriptionPlan.FREE,
    )

    pro = repository.list_by_plan(
        subscription_plan=SubscriptionPlan.PRO,
    )

    assert len(free) == 4
    assert len(pro) == 4
