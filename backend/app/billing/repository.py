from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.billing.models import PaymentTransaction
from app.common.constants import (
    BillingTransactionType,
    PaymentMethod,
    PaymentProvider,
    PaymentStatus,
    SubscriptionPlan,
)


class PaymentTransactionRepository:
    """
    Repository for payment transaction persistence and retrieval.


    This repository is responsible only for database access.
    Payment provider communication and subscription activation logic
    belong to higher application layers.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def create(
        self,
        *,
        user_id: UUID,
        subscription_plan: SubscriptionPlan,
        transaction_type: BillingTransactionType,
        provider: PaymentProvider,
        provider_order_id: str,
        amount: Decimal,
        currency: str = "KES",
        provider_transaction_id: str | None = None,
        payment_method: PaymentMethod | None = None,
        status: PaymentStatus = PaymentStatus.PENDING,
        failure_reason: str | None = None,
        provider_response: dict | None = None,
    ) -> PaymentTransaction:
        """
        Create and persist a payment transaction.
        """

        transaction = PaymentTransaction(
            user_id=user_id,
            subscription_plan=subscription_plan,
            transaction_type=transaction_type,
            provider=provider,
            provider_order_id=provider_order_id,
            provider_transaction_id=provider_transaction_id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            status=status,
            failure_reason=failure_reason,
            provider_response=provider_response,
        )

        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        return transaction

    def get_by_id(
        self,
        transaction_id: UUID,
    ) -> PaymentTransaction | None:
        """
        Retrieve a payment transaction by its primary key.
        """

        return self.db.get(
            PaymentTransaction,
            transaction_id,
        )

    def get_by_provider_order_id(
        self,
        *,
        provider: PaymentProvider,
        provider_order_id: str,
    ) -> PaymentTransaction | None:
        """
        Retrieve a payment transaction by payment provider
        and provider-specific order ID.
        """

        statement = select(PaymentTransaction).where(
            PaymentTransaction.provider == provider,
            PaymentTransaction.provider_order_id == provider_order_id,
        )

        return self.db.scalar(statement)

    def get_by_provider_transaction_id(
        self,
        *,
        provider: PaymentProvider,
        provider_transaction_id: str,
    ) -> PaymentTransaction | None:
        """
        Retrieve a payment transaction by payment provider
        and provider-specific transaction ID.
        """

        statement = select(PaymentTransaction).where(
            PaymentTransaction.provider == provider,
            PaymentTransaction.provider_transaction_id == provider_transaction_id,
        )

        return self.db.scalar(statement)

    def list_by_user(
        self,
        *,
        user_id: UUID,
        status: PaymentStatus | None = None,
    ) -> list[PaymentTransaction]:
        """
        Return payment transactions belonging to a user.

        Results are ordered from newest to oldest.
        Optionally filter by payment status.
        """

        statement = (
            select(PaymentTransaction)
            .where(
                PaymentTransaction.user_id == user_id,
            )
            .order_by(
                PaymentTransaction.created_at.desc(),
            )
        )

        if status is not None:
            statement = statement.where(
                PaymentTransaction.status == status,
            )

        return list(
            self.db.scalars(statement).all(),
        )

    def update(
        self,
        transaction: PaymentTransaction,
    ) -> PaymentTransaction:
        """
        Persist changes made to an existing payment transaction.
        """

        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        return transaction
