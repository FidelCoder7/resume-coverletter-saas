from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.constants import (
    AccountStatus,
    SubscriptionPlan,
    UserRole,
)
from app.users.models import User


class UserRepository:
    """Repository for user persistence."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def get_by_id(self, user_id: UUID) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def update(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()

    def get_by_google_id(
        self,
        google_id: str,
    ) -> User | None:
        statement = select(User).where(
            User.google_id == google_id,
        )

        return self.db.scalar(statement)

    def create_google_user(
        self,
        *,
        email: str,
        full_name: str,
        google_id: str,
    ) -> User:
        user = User(
            email=email,
            full_name=full_name,
            google_id=google_id,
            is_email_verified=True,
            status=AccountStatus.ACTIVE,
            role=UserRole.USER,
            subscription_plan=SubscriptionPlan.FREE,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_profile(
        self,
        user_id: UUID,
    ) -> User | None:
        """
        Return the authenticated user's profile.
        """

        return self.get_by_id(user_id)

    def update_profile(
        self,
        *,
        user: User,
        full_name: str,
    ) -> User:
        """
        Update editable profile fields.
        """

        user.full_name = full_name

        self.db.commit()
        self.db.refresh(user)

        return user

    def soft_delete(
        self,
        user: User,
    ) -> None:
        """
        Soft delete a user account.
        """

        user.status = AccountStatus.DELETED
        user.deleted_at = datetime.now(UTC)

        self.db.commit()
