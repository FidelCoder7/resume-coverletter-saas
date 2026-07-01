from datetime import UTC, datetime
from uuid import UUID

from app.auth.exceptions import AccountInactive, InvalidCredentials
from app.auth.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_password,
)
from app.common.constants import AccountStatus
from app.users.models import User
from app.users.repository import UserRepository


class AuthService:
    """Business logic for authentication."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

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

        return (
            access_token,
            refresh_token,
            user,
        )

    def refresh_access_token(
        self,
        refresh_token: str,
    ) -> str:
        """
        Exchange a valid refresh token for a new access token.
        """

        payload = decode_refresh_token(refresh_token)

        user = self.repository.get_by_id(
            UUID(payload.sub),
        )

        if user is None:
            raise InvalidCredentials("User not found.")

        if user.status != AccountStatus.ACTIVE:
            raise AccountInactive("Account is not active.")

        return create_access_token(str(user.id))