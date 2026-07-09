from datetime import UTC, datetime, timedelta

from app.auth.security import (
    generate_password_reset_token,
    hash_password,
    hash_password_reset_token,
)
from app.core.config import settings
from app.mail.service import MailService
from app.mail.templates import password_reset_email
from app.password_reset.exceptions import (
    PasswordResetTokenExpired,
    PasswordResetTokenInvalid,
)
from app.password_reset.models import PasswordResetToken
from app.password_reset.repository import PasswordResetRepository
from app.users.models import User
from app.users.repository import UserRepository


class PasswordResetService:
    """
    Handles password reset.
    """

    def __init__(
        self,
        repository: PasswordResetRepository,
        user_repository: UserRepository,
        mail_service: MailService,
    ):
        self.repository = repository
        self.user_repository = user_repository
        self.mail_service = mail_service

    def request_password_reset(
        self,
        user: User,
    ) -> None:
        """
        Create a password reset token
        and send it via email.
        """

        self.repository.delete_for_user(
            user.id,
        )

        raw_token = generate_password_reset_token()

        token = PasswordResetToken(
            user_id=user.id,
            token_hash=hash_password_reset_token(
                raw_token,
            ),
            expires_at=datetime.now(UTC)
            + timedelta(
                hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS,
            ),
        )

        self.repository.create(
            token,
        )

        subject, html = password_reset_email(
            full_name=user.full_name,
            token=raw_token,
        )

        self.mail_service.send(
            recipient=user.email,
            subject=subject,
            body=(f"Reset your password.\n\nToken: {raw_token}"),
            html=html,
        )

    def reset_password(
        self,
        raw_token: str,
        new_password: str,
    ) -> None:
        """
        Reset a user's password.
        """

        token_hash = hash_password_reset_token(
            raw_token,
        )

        token = self.repository.get_by_hash(
            token_hash,
        )

        if token is None:
            raise PasswordResetTokenInvalid(
                "Invalid password reset token.",
            )

        if token.is_expired:
            self.repository.delete(token)

            raise PasswordResetTokenExpired(
                "Password reset token has expired.",
            )

        user = self.user_repository.get_by_id(
            token.user_id,
        )

        if user is None:
            raise PasswordResetTokenInvalid(
                "User not found.",
            )

        user.password_hash = hash_password(
            new_password,
        )

        self.user_repository.update(
            user,
        )

        self.repository.delete(
            token,
        )
