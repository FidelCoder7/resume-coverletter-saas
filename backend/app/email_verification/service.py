from datetime import UTC, datetime, timedelta

from app.auth.security import (
    generate_email_verification_token,
    hash_email_verification_token,
)
from app.core.config import settings
from app.email_verification.exceptions import (
    VerificationTokenExpired,
    VerificationTokenInvalid,
)
from app.email_verification.models import EmailVerificationToken
from app.email_verification.repository import (
    EmailVerificationRepository,
)
from app.mail.service import MailService
from app.mail.templates import verification_email
from app.users.models import User
from app.users.repository import UserRepository


class EmailVerificationService:
    """
    Handles email verification.
    """

    def __init__(
        self,
        repository: EmailVerificationRepository,
        user_repository: UserRepository,
        mail_service: MailService,
    ):
        self.repository = repository
        self.user_repository = user_repository
        self.mail_service = mail_service

    def create_verification_token(
        self,
        user: User,
    ) -> None:
        """
        Generate a verification token,
        persist it and send the verification email.
        """

        self.repository.delete_for_user(user.id)

        raw_token = generate_email_verification_token()

        verification_token = EmailVerificationToken(
            user_id=user.id,
            token_hash=hash_email_verification_token(raw_token),
            expires_at=datetime.now(UTC)
            + timedelta(
                hours=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS,
            ),
        )

        self.repository.create(
            verification_token,
        )

        subject, html = verification_email(
            full_name=user.full_name,
            token=raw_token,
        )

        self.mail_service.send(
            recipient=user.email,
            subject=subject,
            body=(f"Please verify your email.\n\nToken: {raw_token}"),
            html=html,
        )

    def verify_email(
        self,
        raw_token: str,
    ) -> None:
        """
        Verify a user's email.
        """

        token_hash = hash_email_verification_token(
            raw_token,
        )

        token = self.repository.get_by_hash(
            token_hash,
        )

        if token is None:
            raise VerificationTokenInvalid(
                "Invalid verification token.",
            )

        if token.is_expired:
            self.repository.delete(token)

            raise VerificationTokenExpired(
                "Verification token has expired.",
            )

        user = self.user_repository.get_by_id(
            token.user_id,
        )

        if user is None:
            raise VerificationTokenInvalid(
                "User not found.",
            )

        user.is_email_verified = True

        self.user_repository.update(user)

        self.repository.delete(token)
