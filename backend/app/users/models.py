from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

if TYPE_CHECKING:
    from app.email_verification.models import EmailVerificationToken
    from app.refresh_tokens.models import RefreshToken


class User(Base):
    __tablename__ = "users"

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Authorization
    # ------------------------------------------------------------------

    role: Mapped[UserRole] = mapped_column(
        user_role_enum,
        default=UserRole.USER,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Subscription
    # ------------------------------------------------------------------

    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        subscription_plan_enum,
        default=SubscriptionPlan.FREE,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Account
    # ------------------------------------------------------------------

    status: Mapped[AccountStatus] = mapped_column(
        account_status_enum,
        default=AccountStatus.ACTIVE,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------------

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    email_verification_tokens: Mapped[list["EmailVerificationToken"]] = relationship(
        "EmailVerificationToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )
