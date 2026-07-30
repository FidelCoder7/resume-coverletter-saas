from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.billing.providers.exceptions import (
    PaymentProviderResponseError,
    PaymentProviderUnsupportedOperationError,
)
from app.billing.providers.pesapal.provider import PesaPalProvider
from app.billing.providers.schemas import PaymentInitiationRequest
from app.common.constants import (
    PaymentMethod,
    PaymentStatus,
)


@pytest.fixture()
def client():
    return Mock()


@pytest.fixture()
def provider(
    client,
):
    return PesaPalProvider(
        client=client,
    )


@pytest.fixture()
def initiation_request():
    return PaymentInitiationRequest(
        provider_order_id="ORDER-001",
        amount=Decimal("1500.00"),
        currency="KES",
        description="Pro subscription",
        callback_url="https://example.com/callback",
        customer_email="user@example.com",
        customer_name="Test User",
        payment_method=PaymentMethod.MPESA,
    )


# ------------------------------------------------------------------
# Payment Initiation
# ------------------------------------------------------------------


def test_initiate_payment_submits_expected_pesapal_payload(
    provider,
    client,
    initiation_request,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.billing.providers.pesapal.provider.settings.PESAPAL_IPN_URL",
        "https://example.com/ipn",
    )

    client.submit_order.return_value = {
        "order_tracking_id": "TRACK-001",
        "redirect_url": "https://example.com/pay",
    }

    result = provider.initiate_payment(
        initiation_request,
    )

    client.submit_order.assert_called_once_with(
        payload={
            "id": "ORDER-001",
            "currency": "KES",
            "amount": 1500.0,
            "description": "Pro subscription",
            "callback_url": "https://example.com/callback",
            "notification_id": "https://example.com/ipn",
            "billing_address": {
                "email_address": "user@example.com",
                "first_name": "Test User",
            },
        },
    )

    assert result.provider_order_id == "ORDER-001"
    assert result.provider_transaction_id == "TRACK-001"
    assert result.status == PaymentStatus.PENDING
    assert result.redirect_url == "https://example.com/pay"
    assert result.provider_response == {
        "order_tracking_id": "TRACK-001",
        "redirect_url": "https://example.com/pay",
    }


def test_initiate_payment_maps_failed_provider_response_to_failed(
    provider,
    client,
    initiation_request,
):
    client.submit_order.return_value = {
        "order_tracking_id": "TRACK-001",
        "status": "Failed",
        "description": "Payment submission failed",
    }

    result = provider.initiate_payment(
        initiation_request,
    )

    assert result.status == PaymentStatus.FAILED
    assert result.provider_transaction_id == "TRACK-001"


@pytest.mark.parametrize(
    "response",
    [
        {},
        {
            "redirect_url": "https://example.com/pay",
        },
        {
            "status": "success",
        },
    ],
)
def test_initiate_payment_raises_response_error_when_tracking_id_is_missing(
    provider,
    client,
    initiation_request,
    response,
):
    client.submit_order.return_value = response

    with pytest.raises(
        PaymentProviderResponseError,
        match="order tracking ID",
    ):
        provider.initiate_payment(
            initiation_request,
        )


def test_initiate_payment_accepts_camel_case_tracking_id(
    provider,
    client,
    initiation_request,
):
    client.submit_order.return_value = {
        "orderTrackingId": "TRACK-001",
        "redirectUrl": "https://example.com/pay",
    }

    result = provider.initiate_payment(
        initiation_request,
    )

    assert result.provider_transaction_id == "TRACK-001"
    assert result.redirect_url == "https://example.com/pay"
    assert result.status == PaymentStatus.PENDING


# ------------------------------------------------------------------
# Payment Status
# ------------------------------------------------------------------


def test_get_payment_status_maps_completed_mpesa_payment(
    provider,
    client,
):
    client.get_transaction_status.return_value = {
        "payment_status_description": "Completed",
        "payment_method": "Mpesa",
        "confirmation_code": "CONFIRM-001",
    }

    result = provider.get_payment_status(
        provider_transaction_id="TRACK-001",
    )

    client.get_transaction_status.assert_called_once_with(
        provider_transaction_id="TRACK-001",
    )

    assert result.provider_transaction_id == "CONFIRM-001"
    assert result.status == PaymentStatus.COMPLETED
    assert result.payment_method == PaymentMethod.MPESA
    assert result.failure_reason == "Completed"
    assert result.provider_response == {
        "payment_status_description": "Completed",
        "payment_method": "Mpesa",
        "confirmation_code": "CONFIRM-001",
    }


