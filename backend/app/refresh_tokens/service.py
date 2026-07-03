import hashlib
from datetime import UTC, datetime, timedelta

from app.auth.exceptions import InvalidToken
from app.auth.security import (
    create_refresh_token,
    decode_refresh_token,
)
from app.core.config import settings
from app.refresh_tokens.models import RefreshToken
from app.refresh_tokens.repository import RefreshTokenRepository


class TokenService:
    """
    Business logic for refresh token lifecycle.
    """

    def __init__(
        self,
        repository: RefreshTokenRepository,
    ):
        self.repository = repository

    @staticmethod
    def hash_token(token: str) -> str:
        """
        Hash a refresh token before persisting it.
        """
        return hashlib.sha256(token.encode()).hexdigest()

    def issue_refresh_token(
        self,
        user_id: str,
        device_name: str | None = None,
    ) -> str:
        """
        Create, hash and persist a refresh token.
        """

        token = create_refresh_token(user_id)

        token_hash = self.hash_token(token)

        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            device_name=device_name,
            expires_at=datetime.now(UTC)
            + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
            ),
        )

        self.repository.create(refresh_token)

        return token

    def validate_refresh_token(
        self,
        token: str,
    ) -> RefreshToken:
        """
        Validate a persisted refresh token.
        """

        decode_refresh_token(token)

        token_hash = self.hash_token(token)

        stored_token = self.repository.get_by_hash(
            token_hash,
        )

        if stored_token is None:
            raise InvalidToken("Refresh token not found.")

        if stored_token.revoked:
            raise InvalidToken("Refresh token revoked.")

        if stored_token.expires_at < datetime.now(UTC):
            raise InvalidToken("Refresh token expired.")

        return stored_token
