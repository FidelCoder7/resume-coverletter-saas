from datetime import datetime

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.constants import (
    AccountStatus,
    SubscriptionPlan,
    UserRole,
)
from app.database.base import Base


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
        Enum(
            UserRole,
            name="user_role",
            create_constraint=True,
        ),
        default=UserRole.USER,
        nullable=False,
    )

    status: Mapped[AccountStatus] = mapped_column(
        Enum(
            AccountStatus,
            name="account_status",
            create_constraint=True,
        ),
        default=AccountStatus.PENDING,
        nullable=False,
    )

    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        Enum(
            SubscriptionPlan,
            name="subscription_plan",
            create_constraint=True,
        ),
        default=SubscriptionPlan.FREE,
        nullable=False,
    )

    is_email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login_at: Mapped[datetime | None]

    deleted_at: Mapped[datetime | None]
