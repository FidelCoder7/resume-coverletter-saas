from app.auth.exceptions import EmailAlreadyRegistered
from app.auth.security import hash_password
from app.common.constants import (
    AccountStatus,
    SubscriptionPlan,
    UserRole,
)
from app.users.models import User
from app.users.repository import UserRepository


class UserService:
    """Business logic for user management."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(
        self,
        full_name: str,
        email: str,
        password: str,
    ) -> User:
        if self.repository.exists(email):
            raise EmailAlreadyRegistered("Email already registered.")

        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role=UserRole.USER,
            subscription_plan=SubscriptionPlan.FREE,
            status=AccountStatus.ACTIVE,
            is_email_verified=False,
        )

        return self.repository.create(user)
