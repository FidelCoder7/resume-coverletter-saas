from uuid import UUID

from app.auth.exceptions import EmailAlreadyRegistered, InvalidCredentials
from app.auth.security import hash_password
from app.common.constants import (
    AccountStatus,
    SubscriptionPlan,
    UserRole,
)
from app.email_verification.repository import (
    EmailVerificationRepository,
)
from app.email_verification.service import (
    EmailVerificationService,
)
from app.mail.service import MailService
from app.users.models import User
from app.users.repository import UserRepository


class UserService:
    """Business logic for user management."""

    def __init__(
        self,
        repository: UserRepository,
        verification_repository: EmailVerificationRepository,
    ):
        self.repository = repository

        self.verification_service = EmailVerificationService(
            verification_repository,
            repository,
            MailService(),
        )

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

        user = self.repository.create(user)

        self.verification_service.create_verification_token(
            user,
        )

        return user

    def get_profile(
        self,
        user_id: UUID,
    ) -> User:
        """
        Return the authenticated user's profile.
        """

        user = self.repository.get_profile(user_id)

        if user is None:
            raise InvalidCredentials("User not found.")

        return user

    def update_profile(
        self,
        *,
        user_id: UUID,
        full_name: str,
    ) -> User:
        """
        Update the authenticated user's profile.
        """

        user = self.repository.get_profile(user_id)

        if user is None:
            raise InvalidCredentials("User not found.")

        return self.repository.update_profile(
            user=user,
            full_name=full_name,
        )

    def delete_account(
        self,
        user_id: UUID,
    ) -> None:
        """
        Soft delete a user account.
        """

        user = self.repository.get_profile(user_id)

        if user is None:
            raise InvalidCredentials("User not found.")

        self.repository.soft_delete(user)
