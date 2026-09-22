from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
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

    def count_all(self) -> int:
        """
        Return the total number of payment transactions.
        """

        statement = select(
            func.count(PaymentTransaction.id),
        )

        return (
            self.db.scalar(
                statement,
            )
            or 0
        )

    def count_by_status(
        self,
        *,
        status: PaymentStatus,
    ) -> int:
        """
        Return the number of payment transactions with a given status.
        """

        statement = select(
            func.count(PaymentTransaction.id),
        ).where(
            PaymentTransaction.status == status,
        )

        return (
            self.db.scalar(
                statement,
            )
            or 0
        )

    def sum_completed_amounts_by_currency(
        self,
    ) -> dict[str, Decimal]:
        """
        Return completed payment revenue grouped by currency.

        Only completed transactions are included.
        """

        statement = (
            select(
                PaymentTransaction.currency,
                func.coalesce(
                    func.sum(
                        PaymentTransaction.amount,
                    ),
                    0,
                ),
            )
            .where(
                PaymentTransaction.status == PaymentStatus.COMPLETED,
            )
            .group_by(
                PaymentTransaction.currency,
            )
        )

        return {
            currency: Decimal(str(amount))
            for currency, amount in self.db.execute(
                statement,
            ).all()
        }

    def count_by_period(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> int:
        """
        Return the number of payment transactions created within a period.
        """

        statement = select(
            func.count(PaymentTransaction.id),
        ).where(
            PaymentTransaction.created_at >= start_date,
            PaymentTransaction.created_at < end_date,
        )

        return self.db.scalar(statement) or 0

    def count_by_status_and_period(
        self,
        *,
        status: PaymentStatus,
        start_date: datetime,
        end_date: datetime,
    ) -> int:
        """
        Return payment transaction count by status within a period.
        """

        statement = select(
            func.count(PaymentTransaction.id),
        ).where(
            PaymentTransaction.status == status,
            PaymentTransaction.created_at >= start_date,
            PaymentTransaction.created_at < end_date,
        )

        return self.db.scalar(statement) or 0

    def sum_completed_amounts_by_currency_and_period(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[str, Decimal]:
        """
        Return completed revenue grouped by currency within a period.
        """

        statement = (
            select(
                PaymentTransaction.currency,
                func.coalesce(
                    func.sum(PaymentTransaction.amount),
                    0,
                ),
            )
            .where(
                PaymentTransaction.status == PaymentStatus.COMPLETED,
                PaymentTransaction.created_at >= start_date,
                PaymentTransaction.created_at < end_date,
            )
            .group_by(
                PaymentTransaction.currency,
            )
        )

        return {
            currency: Decimal(str(amount))
            for currency, amount in self.db.execute(statement).all()
        }

    def count_by_plan(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[SubscriptionPlan, int]:
        """
        Return transaction counts grouped by subscription plan.
        """

        statement = (
            select(
                PaymentTransaction.subscription_plan,
                func.count(PaymentTransaction.id),
            )
            .where(
                PaymentTransaction.created_at >= start_date,
                PaymentTransaction.created_at < end_date,
            )
            .group_by(
                PaymentTransaction.subscription_plan,
            )
        )

        return {plan: count for plan, count in self.db.execute(statement).all()}

    def count_by_transaction_type(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[BillingTransactionType, int]:
        """
        Return transaction counts grouped by billing transaction type.
        """

        statement = (
            select(
                PaymentTransaction.transaction_type,
                func.count(PaymentTransaction.id),
            )
            .where(
                PaymentTransaction.created_at >= start_date,
                PaymentTransaction.created_at < end_date,
            )
            .group_by(
                PaymentTransaction.transaction_type,
            )
        )

        return {
            transaction_type: count
            for transaction_type, count in self.db.execute(statement).all()
        }

    def count_by_provider(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[PaymentProvider, int]:
        """
        Return transaction counts grouped by payment provider.
        """

        statement = (
            select(
                PaymentTransaction.provider,
                func.count(PaymentTransaction.id),
            )
            .where(
                PaymentTransaction.created_at >= start_date,
                PaymentTransaction.created_at < end_date,
            )
            .group_by(
                PaymentTransaction.provider,
            )
        )

        return {provider: count for provider, count in self.db.execute(statement).all()}

    def count_by_payment_method(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[PaymentMethod, int]:
        """
        Return transaction counts grouped by payment method.
        """

        statement = (
            select(
                PaymentTransaction.payment_method,
                func.count(PaymentTransaction.id),
            )
            .where(
                PaymentTransaction.created_at >= start_date,
                PaymentTransaction.created_at < end_date,
                PaymentTransaction.payment_method.is_not(None),
            )
            .group_by(
                PaymentTransaction.payment_method,
            )
        )

        return {
            payment_method: count
            for payment_method, count in self.db.execute(statement).all()
        }

    def count_by_day(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> list[tuple[date, int]]:
        """
        Return payment transaction counts grouped by UTC calendar day.
        """

        statement = (
            select(
                func.date(PaymentTransaction.created_at).label("date"),
                func.count(PaymentTransaction.id).label("count"),
            )
            .where(
                PaymentTransaction.created_at >= start_date,
                PaymentTransaction.created_at < end_date,
            )
            .group_by(
                func.date(PaymentTransaction.created_at),
            )
            .order_by(
                func.date(PaymentTransaction.created_at),
            )
        )

        return [(row.date, row.count) for row in self.db.execute(statement).all()]

    def sum_completed_amounts_by_day_and_currency(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[str, list[tuple[date, Decimal]]]:
        """
        Return completed revenue grouped by currency and UTC calendar day.
        """

        statement = (
            select(
                PaymentTransaction.currency,
                func.date(PaymentTransaction.created_at).label("date"),
                func.coalesce(
                    func.sum(PaymentTransaction.amount),
                    0,
                ).label("amount"),
            )
            .where(
                PaymentTransaction.status == PaymentStatus.COMPLETED,
                PaymentTransaction.created_at >= start_date,
                PaymentTransaction.created_at < end_date,
            )
            .group_by(
                PaymentTransaction.currency,
                func.date(PaymentTransaction.created_at),
            )
            .order_by(
                PaymentTransaction.currency,
                func.date(PaymentTransaction.created_at),
            )
        )

        result: dict[str, list[tuple[date, Decimal]]] = {}

        for row in self.db.execute(statement).all():
            result.setdefault(
                row.currency,
                [],
            ).append(
                (
                    row.date,
                    Decimal(str(row.amount or 0)),
                )
            )

        return result
