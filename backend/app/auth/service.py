from datetime import UTC, datetime, timedelta
from uuid import UUID

from app.auth.exceptions import (
    AccountInactive,
    InvalidCredentials,
    InvalidToken,
)
from app.auth.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_refresh_token,
    verify_password,
)
from app.common.constants import AccountStatus
from app.core.config import settings
from app.refresh_tokens.models import RefreshToken
from app.refresh_tokens.repository import RefreshTokenRepository
from app.users.models import User
from app.users.repository import UserRepository


class AuthService:
    """Business logic for authentication."""

    def __init__(
        self,
        repository: UserRepository,
        refresh_repository: RefreshTokenRepository,
    ):
        self.repository = repository
        self.refresh_repository = refresh_repository

    def authenticate(
        self,
        email: str,
        password: str,
    ) -> User | None:
        user = self.repository.get_by_email(email)

        if user is None:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    def login(
        self,
        email: str,
        password: str,
    ) -> tuple[str, str, User]:
        user = self.authenticate(email, password)

        if user is None:
            raise InvalidCredentials("Invalid credentials.")

        if user.status != AccountStatus.ACTIVE:
            raise AccountInactive("Account is not active.")

        user.last_login_at = datetime.now(UTC)

        self.repository.update(user)

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))
        refresh_token_model = RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=datetime.now(UTC)
            + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
            ),
        )

        self.refresh_repository.create(
            refresh_token_model,
        )

        return (
            access_token,
            refresh_token,
            user,
        )

    def refresh_access_token(
        self,
        refresh_token: str,
    ) -> tuple[str, str]:
        """
        Exchange a valid refresh token for a new
        access token and a new refresh token.

        Implements refresh token rotation.
        """

        payload = decode_refresh_token(refresh_token)

        token_hash = hash_refresh_token(refresh_token)

        stored_token = self.refresh_repository.get_active_by_hash(
            token_hash,
        )

        if stored_token is None:
            raise InvalidToken("Refresh token is invalid.")

        if stored_token.is_expired:
            raise InvalidToken("Refresh token has expired.")

        user = self.repository.get_by_id(
            UUID(payload.sub),
        )

        if user is None:
            raise InvalidCredentials("User not found.")

        if user.status != AccountStatus.ACTIVE:
            raise AccountInactive("Account is not active.")

        # ---------------------------------------------------------
        # Revoke the current refresh token
        # ---------------------------------------------------------

        self.refresh_repository.revoke(
            stored_token,
        )

        # ---------------------------------------------------------
        # Issue fresh tokens
        # ---------------------------------------------------------

        new_access_token = create_access_token(
            str(user.id),
        )

        new_refresh_token = create_refresh_token(
            str(user.id),
        )

        # ---------------------------------------------------------
        # Persist the new refresh token
        # ---------------------------------------------------------

        new_refresh_token_model = RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(
                new_refresh_token,
            ),
            expires_at=datetime.now(UTC)
            + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
            ),
        )

        self.refresh_repository.create(
            new_refresh_token_model,
        )

        return (
            new_access_token,
            new_refresh_token,
        )

    def logout(
        self,
        refresh_token: str,
    ) -> None:
        """
        Revoke a refresh token so it can no longer
        be used to obtain new access tokens.
        """

        token_hash = hash_refresh_token(
            refresh_token,
        )

        stored_token = self.refresh_repository.get_active_by_hash(
            token_hash,
        )

        if stored_token is None:
            raise InvalidToken(
                "Refresh token is invalid.",
            )

        self.refresh_repository.revoke(
            stored_token,
        )
