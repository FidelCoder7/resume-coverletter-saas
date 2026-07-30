from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.billing.exceptions import (
    InvalidPaymentCallback,
    InvalidSubscriptionPaymentPlan,
    PaymentTransactionNotFound,
)
from app.billing.models import PaymentTransaction
from app.billing.router import (
    get_payment_transaction,
    initiate_payment,
    list_payment_transactions,
    payment_callback,
    synchronize_payment_status,
)
from app.billing.schemas import (
    PaymentInitiationRequest,
    PaymentInitiationResponse,
    PaymentStatusResponse,
    PaymentTransactionListResponse,
    PaymentTransactionResponse,
)
from app.billing.service import PaymentTransactionService
from app.common.constants import (
    BillingTransactionType,
    PaymentMethod,
    PaymentProvider,
    PaymentStatus,
    SubscriptionPlan,
)
from app.users.models import User


def create_user() -> Mock:
    """
    Create a lightweight mock user for router tests.
    """

    user = Mock(
        spec=User,
    )

    user.id = uuid4()
    user.email = "test@example.com"
    user.full_name = "Test User"

    return user


def create_transaction(
    *,
    user_id,
    status: PaymentStatus = PaymentStatus.PENDING,
) -> Mock:
    """
    Create a lightweight mock payment transaction for router tests.
    """

    transaction = Mock(
        spec=PaymentTransaction,
    )

    transaction.id = uuid4()
    transaction.user_id = user_id
    transaction.subscription_plan = SubscriptionPlan.PRO
    transaction.transaction_type = BillingTransactionType.SUBSCRIPTION_PURCHASE
    transaction.provider = PaymentProvider.PESAPAL
    transaction.provider_order_id = "ORDER-001"
    transaction.provider_transaction_id = "TRANSACTION-001"
    transaction.amount = Decimal("1000.00")
    transaction.currency = "KES"
    transaction.payment_method = PaymentMethod.MPESA
    transaction.status = status
    transaction.failure_reason = None
    transaction.provider_response = {
        "status": status.value,
    }

    return transaction


def create_callback_payload():
    return {
        "OrderTrackingId": "TRACKING-001",
        "OrderMerchantReference": "ORDER-001",
        "OrderNotificationType": "COMPLETED",
    }


# ---------------------------------------------------------------------------

# POST /billing/payments/callback

# ---------------------------------------------------------------------------


def test_initiate_payment_returns_payment_response():
    """
    Initiating a valid subscription payment should delegate to the
    payment transaction service and return the created transaction
    together with the provider redirect URL.
    """

    user = create_user()

    service = Mock(
        spec=PaymentTransactionService,
    )

    transaction = create_transaction(
        user_id=user.id,
        status=PaymentStatus.PENDING,
    )

    service.start_payment.return_value = (
        transaction,
        "https://pay.example.com/checkout",
    )

    payload = PaymentInitiationRequest(
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=(BillingTransactionType.SUBSCRIPTION_PURCHASE),
        payment_method=PaymentMethod.MPESA,
    )

    result = initiate_payment(
        payload=payload,
        current_user=user,
        service=service,
        payment_provider=Mock(),
    )

    assert isinstance(
        result,
        PaymentInitiationResponse,
    )

    assert result.transaction.id == transaction.id
    assert result.transaction.user_id == user.id
    assert result.transaction.subscription_plan == SubscriptionPlan.PRO
    assert result.transaction.status == PaymentStatus.PENDING
    assert result.redirect_url == "https://pay.example.com/checkout"

    service.start_payment.assert_called_once_with(
        user_id=user.id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=(BillingTransactionType.SUBSCRIPTION_PURCHASE),
        customer_email=user.email,
        customer_name=user.full_name,
        payment_method=PaymentMethod.MPESA,
    )


def test_initiate_payment_rejects_free_subscription_plan():
    """
    The FREE plan must not initiate a payment transaction.
    """

    user = create_user()

    service = Mock(
        spec=PaymentTransactionService,
    )

    payload = PaymentInitiationRequest(
        subscription_plan=SubscriptionPlan.FREE,
        transaction_type=(BillingTransactionType.SUBSCRIPTION_PURCHASE),
        payment_method=PaymentMethod.MPESA,
    )

    with pytest.raises(
        InvalidSubscriptionPaymentPlan,
    ):
        initiate_payment(
            payload=payload,
            current_user=user,
            service=service,
            payment_provider=Mock(),
        )

    service.start_payment.assert_not_called()


