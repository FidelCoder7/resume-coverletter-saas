from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.billing.exceptions import (
    InvalidPaymentTransactionState,
    PaymentTransactionAlreadyCompleted,
    PaymentTransactionNotFound,
)
from app.billing.providers.base import PaymentProvider as PaymentProviderClient
from app.billing.providers.schemas import (
    PaymentCallbackResult,
    PaymentInitiationResult,
    PaymentStatusResult,
)
from app.billing.repository import PaymentTransactionRepository
from app.billing.service import PaymentTransactionService
from app.common.constants import (
    BillingTransactionType,
    PaymentMethod,
    PaymentProvider,
    PaymentStatus,
    SubscriptionPlan,
)
from tests.factories.user_factory import create_user


def create_service(
    db_session,
    provider: PaymentProviderClient | None = None,
) -> PaymentTransactionService:
    repository = PaymentTransactionRepository(
        db_session,
    )

    return PaymentTransactionService(
        repository=repository,
        provider=provider or Mock(spec=PaymentProviderClient),
    )


def initiate_transaction(
    service: PaymentTransactionService,
    *,
    user_id,
    provider_order_id: str | None = None,
):
    return service.initiate_payment(
        user_id=user_id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=BillingTransactionType.SUBSCRIPTION_PURCHASE,
        provider=PaymentProvider.PESAPAL,
        provider_order_id=(provider_order_id or f"ORDER-{uuid4().hex}"),
        amount=Decimal("1000.00"),
        currency="KES",
        payment_method=PaymentMethod.MPESA,
    )


def callback_payload(
    *,
    merchant_reference: str = "ORDER-001",
    tracking_id: str | None = "TRACKING-001",
    notification_type: str = "COMPLETED",
) -> dict:
    return {
        "OrderMerchantReference": merchant_reference,
        "OrderTrackingId": tracking_id,
        "OrderNotificationType": notification_type,
    }


# ---------------------------------------------------------------------------
# Creation
# ---------------------------------------------------------------------------


def test_initiate_payment_creates_pending_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    assert transaction.id is not None
    assert transaction.user_id == user.id
    assert transaction.subscription_plan == SubscriptionPlan.PRO
    assert transaction.transaction_type == BillingTransactionType.SUBSCRIPTION_PURCHASE
    assert transaction.provider == PaymentProvider.PESAPAL
    assert transaction.provider_order_id.startswith(
        "ORDER-",
    )
    assert transaction.amount == Decimal("1000.00")
    assert transaction.currency == "KES"
    assert transaction.payment_method == PaymentMethod.MPESA
    assert transaction.status == PaymentStatus.PENDING


