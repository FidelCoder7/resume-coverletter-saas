from uuid import uuid4

from app.auth.security import hash_password
from app.common.constants import (
    AccountStatus,
    SubscriptionPlan,
    UserRole,
)
from app.users.models import User

DEFAULT_PASSWORD = "Password123!"


def make_user(
    *,
    email: str | None = None,
    password: str = DEFAULT_PASSWORD,
    full_name: str = "Test User",
    verified: bool = True,
    google_id: str | None = None,
) -> User:
    """
    Build a User instance without persisting it.
    """

    return User(
        id=uuid4(),
        email=email or f"{uuid4().hex}@example.com",
        full_name=full_name,
        password_hash=(hash_password(password) if google_id is None else None),
        google_id=google_id,
        is_email_verified=verified,
        role=UserRole.USER,
        subscription_plan=SubscriptionPlan.FREE,
        status=AccountStatus.ACTIVE,
    )


def create_user(
    db,
    **kwargs,
) -> User:
    """
    Create and persist a user.
    """

    user = make_user(**kwargs)

    db.add(user)

    db.commit()

    db.refresh(user)

    return user
