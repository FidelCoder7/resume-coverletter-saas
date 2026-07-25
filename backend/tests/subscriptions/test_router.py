from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)
from app.subscriptions.models import PlanLimit


def create_plan_limit(
    db_session,
    *,
    subscription_plan: SubscriptionPlan,
    feature: AIFeature,
    limit_value: int,
    period: SubscriptionLimitPeriod = SubscriptionLimitPeriod.MONTHLY,
) -> PlanLimit:
    plan_limit = PlanLimit(
        subscription_plan=subscription_plan,
        feature=feature,
        limit_value=limit_value,
        period=period,
    )

    db_session.add(plan_limit)
    db_session.commit()
    db_session.refresh(plan_limit)

    return plan_limit


def test_get_my_subscription_limits_requires_authentication(
    client,
):
    response = client.get(
        "/api/subscriptions/limits",
    )

    assert response.status_code == 401


def test_get_my_subscription_limits_returns_free_plan_limits(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    create_plan_limit(
        db_session,
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        limit_value=5,
    )

    create_plan_limit(
        db_session,
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.COVER_LETTER_GENERATION,
        limit_value=5,
    )

    create_plan_limit(
        db_session,
        subscription_plan=SubscriptionPlan.PRO,
        feature=AIFeature.RESUME_GENERATION,
        limit_value=50,
    )

    response = client.get(
        "/api/subscriptions/limits",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["subscription_plan"] == SubscriptionPlan.FREE.value
    assert len(data["limits"]) == 2

    assert {
        item["feature"]
        for item in data["limits"]
    } == {
        AIFeature.RESUME_GENERATION.value,
        AIFeature.COVER_LETTER_GENERATION.value,
    }

    assert all(
        item["subscription_plan"] == SubscriptionPlan.FREE.value
        for item in data["limits"]
    )

    assert all(
        item["period"] == SubscriptionLimitPeriod.MONTHLY.value
        for item in data["limits"]
    )


def test_get_my_subscription_limits_returns_pro_plan_limits(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    user.subscription_plan = SubscriptionPlan.PRO
    db_session.commit()
    db_session.refresh(user)

    create_plan_limit(
        db_session,
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
        limit_value=5,
    )

    create_plan_limit(
        db_session,
        subscription_plan=SubscriptionPlan.PRO,
        feature=AIFeature.RESUME_GENERATION,
        limit_value=50,
    )

    create_plan_limit(
        db_session,
        subscription_plan=SubscriptionPlan.PRO,
        feature=AIFeature.ATS_OPTIMIZATION,
        limit_value=25,
    )

    response = client.get(
        "/api/subscriptions/limits",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["subscription_plan"] == SubscriptionPlan.PRO.value
    assert len(data["limits"]) == 2

    assert {
        item["feature"]
        for item in data["limits"]
    } == {
        AIFeature.RESUME_GENERATION.value,
        AIFeature.ATS_OPTIMIZATION.value,
    }

    assert all(
        item["subscription_plan"] == SubscriptionPlan.PRO.value
        for item in data["limits"]
    )


def test_get_my_subscription_limits_returns_empty_limits_when_none_configured(
    authenticated_client,
):
    client, user = authenticated_client

    response = client.get(
        "/api/subscriptions/limits",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["subscription_plan"] == SubscriptionPlan.FREE.value
    assert data["limits"] == []