def test_initiate_payment_passes_authenticated_user_information_to_service():
    """
    The authenticated user's email and full name should come from the
    authenticated user and not from the client request.
    """

    user = create_user()

    service = Mock(
        spec=PaymentTransactionService,
    )

    transaction = create_transaction(
        user_id=user.id,
    )

    service.start_payment.return_value = (
        transaction,
        None,
    )

    payload = PaymentInitiationRequest(
        subscription_plan=SubscriptionPlan.PRO,
    )

    initiate_payment(
        payload=payload,
        current_user=user,
        service=service,
        payment_provider=Mock(),
    )

    service.start_payment.assert_called_once_with(
        user_id=user.id,
        subscription_plan=SubscriptionPlan.PRO,
        transaction_type=(BillingTransactionType.SUBSCRIPTION_PURCHASE),
        customer_email=user.email,
        customer_name=user.full_name,
        payment_method=None,
    )


def test_payment_callback_processes_valid_callback():
    """
    A valid provider callback should be delegated to the payment
    transaction service and acknowledge receipt.
    """

    service = Mock(
        spec=PaymentTransactionService,
    )

    provider = Mock()

    payload = create_callback_payload()

    result = payment_callback(
        payload=payload,
        service=service,
        payment_provider=provider,
    )

    assert result == {
        "status": "received",
    }

    service.process_payment_callback.assert_called_once_with(
        provider=provider,
        payload=payload,
    )


def test_payment_callback_propagates_unknown_transaction():
    """
    Unknown merchant references should be delegated to the service,
    which is responsible for resolving transactions.
    """

    service = Mock(
        spec=PaymentTransactionService,
    )

    provider = Mock()

    service.process_payment_callback.side_effect = PaymentTransactionNotFound(
        "Unknown transaction",
    )

    with pytest.raises(
        PaymentTransactionNotFound,
    ):
        payment_callback(
            payload=create_callback_payload(),
            service=service,
            payment_provider=provider,
        )


def test_payment_callback_accepts_callback_without_tracking_id():
    """
    A callback without OrderTrackingId should still be passed to the
    service because some providers deliver tracking information later.
    """

    service = Mock(
        spec=PaymentTransactionService,
    )

    provider = Mock()

    payload = {
        "OrderMerchantReference": "ORDER-001",
    }

    result = payment_callback(
        payload=payload,
        service=service,
        payment_provider=provider,
    )

    assert result == {
        "status": "received",
    }

    service.process_payment_callback.assert_called_once_with(
        provider=provider,
        payload=payload,
    )


def test_payment_callback_propagates_invalid_callback():
    """
    Invalid callbacks should propagate the validation error from the
    billing service.
    """

    service = Mock(
        spec=PaymentTransactionService,
    )

    provider = Mock()

    service.process_payment_callback.side_effect = InvalidPaymentCallback(
        "Missing merchant reference",
    )

    with pytest.raises(
        InvalidPaymentCallback,
    ):
        payment_callback(
            payload={
                "OrderTrackingId": "TRACKING-001",
            },
            service=service,
            payment_provider=provider,
        )


def test_payment_callback_completed_transaction():
    """
    Completed callbacks should still return a successful HTTP payload
    after the service processes them.
    """

    service = Mock(
        spec=PaymentTransactionService,
    )

    provider = Mock()

    payload = create_callback_payload()

    payment_callback(
        payload=payload,
        service=service,
        payment_provider=provider,
    )

    service.process_payment_callback.assert_called_once()


def test_payment_callback_failed_transaction():
    """
    Failed callbacks are processed identically by the router.
    """

    service = Mock(
        spec=PaymentTransactionService,
    )

    provider = Mock()

    payload = create_callback_payload()

    payload["OrderNotificationType"] = "FAILED"

    result = payment_callback(
        payload=payload,
        service=service,
        payment_provider=provider,
    )

    assert result == {
        "status": "received",
    }

    service.process_payment_callback.assert_called_once_with(
        provider=provider,
        payload=payload,
    )


def test_payment_callback_duplicate_callback():
    """
    Duplicate callbacks should simply be delegated to the billing
    service. Idempotency is enforced by the service layer.
    """

    service = Mock(
        spec=PaymentTransactionService,
    )

    provider = Mock()

    payload = create_callback_payload()

    payment_callback(
        payload=payload,
        service=service,
        payment_provider=provider,
    )

    payment_callback(
        payload=payload,
        service=service,
        payment_provider=provider,
    )

    assert service.process_payment_callback.call_count == 2


# ---------------------------------------------------------------------------

# GET /billing/transactions

# ---------------------------------------------------------------------------


