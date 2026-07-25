
from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)
from app.subscriptions.models import PlanLimit
from app.subscriptions.repository import PlanLimitRepository


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


def test_create_persists_plan_limit(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    plan_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        limit_value=5,
    )

    result = repository.create(plan_limit)

    assert result.id is not None
    assert result.subscription_plan == SubscriptionPlan.FREE
    assert result.feature == AIFeature.RESUME_GENERATION
    assert result.limit_value == 5
    assert result.period == SubscriptionLimitPeriod.MONTHLY


def test_get_by_id_returns_plan_limit(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    plan_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
    )

    created = repository.create(plan_limit)

    result = repository.get_by_id(
        created.id,
    )

    assert result is not None
    assert result.id == created.id
    assert result.subscription_plan == SubscriptionPlan.FREE
    assert result.feature == AIFeature.RESUME_GENERATION
    assert result.limit_value == created.limit_value
    assert result.period == created.period

def test_get_by_id_returns_none_for_unknown_id(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    result = repository.get_by_id(
        plan_limit_id := __import__("uuid").uuid4(),
    )

    assert result is None


def test_get_by_plan_and_feature_returns_matching_limit(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    plan_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        limit_value=5,
    )

    repository.create(plan_limit)

    result = repository.get_by_plan_and_feature(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        period=SubscriptionLimitPeriod.MONTHLY,
    )

    assert result is not None
    assert result.id == plan_limit.id
    assert result.limit_value == 5


def test_get_by_plan_and_feature_returns_none_for_wrong_plan(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    plan_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
    )

    repository.create(plan_limit)

    result = repository.get_by_plan_and_feature(
        subscription_plan=SubscriptionPlan.PRO,
        feature=AIFeature.RESUME_GENERATION,
        period=SubscriptionLimitPeriod.MONTHLY,
    )

    assert result is None


def test_get_by_plan_and_feature_returns_none_for_wrong_feature(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    plan_limit = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
    )

    repository.create(plan_limit)

    result = repository.get_by_plan_and_feature(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.ATS_OPTIMIZATION,
        period=SubscriptionLimitPeriod.MONTHLY,
    )

    assert result is None


def test_list_by_plan_returns_only_limits_for_requested_plan(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    free_resume = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        limit_value=5,
    )

    free_ats = make_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.ATS_OPTIMIZATION,
        limit_value=3,
    )

    pro_resume = make_plan_limit(
        subscription_plan=SubscriptionPlan.PRO,
        feature=AIFeature.RESUME_GENERATION,
        limit_value=50,
    )

    db_session.add_all(
        [
            free_resume,
            free_ats,
            pro_resume,
        ],
    )
    db_session.commit()

    results = repository.list_by_plan(
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


def test_list_by_plan_returns_empty_list_when_no_limits_exist(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    results = repository.list_by_plan(
        subscription_plan=SubscriptionPlan.PRO,
    )

    assert results == []