import pytest

from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)
from app.subscriptions.exceptions import PlanLimitNotFound
from app.subscriptions.models import PlanLimit
from app.subscriptions.repository import PlanLimitRepository
from app.subscriptions.service import SubscriptionService


def make_plan_limit(
    *,
    subscription_plan: SubscriptionPlan,
    feature: AIFeature,
    limit_value: int = 5,
    period: SubscriptionLimitPeriod = SubscriptionLimitPeriod.MONTHLY,
) -> PlanLimit:
    return PlanLimit(
        subscription_plan=subscription_plan,
        feature=feature,
        limit_value=limit_value,
        period=period,
    )


def test_get_plan_limit_returns_configured_limit(
    db_session,
):
    repository = PlanLimitRepository(db_session)
    service = SubscriptionService(repository)

    plan_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        limit_value=5,
    )

    repository.create(plan_limit)

    result = service.get_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
    )

    assert result.id == plan_limit.id
    assert result.limit_value == 5
    assert result.period == SubscriptionLimitPeriod.MONTHLY


def test_get_plan_limit_uses_monthly_period_by_default(
    db_session,
):
    repository = PlanLimitRepository(db_session)
    service = SubscriptionService(repository)

    plan_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.PRO,
        feature=AIFeature.ATS_OPTIMIZATION,
        period=SubscriptionLimitPeriod.MONTHLY,
        limit_value=50,
    )

    repository.create(plan_limit)

    result = service.get_plan_limit(
        subscription_plan=SubscriptionPlan.PRO,
        feature=AIFeature.ATS_OPTIMIZATION,
    )

    assert result.id == plan_limit.id
    assert result.period == SubscriptionLimitPeriod.MONTHLY


def test_get_plan_limit_raises_when_limit_is_not_configured(
    db_session,
):
    repository = PlanLimitRepository(db_session)
    service = SubscriptionService(repository)

    with pytest.raises(
        PlanLimitNotFound,
        match="No subscription limit is configured",
    ):
        service.get_plan_limit(
            subscription_plan=SubscriptionPlan.FREE,
            feature=AIFeature.RESUME_GENERATION,
        )


def test_get_plan_limit_error_contains_plan_feature_and_period(
    db_session,
):
    repository = PlanLimitRepository(db_session)
    service = SubscriptionService(repository)

    with pytest.raises(
        PlanLimitNotFound,
        match=(
            r"plan=free, "
            r"feature=resume_generation, "
            r"period=monthly"
        ),
    ):
        service.get_plan_limit(
            subscription_plan=SubscriptionPlan.FREE,
            feature=AIFeature.RESUME_GENERATION,
        )


def test_list_plan_limits_returns_all_limits_for_plan(
    db_session,
):
    repository = PlanLimitRepository(db_session)
    service = SubscriptionService(repository)

    resume_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        limit_value=5,
    )

    ats_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.ATS_OPTIMIZATION,
        limit_value=3,
    )

    pro_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.PRO,
        feature=AIFeature.RESUME_GENERATION,
        limit_value=50,
    )

    db_session.add_all(
        [
            resume_limit,
            ats_limit,
            pro_limit,
        ],
    )
    db_session.commit()

    results = service.list_plan_limits(
        subscription_plan=SubscriptionPlan.FREE,
    )

    assert len(results) == 2
    assert all(
        result.subscription_plan == SubscriptionPlan.FREE
        for result in results
    )

    assert {
        result.feature
        for result in results
    } == {
        AIFeature.RESUME_GENERATION,
        AIFeature.ATS_OPTIMIZATION,
    }


def test_list_plan_limits_returns_empty_list_when_no_limits_exist(
    db_session,
):
    repository = PlanLimitRepository(db_session)
    service = SubscriptionService(repository)

    results = service.list_plan_limits(
        subscription_plan=SubscriptionPlan.PRO,
    )

    assert results == []