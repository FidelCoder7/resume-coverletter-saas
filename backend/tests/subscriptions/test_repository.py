from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)
from app.subscriptions.repository import PlanLimitRepository


def test_create_persists_plan_limit(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    result = repository.get_by_plan_and_feature(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        period=SubscriptionLimitPeriod.MONTHLY,
    )

    assert result is not None
    assert result.subscription_plan == SubscriptionPlan.FREE
    assert result.feature == AIFeature.RESUME_GENERATION
    assert result.limit_value == 3


def test_get_by_id_returns_plan_limit(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    existing = repository.get_by_plan_and_feature(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        period=SubscriptionLimitPeriod.MONTHLY,
    )

    result = repository.get_by_id(existing.id)

    assert result is not None
    assert result.id == existing.id
    assert result.subscription_plan == SubscriptionPlan.FREE
    assert result.feature == AIFeature.RESUME_GENERATION


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

    result = repository.get_by_plan_and_feature(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        period=SubscriptionLimitPeriod.MONTHLY,
    )

    assert result is not None
    assert result.limit_value == 3


def test_list_by_plan_returns_only_limits_for_requested_plan(
    db_session,
):
    repository = PlanLimitRepository(db_session)

    results = repository.list_by_plan(
        subscription_plan=SubscriptionPlan.FREE,
    )

    assert len(results) == 4

    assert {item.feature for item in results} == {
        AIFeature.RESUME_GENERATION,
        AIFeature.COVER_LETTER_GENERATION,
        AIFeature.COVER_LETTER_REGENERATION,
        AIFeature.ATS_OPTIMIZATION,
    }
