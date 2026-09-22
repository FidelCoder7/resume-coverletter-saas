import pytest


def test_admin_can_get_subscription_analytics(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/analytics/subscriptions",
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_users" in data
    assert "free_users" in data
    assert "pro_users" in data
    assert "active_subscriptions" in data

    assert data["total_users"] >= 1
    assert data["free_users"] >= 0
    assert data["pro_users"] >= 0
    assert data["active_subscriptions"] >= 0


def test_non_admin_cannot_get_subscription_analytics(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        "/api/admin/analytics/subscriptions",
    )

    assert response.status_code == 403


def test_unauthenticated_user_cannot_get_subscription_analytics(
    client,
):
    response = client.get(
        "/api/admin/analytics/subscriptions",
    )

    assert response.status_code == 401


def test_admin_can_get_payment_analytics(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/analytics/payments",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["days"] == 30

    assert "total_transactions" in data
    assert "completed_transactions" in data
    assert "pending_transactions" in data
    assert "failed_transactions" in data
    assert "cancelled_transactions" in data
    assert "expired_transactions" in data
    assert "total_revenue_by_currency" in data
    assert "transactions_by_plan" in data
    assert "transactions_by_type" in data
    assert "transactions_by_provider" in data
    assert "transactions_by_payment_method" in data
    assert "transaction_activity" in data
    assert "revenue_activity" in data


def test_payment_analytics_supports_seven_day_period(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/analytics/payments",
        params={
            "days": 7,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["days"] == 7
    assert len(data["transaction_activity"]) == 7

    for point in data["transaction_activity"]:
        assert "date" in point
        assert "count" in point


def test_payment_analytics_supports_ninety_day_period(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/analytics/payments",
        params={
            "days": 90,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["days"] == 90
    assert len(data["transaction_activity"]) == 90


@pytest.mark.parametrize(
    "days",
    [
        6,
        91,
    ],
)
def test_payment_analytics_rejects_invalid_period(
    admin_client,
    days,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/analytics/payments",
        params={
            "days": days,
        },
    )

    assert response.status_code == 422


def test_non_admin_cannot_get_payment_analytics(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        "/api/admin/analytics/payments",
    )

    assert response.status_code == 403


def test_unauthenticated_user_cannot_get_payment_analytics(
    client,
):
    response = client.get(
        "/api/admin/analytics/payments",
    )

    assert response.status_code == 401


def test_admin_payment_analytics_returns_zero_for_empty_period(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/analytics/payments",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_transactions"] == 0
    assert data["completed_transactions"] == 0
    assert data["pending_transactions"] == 0
    assert data["failed_transactions"] == 0
    assert data["cancelled_transactions"] == 0
    assert data["expired_transactions"] == 0
    assert data["total_revenue_by_currency"] == {}

    assert len(data["transaction_activity"]) == 30

    for point in data["transaction_activity"]:
        assert point["count"] == 0

    assert data["revenue_activity"] == {}


def test_admin_can_get_ai_analytics(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/analytics/ai",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["days"] == 30

    assert "total_requests" in data
    assert "successful_requests" in data
    assert "failed_requests" in data
    assert "cancelled_requests" in data
    assert "total_tokens" in data
    assert "estimated_cost" in data
    assert "average_latency_ms" in data
    assert "requests_by_feature" in data
    assert "requests_by_status" in data
    assert "tokens_by_feature" in data
    assert "request_activity" in data
    assert "token_activity" in data
    assert "cost_activity" in data


def test_ai_analytics_supports_seven_day_period(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/analytics/ai",
        params={
            "days": 7,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["days"] == 7
    assert len(data["request_activity"]) == 7
    assert len(data["token_activity"]) == 7
    assert len(data["cost_activity"]) == 7


def test_ai_analytics_supports_ninety_day_period(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/analytics/ai",
        params={
            "days": 90,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["days"] == 90
    assert len(data["request_activity"]) == 90
    assert len(data["token_activity"]) == 90
    assert len(data["cost_activity"]) == 90


@pytest.mark.parametrize(
    "days",
    [
        6,
        91,
    ],
)
def test_ai_analytics_rejects_invalid_period(
    admin_client,
    days,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/analytics/ai",
        params={
            "days": days,
        },
    )

    assert response.status_code == 422


def test_non_admin_cannot_get_ai_analytics(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        "/api/admin/analytics/ai",
    )

    assert response.status_code == 403


def test_unauthenticated_user_cannot_get_ai_analytics(
    client,
):
    response = client.get(
        "/api/admin/analytics/ai",
    )

    assert response.status_code == 401


def test_admin_ai_analytics_returns_zero_for_empty_period(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/analytics/ai",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_requests"] == 0
    assert data["successful_requests"] == 0
    assert data["failed_requests"] == 0
    assert data["cancelled_requests"] == 0
    assert data["total_tokens"] == 0
    assert data["estimated_cost"] == "0"
    assert data["average_latency_ms"] is None

    assert data["requests_by_feature"] == {}
    assert data["requests_by_status"] == {}
    assert data["tokens_by_feature"] == {}

    assert len(data["request_activity"]) == 30
    assert len(data["token_activity"]) == 30
    assert len(data["cost_activity"]) == 30

    for point in data["request_activity"]:
        assert point["count"] == 0

    for point in data["token_activity"]:
        assert point["count"] == 0

    for point in data["cost_activity"]:
        assert point["amount"] == "0"