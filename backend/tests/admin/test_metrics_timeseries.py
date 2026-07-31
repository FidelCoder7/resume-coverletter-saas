


def test_admin_can_get_dashboard_time_series(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/metrics/timeseries",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["days"] == 30
    assert len(data["registrations"]) == 30
    assert len(data["audit_activity"]) == 30


def test_admin_can_request_seven_day_time_series(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/metrics/timeseries",
        params={
            "days": 7,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["days"] == 7
    assert len(data["registrations"]) == 7
    assert len(data["audit_activity"]) == 7


def test_admin_can_request_ninety_day_time_series(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/metrics/timeseries",
        params={
            "days": 90,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["days"] == 90
    assert len(data["registrations"]) == 90
    assert len(data["audit_activity"]) == 90


def test_admin_dashboard_time_series_rejects_invalid_days(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/metrics/timeseries",
        params={
            "days": 5,
        },
    )

    assert response.status_code == 422


def test_admin_dashboard_time_series_rejects_days_above_maximum(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/metrics/timeseries",
        params={
            "days": 91,
        },
    )

    assert response.status_code == 422


def test_non_admin_cannot_get_dashboard_time_series(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        "/api/admin/metrics/timeseries",
    )

    assert response.status_code == 403


def test_unauthenticated_user_cannot_get_dashboard_time_series(
    client,
):
    response = client.get(
        "/api/admin/metrics/timeseries",
    )

    assert response.status_code == 401


def test_dashboard_time_series_includes_zero_activity_days(
    admin_client,
):
    client, _ = admin_client

    response = client.get(
        "/api/admin/metrics/timeseries",
        params={
            "days": 7,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["registrations"]) == 7
    assert len(data["audit_activity"]) == 7

    for point in data["registrations"]:
        assert "date" in point
        assert "count" in point
        assert point["count"] >= 0

    for point in data["audit_activity"]:
        assert "date" in point
        assert "count" in point
        assert point["count"] >= 0