def test_initiate_payment_persists_provider_response(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    provider_response = {
        "order_tracking_id": "TRACKING-001",
        "status": "200",
    }

    transaction = service.initiate_payment(
        user_id=user.id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=BillingTransactionType.SUBSCRIPTION_PURCHASE,
        provider=PaymentProvider.PESAPAL,
        provider_order_id="ORDER-001",
        amount=Decimal("1000.00"),
        currency="KES",
        provider_response=provider_response,
    )

    assert transaction.status == PaymentStatus.PENDING
    assert transaction.provider_response == provider_response


# ---------------------------------------------------------------------------
# Provider Integration
# ---------------------------------------------------------------------------


def test_start_payment_initiates_provider_and_persists_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    provider = Mock(
        spec=PaymentProviderClient,
    )

    provider.initiate_payment.return_value = PaymentInitiationResult(
        provider_order_id="ORDER-001",
        provider_transaction_id="TRANSACTION-001",
        status=PaymentStatus.PENDING,
        redirect_url="https://pay.example.com/checkout",
        provider_response={
            "order_tracking_id": "TRACKING-001",
            "status": "200",
        },
    )

    service = create_service(
        db_session,
        provider=provider,
    )

    transaction, redirect_url = service.start_payment(
        user_id=user.id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=(BillingTransactionType.SUBSCRIPTION_PURCHASE),
        customer_email=user.email,
        customer_name="Test User",
        payment_method=PaymentMethod.MPESA,
    )

    provider.initiate_payment.assert_called_once()

    assert transaction.user_id == user.id
    assert transaction.provider == PaymentProvider.PESAPAL

    assert transaction.status == PaymentStatus.PENDING
    assert transaction.provider_transaction_id == "TRANSACTION-001"
    assert transaction.provider_response == {
        "order_tracking_id": "TRACKING-001",
        "status": "200",
    }
    assert redirect_url == "https://pay.example.com/checkout"


def test_start_payment_passes_correct_request_to_provider(
    db_session,
):
    user = create_user(
        db_session,
    )

    provider = Mock(
        spec=PaymentProviderClient,
    )

    provider.initiate_payment.return_value = PaymentInitiationResult(
        provider_order_id="ORDER-001",
        provider_transaction_id=None,
        status=PaymentStatus.PENDING,
        redirect_url=None,
        provider_response={
            "status": "200",
        },
    )

    service = create_service(
        db_session,
        provider=provider,
    )

    service.start_payment(
        user_id=user.id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=(BillingTransactionType.SUBSCRIPTION_PURCHASE),
        customer_email=user.email,
        customer_name="Test User",
        payment_method=PaymentMethod.MPESA,
    )

    request = provider.initiate_payment.call_args.args[0]

    assert request.payment_method == PaymentMethod.MPESA


def test_start_payment_synchronizes_immediate_completed_provider_result(
    db_session,
):
    user = create_user(
        db_session,
    )

    provider = Mock(
        spec=PaymentProviderClient,
    )

    provider.initiate_payment.return_value = PaymentInitiationResult(
        provider_order_id="ORDER-001",
        provider_transaction_id="TRANSACTION-001",
        status=PaymentStatus.COMPLETED,
        redirect_url=None,
        provider_response={
            "status": "COMPLETED",
        },
    )

    service = create_service(
        db_session,
        provider=provider,
    )

    transaction, redirect_url = service.start_payment(
        user_id=user.id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=(BillingTransactionType.SUBSCRIPTION_PURCHASE),
        customer_email=user.email,
        customer_name="Test User",
        payment_method=PaymentMethod.MPESA,
    )

    assert transaction.status == PaymentStatus.COMPLETED
    assert transaction.provider_transaction_id == "TRANSACTION-001"
    assert transaction.provider_response == {
        "status": "COMPLETED",
    }
    assert redirect_url is None


def test_start_payment_synchronizes_immediate_failed_provider_result(
    db_session,
):
    user = create_user(
        db_session,
    )

    provider = Mock(
        spec=PaymentProviderClient,
    )

    provider.initiate_payment.return_value = PaymentInitiationResult(
        provider_order_id="ORDER-001",
        provider_transaction_id=None,
        status=PaymentStatus.FAILED,
        redirect_url=None,
        provider_response={
            "status": "FAILED",
        },
    )

    service = create_service(
        db_session,
        provider=provider,
    )

    transaction, _ = service.start_payment(
        user_id=user.id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=(BillingTransactionType.SUBSCRIPTION_PURCHASE),
        customer_email=user.email,
        customer_name="Test User",
        payment_method=PaymentMethod.MPESA,
    )

    assert transaction.status == PaymentStatus.FAILED
    assert transaction.provider_response == {
        "status": "FAILED",
    }


def test_start_payment_synchronizes_immediate_cancelled_provider_result(
    db_session,
):
    user = create_user(
        db_session,
    )

    provider = Mock(
        spec=PaymentProviderClient,
    )

    provider.initiate_payment.return_value = PaymentInitiationResult(
        provider_order_id="ORDER-001",
        provider_transaction_id=None,
        status=PaymentStatus.CANCELLED,
        redirect_url=None,
        provider_response={
            "status": "CANCELLED",
        },
    )

    service = create_service(
        db_session,
        provider=provider,
    )

    transaction, _ = service.start_payment(
        user_id=user.id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=(BillingTransactionType.SUBSCRIPTION_PURCHASE),
        customer_email=user.email,
        customer_name="Test User",
        payment_method=PaymentMethod.MPESA,
    )

    assert transaction.status == PaymentStatus.CANCELLED
    assert transaction.provider_response == {
        "status": "CANCELLED",
    }


def test_get_transaction_raises_for_unknown_transaction(
    db_session,
):
    service = create_service(
        db_session,
    )

    with pytest.raises(
        PaymentTransactionNotFound,
    ):
        service.get_transaction(
            uuid4(),
        )


def test_get_by_provider_order_id_returns_matching_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
        provider_order_id="ORDER-001",
    )

    result = service.get_by_provider_order_id(
        provider=PaymentProvider.PESAPAL,
        provider_order_id="ORDER-001",
    )

    assert result.id == transaction.id
    assert result.provider == PaymentProvider.PESAPAL
    assert result.provider_order_id == "ORDER-001"


