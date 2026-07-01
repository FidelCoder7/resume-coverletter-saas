from datetime import UTC, datetime

from app.auth.exceptions import AccountInactive, InvalidCredentials
from app.auth.security import (
    create_access_token,
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
    ) -> tuple[str, User]:
        user = self.authenticate(email, password)

        if user is None:
            raise InvalidCredentials("Invalid credentials.")

        if user.status != AccountStatus.PENDING:
            raise AccountInactive("Account is not active")

        user.last_login_at = datetime.now(UTC)

        self.repository.update(user)

        token = create_access_token(str(user.id))

        return token, user
