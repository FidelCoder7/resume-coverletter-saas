from decimal import Decimal

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from app.billing.models import PaymentTransaction
from app.common.constants import (
    BillingTransactionType,
    PaymentMethod,
    PaymentProvider,
    PaymentStatus,
    SubscriptionPlan,
)
from tests.factories.user_factory import create_user


def make_transaction(
    *,
    user_id,
    provider_order_id: str = "ORDER-001",
) -> PaymentTransaction:
    return PaymentTransaction(
        user_id=user_id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=BillingTransactionType.SUBSCRIPTION_PURCHASE,
        provider=PaymentProvider.PESAPAL,
        provider_order_id=provider_order_id,
        amount=Decimal("1500.00"),
        currency="KES",
        payment_method=PaymentMethod.MPESA,
        status=PaymentStatus.PENDING,
    )


def test_payment_transaction_persists_required_fields(
    db_session,
):
    user = create_user(
        db_session,
    )

    transaction = make_transaction(
        user_id=user.id,
    )

    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    assert transaction.id is not None
    assert transaction.user_id == user.id
    assert transaction.subscription_plan == SubscriptionPlan.PRO
    assert transaction.transaction_type == BillingTransactionType.SUBSCRIPTION_PURCHASE
    assert transaction.provider == PaymentProvider.PESAPAL
    assert transaction.provider_order_id == "ORDER-001"
    assert transaction.amount == Decimal("1500.00")
    assert transaction.currency == "KES"
    assert transaction.payment_method == PaymentMethod.MPESA
    assert transaction.status == PaymentStatus.PENDING


def test_payment_transaction_defaults_currency_to_kes(
    db_session,
):
    user = create_user(
        db_session,
    )

    transaction = PaymentTransaction(
        user_id=user.id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=BillingTransactionType.SUBSCRIPTION_PURCHASE,
        provider=PaymentProvider.PESAPAL,
        provider_order_id="ORDER-DEFAULT-CURRENCY",
        amount=Decimal("1500.00"),
        payment_method=PaymentMethod.MPESA,
        status=PaymentStatus.PENDING,
    )

    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    assert transaction.currency == "KES"


def test_payment_transaction_allows_nullable_provider_fields(
    db_session,
):
    user = create_user(
        db_session,
    )

    transaction = make_transaction(
        user_id=user.id,
    )

    transaction.provider_transaction_id = None
    transaction.payment_method = None
    transaction.failure_reason = None
    transaction.provider_response = None

    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    assert transaction.provider_transaction_id is None
    assert transaction.payment_method is None
    assert transaction.failure_reason is None
    assert transaction.provider_response is None


def test_payment_transaction_requires_unique_provider_order_id(
    db_session,
):
    user = create_user(
        db_session,
    )

    first = make_transaction(
        user_id=user.id,
        provider_order_id="DUPLICATE-ORDER",
    )

    second = make_transaction(
        user_id=user.id,
        provider_order_id="DUPLICATE-ORDER",
    )

    db_session.add(first)
    db_session.commit()

    db_session.add(second)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_payment_transaction_user_relationship(
    db_session,
):
    user = create_user(
        db_session,
    )

    transaction = make_transaction(
        user_id=user.id,
    )

    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    assert transaction.user is user


def test_payment_transaction_has_expected_indexes_and_constraints():
    table = PaymentTransaction.__table__

    index_names = {index.name for index in table.indexes}

    constraint_names = {constraint.name for constraint in table.constraints}

    assert "ix_payment_transactions_provider_transaction_id" in index_names

    assert "ix_payment_transactions_user_status" in index_names

    assert "uq_payment_transactions_provider_order_id" in constraint_names


def test_payment_transaction_has_uuid_primary_key():
    mapper = inspect(
        PaymentTransaction,
    )

    primary_key_columns = mapper.primary_key

    assert len(primary_key_columns) == 1
    assert primary_key_columns[0].name == "id"
