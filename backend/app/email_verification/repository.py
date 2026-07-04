from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.email_verification.models import EmailVerificationToken


class EmailVerificationRepository:
    """
    Persistence layer for email verification tokens.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        token: EmailVerificationToken,
    ) -> EmailVerificationToken:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)

        return token

    def get_by_hash(
        self,
        token_hash: str,
    ) -> EmailVerificationToken | None:
        statement = select(
            EmailVerificationToken,
        ).where(
            EmailVerificationToken.token_hash == token_hash,
        )

        return self.db.scalar(statement)

    def delete(
        self,
        token: EmailVerificationToken,
    ) -> None:
        self.db.delete(token)
        self.db.commit()

    def delete_for_user(
        self,
        user_id: UUID,
    ) -> None:
        statement = delete(
            EmailVerificationToken,
        ).where(
            EmailVerificationToken.user_id == user_id,
        )

        self.db.execute(statement)
        self.db.commit()

    def get_active_by_hash(
        self,
        token_hash: str,
    ) -> EmailVerificationToken | None:
        """
        Return a verification token if it exists.
        """

        statement = select(
            EmailVerificationToken,
        ).where(
            EmailVerificationToken.token_hash == token_hash,
        )

        return self.db.scalar(statement)
