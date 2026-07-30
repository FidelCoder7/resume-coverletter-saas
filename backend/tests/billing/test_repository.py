from decimal import Decimal
from uuid import uuid4

from app.billing.repository import PaymentTransactionRepository
from app.common.constants import (
    BillingTransactionType,
    PaymentMethod,
    PaymentProvider,
    PaymentStatus,
    SubscriptionPlan,
)
from tests.factories.user_factory import create_user


def create_transaction(
    db_session,
    *,
    user_id,
    provider_order_id: str = "ORDER-001",
    provider_transaction_id: str | None = "TRANSACTION-001",
    status: PaymentStatus = PaymentStatus.PENDING,
):
    repository = PaymentTransactionRepository(
        db_session,
    )

    return repository.create(
        user_id=user_id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=BillingTransactionType.SUBSCRIPTION_PURCHASE,
        provider=PaymentProvider.PESAPAL,
        provider_order_id=provider_order_id,
        provider_transaction_id=provider_transaction_id,
        amount=Decimal("1500.00"),
        currency="KES",
        payment_method=PaymentMethod.MPESA,
        status=status,
        provider_response={
            "order_tracking_id": provider_transaction_id,
        },
    )


def test_create_persists_payment_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    repository = PaymentTransactionRepository(
        db_session,
    )

    result = repository.create(
        user_id=user.id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=BillingTransactionType.SUBSCRIPTION_PURCHASE,
        provider=PaymentProvider.PESAPAL,
        provider_order_id="ORDER-001",
        amount=Decimal("1500.00"),
        currency="KES",
        payment_method=PaymentMethod.MPESA,
    )

    assert result.id is not None
    assert result.user_id == user.id
    assert result.subscription_plan == SubscriptionPlan.PRO
    assert result.transaction_type == BillingTransactionType.SUBSCRIPTION_PURCHASE
    assert result.provider == PaymentProvider.PESAPAL
    assert result.provider_order_id == "ORDER-001"
    assert result.amount == Decimal("1500.00")
    assert result.currency == "KES"
    assert result.payment_method == PaymentMethod.MPESA
    assert result.status == PaymentStatus.PENDING


def test_get_by_id_returns_payment_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    transaction = create_transaction(
        db_session,
        user_id=user.id,
    )

    repository = PaymentTransactionRepository(
        db_session,
    )

    result = repository.get_by_id(
        transaction.id,
    )

    assert result is not None
    assert result.id == transaction.id
    assert result.user_id == user.id
    assert result.provider_order_id == "ORDER-001"


def test_get_by_id_returns_none_for_unknown_id(
    db_session,
):

    repository = PaymentTransactionRepository(
        db_session,
    )

    result = repository.get_by_id(
        uuid4(),
    )

    assert result is None


def test_get_by_provider_order_id_returns_matching_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    transaction = create_transaction(
        db_session,
        user_id=user.id,
    )

    repository = PaymentTransactionRepository(
        db_session,
    )

    result = repository.get_by_provider_order_id(
        provider=PaymentProvider.PESAPAL,
        provider_order_id="ORDER-001",
    )

    assert result is not None
    assert result.id == transaction.id
    assert result.provider == PaymentProvider.PESAPAL
    assert result.provider_order_id == "ORDER-001"


def test_get_by_provider_order_id_returns_none_for_unknown_order(
    db_session,
):
    repository = PaymentTransactionRepository(
        db_session,
    )

    result = repository.get_by_provider_order_id(
        provider=PaymentProvider.PESAPAL,
        provider_order_id="UNKNOWN-ORDER",
    )

    assert result is None


def test_get_by_provider_transaction_id_returns_matching_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    transaction = create_transaction(
        db_session,
        user_id=user.id,
        provider_transaction_id="TRANSACTION-001",
    )

    repository = PaymentTransactionRepository(
        db_session,
    )

    result = repository.get_by_provider_transaction_id(
        provider=PaymentProvider.PESAPAL,
        provider_transaction_id="TRANSACTION-001",
    )

    assert result is not None
    assert result.id == transaction.id
    assert result.provider_transaction_id == "TRANSACTION-001"


def test_get_by_provider_transaction_id_returns_none_for_unknown_transaction(
    db_session,
):
    repository = PaymentTransactionRepository(
        db_session,
    )

    result = repository.get_by_provider_transaction_id(
        provider=PaymentProvider.PESAPAL,
        provider_transaction_id="UNKNOWN-TRANSACTION",
    )

    assert result is None


def test_list_by_user_returns_transactions_for_requested_user(
    db_session,
):
    user = create_user(
        db_session,
    )

    other_user = create_user(
        db_session,
    )

    first = create_transaction(
        db_session,
        user_id=user.id,
        provider_order_id="ORDER-001",
        provider_transaction_id="TRANSACTION-001",
    )

    second = create_transaction(
        db_session,
        user_id=user.id,
        provider_order_id="ORDER-002",
        provider_transaction_id="TRANSACTION-002",
        status=PaymentStatus.COMPLETED,
    )

    create_transaction(
        db_session,
        user_id=other_user.id,
        provider_order_id="ORDER-003",
        provider_transaction_id="TRANSACTION-003",
    )

    repository = PaymentTransactionRepository(
        db_session,
    )

    results = repository.list_by_user(
        user_id=user.id,
    )

    assert len(results) == 2
    assert {item.id for item in results} == {
        first.id,
        second.id,
    }


def test_list_by_user_can_filter_by_status(
    db_session,
):
    user = create_user(
        db_session,
    )

    pending = create_transaction(
        db_session,
        user_id=user.id,
        provider_order_id="ORDER-001",
        provider_transaction_id="TRANSACTION-001",
        status=PaymentStatus.PENDING,
    )

    completed = create_transaction(
        db_session,
        user_id=user.id,
        provider_order_id="ORDER-002",
        provider_transaction_id="TRANSACTION-002",
        status=PaymentStatus.COMPLETED,
    )

    repository = PaymentTransactionRepository(
        db_session,
    )

    results = repository.list_by_user(
        user_id=user.id,
        status=PaymentStatus.COMPLETED,
    )

    assert len(results) == 1
    assert results[0].id == completed.id
    assert results[0].status == PaymentStatus.COMPLETED
    assert results[0].id != pending.id


def test_update_persists_transaction_changes(
    db_session,
):
    user = create_user(
        db_session,
    )

    transaction = create_transaction(
        db_session,
        user_id=user.id,
    )

    transaction.status = PaymentStatus.COMPLETED
    transaction.provider_transaction_id = "TRANSACTION-COMPLETED"
    transaction.payment_method = PaymentMethod.MPESA
    transaction.provider_response = {
        "status": "COMPLETED",
        "order_tracking_id": "TRANSACTION-COMPLETED",
    }

    repository = PaymentTransactionRepository(
        db_session,
    )

    result = repository.update(
        transaction,
    )

    assert result.status == PaymentStatus.COMPLETED
    assert result.provider_transaction_id == "TRANSACTION-COMPLETED"
    assert result.payment_method == PaymentMethod.MPESA
    assert result.provider_response == {
        "status": "COMPLETED",
        "order_tracking_id": "TRANSACTION-COMPLETED",
    }
