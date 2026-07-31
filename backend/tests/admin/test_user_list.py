from app.common.constants import (
    AccountStatus,
    SubscriptionPlan,
    UserRole,
)
from tests.factories.user_factory import create_user


def test_admin_can_list_users(
    client,
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
        full_name="Admin User",
    )

    create_user(
        db_session,
        full_name="Regular User",
    )

    response = client.get(
        "/api/admin/users",
        headers={
            "Authorization": "Bearer "
            + client.post(
                "/auth/login",
                data={
                    "username": admin.email,
                    "password": "Password123!",
                },
            ).json()["access_token"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total_pages"] == 1
    assert len(data["items"]) == 2


def test_regular_user_cannot_list_users(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        "/api/admin/users",
    )

    assert response.status_code == 403


def test_admin_can_filter_users_by_role(
    client,
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    create_user(
        db_session,
        role=UserRole.USER,
    )

    create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": admin.email,
            "password": "Password123!",
        },
    )

    client.headers.update(
        {
            "Authorization": (f"Bearer {login_response.json()['access_token']}"),
        }
    )

    response = client.get(
        "/api/admin/users",
        params={
            "role": UserRole.ADMIN.value,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2

    assert all(item["role"] == UserRole.ADMIN.value for item in data["items"])


def test_admin_can_search_users(
    client,
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    create_user(
        db_session,
        full_name="Alice Johnson",
        email="alice@example.com",
    )

    create_user(
        db_session,
        full_name="Bob Smith",
        email="bob@example.com",
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": admin.email,
            "password": "Password123!",
        },
    )

    client.headers.update(
        {
            "Authorization": (f"Bearer {login_response.json()['access_token']}"),
        }
    )

    response = client.get(
        "/api/admin/users",
        params={
            "search": "Alice",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["email"] == "alice@example.com"


def test_admin_can_filter_by_subscription_plan(
    client,
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    create_user(
        db_session,
        subscription_plan=SubscriptionPlan.PRO,
    )

    create_user(
        db_session,
        subscription_plan=SubscriptionPlan.FREE,
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": admin.email,
            "password": "Password123!",
        },
    )

    client.headers.update(
        {
            "Authorization": (f"Bearer {login_response.json()['access_token']}"),
        }
    )

    response = client.get(
        "/api/admin/users",
        params={
            "subscription_plan": SubscriptionPlan.PRO.value,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["subscription_plan"] == (SubscriptionPlan.PRO.value)


def test_admin_can_filter_by_status(
    client,
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    create_user(
        db_session,
        status=AccountStatus.SUSPENDED,
    )

    create_user(
        db_session,
        status=AccountStatus.ACTIVE,
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": admin.email,
            "password": "Password123!",
        },
    )

    client.headers.update(
        {
            "Authorization": (f"Bearer {login_response.json()['access_token']}"),
        }
    )

    response = client.get(
        "/api/admin/users",
        params={
            "status": AccountStatus.SUSPENDED.value,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["status"] == (AccountStatus.SUSPENDED.value)


def test_admin_user_list_supports_pagination(
    client,
    db_session,
):
    admin = create_user(
        db_session,
        role=UserRole.ADMIN,
    )

    for index in range(5):
        create_user(
            db_session,
            email=f"user{index}@example.com",
        )

    login_response = client.post(
        "/auth/login",
        data={
            "username": admin.email,
            "password": "Password123!",
        },
    )

    client.headers.update(
        {
            "Authorization": (f"Bearer {login_response.json()['access_token']}"),
        }
    )

    response = client.get(
        "/api/admin/users",
        params={
            "page": 1,
            "page_size": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 6
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total_pages"] == 3
    assert len(data["items"]) == 2
