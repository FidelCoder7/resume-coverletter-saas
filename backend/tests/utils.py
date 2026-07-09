from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def authenticated_user(client, db_session):
    """
    Create a verified user and log them in.

    Returns:
        (user, access_token)
    """

    user = create_user(
        db_session,
        verified=True,
    )

    response = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = response.json()["access_token"]

    return user, token


def auth_headers(token: str):
    return {
        "Authorization": f"Bearer {token}",
    }
