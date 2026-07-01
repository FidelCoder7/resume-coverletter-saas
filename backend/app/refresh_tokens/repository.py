from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.refresh_tokens.models import RefreshToken


class RefreshTokenRepository:
    """
    Persistence layer for refresh tokens.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        token: RefreshToken,
    ) -> RefreshToken:
        """
        Persist a refresh token.
        """

        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)

        return token

    def get_by_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        """
        Find a refresh token by its SHA-256 hash.
        """

        statement = (
            select(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash,
            )
        )

        return self.db.scalar(statement)

    def get_active_by_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        """
        Return a refresh token only if it is active.
        """

        statement = (
            select(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked_at.is_(None),
            )
        )

        return self.db.scalar(statement)

    def get_user_tokens(
        self,
        user_id: UUID,
    ) -> list[RefreshToken]:
        """
        Return all refresh tokens for a user.
        """

        statement = (
            select(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def revoke(
        self,
        token: RefreshToken,
    ) -> RefreshToken:
        """
        Revoke a refresh token.
        """

        token.revoked_at = datetime.now(UTC)

        self.db.commit()
        self.db.refresh(token)

        return token

    def revoke_all_for_user(
        self,
        user_id: UUID,
    ) -> None:
        """
        Revoke every refresh token belonging to a user.
        """

        tokens = self.get_user_tokens(user_id)

        now = datetime.now(UTC)

        for token in tokens:
            token.revoked_at = now

        self.db.commit()

    def delete_expired(self) -> int:
        """
        Permanently delete expired refresh tokens.

        Returns the number of rows deleted.
        """

        statement = delete(RefreshToken).where(
            RefreshToken.expires_at < datetime.now(UTC)
        )

        result = self.db.execute(statement)

        self.db.commit()

        return result.rowcount or 0