@pytest.mark.parametrize(
    ("provider_status", "expected_status"),
    [
        ("Completed", PaymentStatus.COMPLETED),
        ("Complete", PaymentStatus.COMPLETED),
        ("Paid", PaymentStatus.COMPLETED),
        ("Failed", PaymentStatus.FAILED),
        ("Failure", PaymentStatus.FAILED),
        ("Rejected", PaymentStatus.FAILED),
        ("Cancelled", PaymentStatus.CANCELLED),
        ("Canceled", PaymentStatus.CANCELLED),
        ("Expired", PaymentStatus.EXPIRED),
        ("Invalid", PaymentStatus.FAILED),
        ("Pending", PaymentStatus.PENDING),
        ("Processing", PaymentStatus.PENDING),
        ("Unknown", PaymentStatus.PENDING),
    ],
)
def test_get_payment_status_maps_provider_status(
    provider,
    client,
    provider_status,
    expected_status,
):
    client.get_transaction_status.return_value = {
        "payment_status_description": provider_status,
        "confirmation_code": "CONFIRM-001",
    }

    result = provider.get_payment_status(
        provider_transaction_id="TRACK-001",
    )

    assert result.status == expected_status


@pytest.mark.parametrize(
    ("provider_method", "expected_method"),
    [
        ("Mpesa", PaymentMethod.MPESA),
        ("M-Pesa", PaymentMethod.MPESA),
        ("CARD", PaymentMethod.CARD),
        ("Visa Card", PaymentMethod.CARD),
        ("Bank", PaymentMethod.BANK),
        ("Bank Transfer", PaymentMethod.BANK),
        ("Unknown", PaymentMethod.OTHER),
    ],
)
def test_get_payment_status_maps_payment_method(
    provider,
    client,
    provider_method,
    expected_method,
):
    client.get_transaction_status.return_value = {
        "payment_status_description": "Completed",
        "payment_method": provider_method,
        "confirmation_code": "CONFIRM-001",
    }

    result = provider.get_payment_status(
        provider_transaction_id="TRACK-001",
    )

    assert result.payment_method == expected_method


def test_get_payment_status_returns_none_when_payment_method_is_missing(
    provider,
    client,
):
    client.get_transaction_status.return_value = {
        "payment_status_description": "Pending",
    }

    result = provider.get_payment_status(
        provider_transaction_id="TRACK-001",
    )

    assert result.payment_method is None


def test_get_payment_status_extracts_camel_case_transaction_id(
    provider,
    client,
):
    client.get_transaction_status.return_value = {
        "payment_status_description": "Completed",
        "confirmationCode": "CONFIRM-001",
    }

    result = provider.get_payment_status(
        provider_transaction_id="TRACK-001",
    )

    assert result.provider_transaction_id == "CONFIRM-001"


def test_get_payment_status_falls_back_to_order_tracking_id(
    provider,
    client,
):
    client.get_transaction_status.return_value = {
        "payment_status_description": "Completed",
        "order_tracking_id": "TRACK-001",
    }

    result = provider.get_payment_status(
        provider_transaction_id="TRACK-001",
    )

    assert result.provider_transaction_id == "TRACK-001"


def test_get_payment_status_extracts_failure_reason(
    provider,
    client,
):
    client.get_transaction_status.return_value = {
        "payment_status_description": "Failed",
        "description": "Insufficient funds",
    }

    result = provider.get_payment_status(
        provider_transaction_id="TRACK-001",
    )

    assert result.status == PaymentStatus.FAILED
    assert result.failure_reason == "Failed"


# ------------------------------------------------------------------
# Payment Cancellation
# ------------------------------------------------------------------


def test_cancel_payment_raises_unsupported_operation_error(
    provider,
):
    with pytest.raises(
        PaymentProviderUnsupportedOperationError,
        match="cancellation is not supported",
    ):
        provider.cancel_payment(
            provider_order_id="ORDER-001",
        )


# ------------------------------------------------------------------
# Provider Client Delegation
# ------------------------------------------------------------------


def test_provider_uses_injected_pesapal_client(
    client,
):
    provider = PesaPalProvider(
        client=client,
    )

    assert provider.client is client