def test_list_payment_transactions_returns_user_transactions():
    """
    The authenticated user's payment transactions should be returned
    as a PaymentTransactionListResponse.
    """

    user = create_user()

    service = Mock(
        spec=PaymentTransactionService,
    )

    first = create_transaction(
        user_id=user.id,
        status=PaymentStatus.PENDING,
    )

    second = create_transaction(
        user_id=user.id,
        status=PaymentStatus.COMPLETED,
    )

    service.list_user_transactions.return_value = [
        first,
        second,
    ]

    result = list_payment_transactions(
        status_filter=None,
        current_user=user,
        service=service,
    )

    assert isinstance(
        result,
        PaymentTransactionListResponse,
    )

    assert len(result.transactions) == 2
    assert result.transactions[0].id == first.id
    assert result.transactions[1].id == second.id

    service.list_user_transactions.assert_called_once_with(
        user_id=user.id,
        status=None,
    )


def test_list_payment_transactions_filters_by_status():
    """
    The optional status query parameter should be passed to the
    payment transaction service.
    """

    user = create_user()

    service = Mock(
        spec=PaymentTransactionService,
    )

    transaction = create_transaction(
        user_id=user.id,
        status=PaymentStatus.COMPLETED,
    )

    service.list_user_transactions.return_value = [
        transaction,
    ]

    result = list_payment_transactions(
        status_filter=PaymentStatus.COMPLETED,
        current_user=user,
        service=service,
    )

    assert isinstance(
        result,
        PaymentTransactionListResponse,
    )

    assert len(result.transactions) == 1
    assert result.transactions[0].status == PaymentStatus.COMPLETED

    service.list_user_transactions.assert_called_once_with(
        user_id=user.id,
        status=PaymentStatus.COMPLETED,
    )

    # ---------------------------------------------------------------------------

    # GET /billing/transactions/{transaction_id}

    # ---------------------------------------------------------------------------


def test_get_payment_transaction_returns_owned_transaction():
    """
    An authenticated user should be able to retrieve their own
    payment transaction.
    """

    user = create_user()

    service = Mock(
        spec=PaymentTransactionService,
    )

    transaction = create_transaction(
        user_id=user.id,
    )

    service.get_transaction.return_value = transaction

    result = get_payment_transaction(
        transaction_id=transaction.id,
        current_user=user,
        service=service,
    )

    assert isinstance(
        result,
        PaymentTransactionResponse,
    )

    assert result.id == transaction.id
    assert result.user_id == user.id

    service.get_transaction.assert_called_once_with(
        transaction.id,
    )


def test_get_payment_transaction_returns_404_for_other_users_transaction():
    """
    A transaction owned by another user should be reported as not
    found to avoid exposing resource existence.
    """

    authenticated_user = create_user()
    transaction_owner = create_user()

    service = Mock(
        spec=PaymentTransactionService,
    )

    transaction = create_transaction(
        user_id=transaction_owner.id,
    )

    service.get_transaction.return_value = transaction

    with pytest.raises(
        HTTPException,
    ) as exc_info:
        get_payment_transaction(
            transaction_id=transaction.id,
            current_user=authenticated_user,
            service=service,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Payment transaction not found."


# ---------------------------------------------------------------------------

# GET /billing/transactions/{transaction_id}/status

# ---------------------------------------------------------------------------


def test_synchronize_payment_status_returns_synchronized_transaction():
    """
    An authenticated transaction owner should be able to synchronize
    the payment status with the provider.
    """

    user = create_user()

    service = Mock(
        spec=PaymentTransactionService,
    )

    pending_transaction = create_transaction(
        user_id=user.id,
        status=PaymentStatus.PENDING,
    )

    completed_transaction = create_transaction(
        user_id=user.id,
        status=PaymentStatus.COMPLETED,
    )

    completed_transaction.id = pending_transaction.id

    service.get_transaction.return_value = pending_transaction

    service.synchronize_payment_status.return_value = completed_transaction

    result = synchronize_payment_status(
        transaction_id=pending_transaction.id,
        current_user=user,
        service=service,
    )

    assert isinstance(
        result,
        PaymentStatusResponse,
    )

    assert result.transaction.id == pending_transaction.id

    assert result.transaction.status == PaymentStatus.COMPLETED

    service.get_transaction.assert_called_once_with(
        pending_transaction.id,
    )

    service.synchronize_payment_status.assert_called_once_with(
        transaction_id=pending_transaction.id,
    )


def test_synchronize_payment_status_returns_404_for_other_users_transaction():
    """
    A user must not be able to synchronize another user's payment
    transaction.
    """

    authenticated_user = create_user()
    transaction_owner = create_user()

    service = Mock(
        spec=PaymentTransactionService,
    )

    transaction = create_transaction(
        user_id=transaction_owner.id,
        status=PaymentStatus.PENDING,
    )

    service.get_transaction.return_value = transaction

    with pytest.raises(
        HTTPException,
    ) as exc_info:
        synchronize_payment_status(
            transaction_id=transaction.id,
            current_user=authenticated_user,
            service=service,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Payment transaction not found."

    service.synchronize_payment_status.assert_not_called()
