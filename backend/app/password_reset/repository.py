from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.password_reset.models import PasswordResetToken


class PasswordResetRepository:
    """
    Persistence layer for password reset tokens.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        token: PasswordResetToken,
    ) -> PasswordResetToken:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)

        return token

    def get_by_hash(
        self,
        token_hash: str,
    ) -> PasswordResetToken | None:
        statement = select(
            PasswordResetToken,
        ).where(
            PasswordResetToken.token_hash == token_hash,
        )

        return self.db.scalar(statement)

    def delete(
        self,
        token: PasswordResetToken,
    ) -> None:
        self.db.delete(token)
        self.db.commit()

    def delete_for_user(
        self,
        user_id: UUID,
    ) -> None:
        statement = delete(
            PasswordResetToken,
        ).where(
            PasswordResetToken.user_id == user_id,
        )

        self.db.execute(statement)
        self.db.commit()
