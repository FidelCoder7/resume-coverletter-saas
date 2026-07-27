from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)


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

    response = client.get(
        "/api/subscriptions/limits",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["subscription_plan"] == SubscriptionPlan.FREE.value
    assert len(data["limits"]) == 4

    assert {item["feature"] for item in data["limits"]} == {
        AIFeature.RESUME_GENERATION.value,
        AIFeature.COVER_LETTER_GENERATION.value,
        AIFeature.COVER_LETTER_REGENERATION.value,
        AIFeature.ATS_OPTIMIZATION.value,
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

    response = client.get(
        "/api/subscriptions/limits",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["subscription_plan"] == SubscriptionPlan.PRO.value
    assert len(data["limits"]) == 4

    assert {item["feature"] for item in data["limits"]} == {
        AIFeature.RESUME_GENERATION.value,
        AIFeature.ATS_OPTIMIZATION.value,
        AIFeature.COVER_LETTER_GENERATION.value,
        AIFeature.COVER_LETTER_REGENERATION.value,
    }

    assert all(
        item["subscription_plan"] == SubscriptionPlan.PRO.value
        for item in data["limits"]
    )
