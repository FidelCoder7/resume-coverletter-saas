from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)
from app.subscriptions.models import PlanLimit


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


def test_plan_limit_can_be_created(
    db_session,
):
    plan_limit = make_plan_limit()

    db_session.add(plan_limit)
    db_session.commit()
    db_session.refresh(plan_limit)

    assert plan_limit.id is not None
    assert plan_limit.subscription_plan == SubscriptionPlan.FREE
    assert plan_limit.feature == AIFeature.RESUME_GENERATION
    assert plan_limit.limit_value == 5
    assert plan_limit.period == SubscriptionLimitPeriod.MONTHLY


def test_plan_limit_persists_enum_values_correctly(
    db_session,
):
    plan_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.PRO,
        feature=AIFeature.ATS_OPTIMIZATION,
    )

    db_session.add(plan_limit)
    db_session.commit()
    db_session.expire_all()

    persisted = db_session.get(
        PlanLimit,
        plan_limit.id,
    )

    assert persisted is not None
    assert persisted.subscription_plan == SubscriptionPlan.PRO
    assert persisted.feature == AIFeature.ATS_OPTIMIZATION
    assert persisted.period == SubscriptionLimitPeriod.MONTHLY


def test_plan_limit_requires_unique_plan_feature_period_combination(
    db_session,
):
    first_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        period=SubscriptionLimitPeriod.MONTHLY,
    )

    second_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        period=SubscriptionLimitPeriod.MONTHLY,
    )

    db_session.add(first_limit)
    db_session.commit()

    db_session.add(second_limit)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_plan_limit_allows_same_feature_for_different_plans(
    db_session,
):
    free_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
    )

    pro_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.PRO,
        feature=AIFeature.RESUME_GENERATION,
    )

    db_session.add_all(
        [
            free_limit,
            pro_limit,
        ],
    )

    db_session.commit()

    assert free_limit.id != pro_limit.id
    assert free_limit.subscription_plan == SubscriptionPlan.FREE
    assert pro_limit.subscription_plan == SubscriptionPlan.PRO


def test_plan_limit_allows_different_features_for_same_plan(
    db_session,
):
    resume_limit = make_plan_limit(
        feature=AIFeature.RESUME_GENERATION,
    )

    ats_limit = make_plan_limit(
        feature=AIFeature.ATS_OPTIMIZATION,
    )

    db_session.add_all(
        [
            resume_limit,
            ats_limit,
        ],
    )

    db_session.commit()

    assert resume_limit.feature != ats_limit.feature