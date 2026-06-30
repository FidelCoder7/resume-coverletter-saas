from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.constants import (
    AccountStatus,
    SubscriptionPlan,
    UserRole,
)
from app.database.base import Base
from app.database.enums import (
    account_status_enum,
    subscription_plan_enum,
    user_role_enum,
)


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        user_role_enum,
        default=UserRole.USER,
        nullable=False,
    )

    status: Mapped[AccountStatus] = mapped_column(
        account_status_enum,
        default=AccountStatus.PENDING,
        nullable=False,
    )

    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        subscription_plan_enum,
        default=SubscriptionPlan.FREE,
        nullable=False,
    )

    is_email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
