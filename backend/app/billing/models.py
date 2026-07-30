from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.constants import SubscriptionPlan
from app.database.base import Base
from app.database.enums import (
    billing_transaction_type_enum,
    payment_method_enum,
    payment_provider_enum,
    payment_status_enum,
    subscription_plan_enum,
)

if TYPE_CHECKING:
    from app.users.models import User


class PaymentTransaction(Base):
    """
    Represents a payment transaction initiated by a user.

    Payment transactions are financial records representing an attempt
    to purchase or renew a subscription.

    Payment lifecycle state is independent from subscription usage
    enforcement. Subscription activation or modification occurs only
    after successful payment confirmation from the provider.
    """

    __tablename__ = "payment_transactions"

    # ------------------------------------------------------------------
    # Ownership
    # ------------------------------------------------------------------

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="payment_transactions",
    )

    # ------------------------------------------------------------------
    # Billing
    # ------------------------------------------------------------------

    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        subscription_plan_enum,
        nullable=False,
    )

    transaction_type: Mapped[str] = mapped_column(
        billing_transaction_type_enum,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Payment Provider
    # ------------------------------------------------------------------

    provider: Mapped[str] = mapped_column(
        payment_provider_enum,
        nullable=False,
    )

    provider_order_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    provider_transaction_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Payment Details
    # ------------------------------------------------------------------

    amount: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=12,
            scale=2,
        ),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="KES",
    )

    payment_method: Mapped[str | None] = mapped_column(
        payment_method_enum,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    status: Mapped[str] = mapped_column(
        payment_status_enum,
        nullable=False,
    )

    failure_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Provider Metadata
    # ------------------------------------------------------------------

    provider_response: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Constraints and Indexes
    # ------------------------------------------------------------------

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_order_id",
            name="uq_payment_transactions_provider_order_id",
        ),
        Index(
            "ix_payment_transactions_provider_transaction_id",
            "provider",
            "provider_transaction_id",
        ),
        Index(
            "ix_payment_transactions_user_status",
            "user_id",
            "status",
        ),
    )