def test_get_by_provider_order_id_raises_for_unknown_order(
    db_session,
):
    service = create_service(
        db_session,
    )

    with pytest.raises(
        PaymentTransactionNotFound,
    ):
        service.get_by_provider_order_id(
            provider=PaymentProvider.PESAPAL,
            provider_order_id="UNKNOWN-ORDER",
        )


def test_get_by_provider_transaction_id_returns_matching_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
        provider_order_id="ORDER-001",
    )

    service.complete_payment(
        transaction_id=transaction.id,
        provider_transaction_id="TRANSACTION-001",
    )

    result = service.get_by_provider_transaction_id(
        provider=PaymentProvider.PESAPAL,
        provider_transaction_id="TRANSACTION-001",
    )

    assert result.id == transaction.id
    assert result.provider_transaction_id == "TRANSACTION-001"


def test_get_by_provider_transaction_id_raises_for_unknown_transaction(
    db_session,
):
    service = create_service(
        db_session,
    )

    with pytest.raises(
        PaymentTransactionNotFound,
    ):
        service.get_by_provider_transaction_id(
            provider=PaymentProvider.PESAPAL,
            provider_transaction_id="UNKNOWN-TRANSACTION",
        )


def test_list_user_transactions_returns_user_transactions(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    first = initiate_transaction(
        service,
        user_id=user.id,
    )

    second = initiate_transaction(
        service,
        user_id=user.id,
    )

    results = service.list_user_transactions(
        user_id=user.id,
    )

    assert len(results) == 2
    assert {transaction.id for transaction in results} == {
        first.id,
        second.id,
    }


def test_list_user_transactions_can_filter_by_status(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    pending = initiate_transaction(
        service,
        user_id=user.id,
    )

    completed = initiate_transaction(
        service,
        user_id=user.id,
    )

    service.complete_payment(
        transaction_id=completed.id,
        provider_transaction_id="TRANSACTION-001",
    )

    results = service.list_user_transactions(
        user_id=user.id,
        status=PaymentStatus.COMPLETED,
    )

    assert len(results) == 1
    assert results[0].id == completed.id
    assert results[0].id != pending.id


# ---------------------------------------------------------------------------
# Successful lifecycle transitions
# ---------------------------------------------------------------------------


def test_complete_payment_marks_pending_transaction_as_completed(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    provider_response = {
        "status": "COMPLETED",
        "order_tracking_id": "TRACKING-001",
    }

    result = service.complete_payment(
        transaction_id=transaction.id,
        provider_transaction_id="TRANSACTION-001",
        payment_method=PaymentMethod.MPESA,
        provider_response=provider_response,
    )

    assert result.status == PaymentStatus.COMPLETED
    assert result.provider_transaction_id == "TRANSACTION-001"
    assert result.payment_method == PaymentMethod.MPESA
    assert result.provider_response == provider_response
    assert result.failure_reason is None


def test_complete_payment_can_update_only_provided_fields(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    result = service.complete_payment(
        transaction_id=transaction.id,
        provider_transaction_id="TRANSACTION-001",
    )

    assert result.status == PaymentStatus.COMPLETED
    assert result.provider_transaction_id == "TRANSACTION-001"
    assert result.payment_method == PaymentMethod.MPESA
    assert result.provider_response is None


def test_fail_payment_marks_pending_transaction_as_failed(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    provider_response = {
        "status": "FAILED",
        "error": "Payment declined",
    }

    result = service.fail_payment(
        transaction_id=transaction.id,
        failure_reason="Payment was declined",
        provider_response=provider_response,
    )

    assert result.status == PaymentStatus.FAILED
    assert result.failure_reason == "Payment was declined"
    assert result.provider_response == provider_response


def test_cancel_payment_marks_pending_transaction_as_cancelled(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    provider_response = {
        "status": "CANCELLED",
    }

    result = service.cancel_payment(
        transaction_id=transaction.id,
        provider_response=provider_response,
    )

    assert result.status == PaymentStatus.CANCELLED
    assert result.provider_response == provider_response


def test_expire_payment_marks_pending_transaction_as_expired(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    provider_response = {
        "status": "EXPIRED",
    }

    result = service.expire_payment(
        transaction_id=transaction.id,
        provider_response=provider_response,
    )

    assert result.status == PaymentStatus.EXPIRED
    assert result.provider_response == provider_response


# ---------------------------------------------------------------------------
# Invalid lifecycle transitions
# ---------------------------------------------------------------------------


def test_complete_payment_raises_for_already_completed_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    service.complete_payment(
        transaction_id=transaction.id,
        provider_transaction_id="TRANSACTION-001",
    )

    with pytest.raises(
        PaymentTransactionAlreadyCompleted,
    ):
        service.complete_payment(
            transaction_id=transaction.id,
            provider_transaction_id="TRANSACTION-002",
        )


def test_fail_payment_raises_for_completed_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    service.complete_payment(
        transaction_id=transaction.id,
        provider_transaction_id="TRANSACTION-001",
    )

    with pytest.raises(
        PaymentTransactionAlreadyCompleted,
    ):
        service.fail_payment(
            transaction_id=transaction.id,
            failure_reason="Late provider failure",
        )


def test_cancel_payment_raises_for_completed_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    service.complete_payment(
        transaction_id=transaction.id,
        provider_transaction_id="TRANSACTION-001",
    )

    with pytest.raises(
        PaymentTransactionAlreadyCompleted,
    ):
        service.cancel_payment(
            transaction_id=transaction.id,
        )


def test_expire_payment_raises_for_completed_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    service.complete_payment(
        transaction_id=transaction.id,
        provider_transaction_id="TRANSACTION-001",
    )

    with pytest.raises(
        PaymentTransactionAlreadyCompleted,
    ):
        service.expire_payment(
            transaction_id=transaction.id,
        )


def test_complete_payment_raises_for_failed_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    service.fail_payment(
        transaction_id=transaction.id,
        failure_reason="Payment declined",
    )

    with pytest.raises(
        InvalidPaymentTransactionState,
    ):
        service.complete_payment(
            transaction_id=transaction.id,
            provider_transaction_id="TRANSACTION-001",
        )


def test_complete_payment_raises_for_cancelled_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    service.cancel_payment(
        transaction_id=transaction.id,
    )

    with pytest.raises(
        InvalidPaymentTransactionState,
    ):
        service.complete_payment(
            transaction_id=transaction.id,
            provider_transaction_id="TRANSACTION-001",
        )


def test_complete_payment_raises_for_expired_transaction(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    service.expire_payment(
        transaction_id=transaction.id,
    )

    with pytest.raises(
        InvalidPaymentTransactionState,
    ):
        service.complete_payment(
            transaction_id=transaction.id,
            provider_transaction_id="TRANSACTION-001",
        )


def test_failed_transaction_cannot_be_failed_again(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    service.fail_payment(
        transaction_id=transaction.id,
        failure_reason="Payment declined",
    )

    with pytest.raises(
        InvalidPaymentTransactionState,
    ):
        service.fail_payment(
            transaction_id=transaction.id,
            failure_reason="Another failure",
        )


def test_cancelled_transaction_cannot_be_cancelled_again(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    service.cancel_payment(
        transaction_id=transaction.id,
    )

    with pytest.raises(
        InvalidPaymentTransactionState,
    ):
        service.cancel_payment(
            transaction_id=transaction.id,
        )


def test_expired_transaction_cannot_be_expired_again(
    db_session,
):
    user = create_user(
        db_session,
    )

    service = create_service(
        db_session,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
    )

    service.expire_payment(
        transaction_id=transaction.id,
    )

    with pytest.raises(
        InvalidPaymentTransactionState,
    ):
        service.expire_payment(
            transaction_id=transaction.id,
        )


# ---------------------------------------------------------------------------
# Callback Tests
# ---------------------------------------------------------------------------


def test_process_payment_callback_completes_transaction(
    db_session,
):
    user = create_user(db_session)

    provider = Mock(spec=PaymentProviderClient)

    service = create_service(
        db_session,
        provider=provider,
    )

    initiate_transaction(
        service,
        user_id=user.id,
        provider_order_id="ORDER-001",
    )

    provider.provider_type = PaymentProvider.PESAPAL

    provider.normalize_callback.return_value = PaymentCallbackResult(
        provider_order_id="ORDER-001",
        provider_transaction_id="TRACKING-001",
        status=PaymentStatus.COMPLETED,
        provider_response={},
    )

    provider.get_payment_status.return_value = PaymentStatusResult(
        provider_order_id="ORDER-001",
        provider_transaction_id="TRACKING-001",
        status=PaymentStatus.COMPLETED,
        payment_method=PaymentMethod.MPESA,
        provider_response={},
    )

    result = service.process_payment_callback(
        provider=provider,
        payload=callback_payload(),
    )

    assert result.status == PaymentStatus.COMPLETED
    assert result.provider_transaction_id == "TRACKING-001"


def test_process_payment_callback_unknown_order_raises(
    db_session,
):
    provider = Mock(spec=PaymentProviderClient)

    service = create_service(
        db_session,
        provider=provider,
    )

    provider.provider_type = PaymentProvider.PESAPAL

    provider.normalize_callback.return_value = PaymentCallbackResult(
        provider_order_id="UNKNOWN",
        provider_transaction_id="TRACKING-001",
        status=PaymentStatus.COMPLETED,
        provider_response={},
    )

    with pytest.raises(
        PaymentTransactionNotFound,
    ):
        service.process_payment_callback(
            provider=provider,
            payload={},
        )


def test_process_payment_callback_without_tracking_id_does_not_sync(
    db_session,
):
    user = create_user(db_session)

    provider = Mock(spec=PaymentProviderClient)

    service = create_service(
        db_session,
        provider=provider,
    )

    initiate_transaction(
        service,
        user_id=user.id,
        provider_order_id="ORDER-001",
    )

    provider.provider_type = PaymentProvider.PESAPAL

    provider.normalize_callback.return_value = PaymentCallbackResult(
        provider_order_id="ORDER-001",
        provider_transaction_id=None,
        status=None,
        provider_response={},
    )

    result = service.process_payment_callback(
        provider=provider,
        payload={},
    )

    assert result.status == PaymentStatus.PENDING

    provider.get_payment_status.assert_not_called()


def test_process_payment_callback_persists_tracking_id(
    db_session,
):
    user = create_user(db_session)

    provider = Mock(spec=PaymentProviderClient)

    service = create_service(
        db_session,
        provider=provider,
    )

    initiate_transaction(
        service,
        user_id=user.id,
        provider_order_id="ORDER-001",
    )

    provider.provider_type = PaymentProvider.PESAPAL

    provider.normalize_callback.return_value = PaymentCallbackResult(
        provider_order_id="ORDER-001",
        provider_transaction_id="TRACKING-999",
        status=None,
        provider_response={},
    )

    provider.get_payment_status.return_value = PaymentStatusResult(
        provider_order_id="ORDER-001",
        provider_transaction_id="TRACKING-999",
        status=PaymentStatus.PENDING,
        provider_response={},
    )

    result = service.process_payment_callback(
        provider=provider,
        payload={},
    )

    assert result.provider_transaction_id == "TRACKING-999"


def test_process_payment_callback_marks_transaction_failed(
    db_session,
):
    user = create_user(db_session)

    provider = Mock(spec=PaymentProviderClient)

    service = create_service(
        db_session,
        provider=provider,
    )

    initiate_transaction(
        service,
        user_id=user.id,
        provider_order_id="ORDER-001",
    )

    provider.provider_type = PaymentProvider.PESAPAL

    provider.normalize_callback.return_value = PaymentCallbackResult(
        provider_order_id="ORDER-001",
        provider_transaction_id="TRACKING-001",
        status=PaymentStatus.FAILED,
        provider_response={},
    )

    provider.get_payment_status.return_value = PaymentStatusResult(
        provider_order_id="ORDER-001",
        provider_transaction_id="TRACKING-001",
        status=PaymentStatus.FAILED,
        failure_reason="Declined",
        provider_response={},
    )

    result = service.process_payment_callback(
        provider=provider,
        payload={},
    )

    assert result.status == PaymentStatus.FAILED


def test_process_payment_callback_duplicate_callback_is_idempotent(
    db_session,
):
    user = create_user(db_session)

    provider = Mock(spec=PaymentProviderClient)

    service = create_service(
        db_session,
        provider=provider,
    )

    transaction = initiate_transaction(
        service,
        user_id=user.id,
        provider_order_id="ORDER-001",
    )

    service.complete_payment(
        transaction_id=transaction.id,
        provider_transaction_id="TRACKING-001",
    )

    provider.provider_type = PaymentProvider.PESAPAL

    provider.normalize_callback.return_value = PaymentCallbackResult(
        provider_order_id="ORDER-001",
        provider_transaction_id="TRACKING-001",
        status=PaymentStatus.COMPLETED,
        provider_response={},
    )

    result = service.process_payment_callback(
        provider=provider,
        payload={},
    )

    assert result.status == PaymentStatus.COMPLETED

    provider.get_payment_status.assert_not_called()


def test_process_payment_callback_prefers_status_api_over_callback(
    db_session,
):
    user = create_user(db_session)

    provider = Mock(spec=PaymentProviderClient)

    service = create_service(
        db_session,
        provider=provider,
    )

    initiate_transaction(
        service,
        user_id=user.id,
        provider_order_id="ORDER-001",
    )

    provider.provider_type = PaymentProvider.PESAPAL

    provider.normalize_callback.return_value = PaymentCallbackResult(
        provider_order_id="ORDER-001",
        provider_transaction_id="TRACKING-001",
        status=PaymentStatus.COMPLETED,
        provider_response={},
    )

    provider.get_payment_status.return_value = PaymentStatusResult(
        provider_order_id="ORDER-001",
        provider_transaction_id="TRACKING-001",
        status=PaymentStatus.FAILED,
        failure_reason="Declined",
        provider_response={},
    )

    result = service.process_payment_callback(
        provider=provider,
        payload={},
    )

    assert result.status == PaymentStatus.FAILED
