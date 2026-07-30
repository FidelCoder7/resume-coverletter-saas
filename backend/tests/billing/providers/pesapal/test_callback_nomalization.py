import pytest

from app.billing.exceptions import InvalidPaymentCallback
from app.billing.providers.pesapal.provider import PesaPalProvider
from app.common.constants import PaymentStatus


def create_provider() -> PesaPalProvider:
    """
    Construct a PesaPal provider without exercising the HTTP client.

    normalize_callback() is pure logic and does not use the client.
    """
    return PesaPalProvider()


def callback_payload(
    *,
    merchant_reference: str = "ORDER-001",
    tracking_id: str | None = "TRACKING-001",
    notification_type: str | None = "COMPLETED",
):
    payload = {
        "OrderMerchantReference": merchant_reference,
    }

    if tracking_id is not None:
        payload["OrderTrackingId"] = tracking_id

    if notification_type is not None:
        payload["OrderNotificationType"] = notification_type

    return payload


# ---------------------------------------------------------------------------
# Successful normalization
# ---------------------------------------------------------------------------


def test_normalize_callback_returns_expected_result():
    provider = create_provider()

    result = provider.normalize_callback(
        callback_payload(),
    )

    assert result.provider_order_id == "ORDER-001"
    assert result.provider_transaction_id == "TRACKING-001"
    assert result.status == PaymentStatus.COMPLETED
    assert result.provider_response == callback_payload()


def test_normalize_callback_accepts_missing_tracking_id():
    provider = create_provider()

    result = provider.normalize_callback(
        callback_payload(
            tracking_id=None,
        ),
    )

    assert result.provider_order_id == "ORDER-001"
    assert result.provider_transaction_id is None
    assert result.status == PaymentStatus.COMPLETED


def test_normalize_callback_accepts_missing_status():
    provider = create_provider()

    result = provider.normalize_callback(
        callback_payload(
            notification_type=None,
        ),
    )

    assert result.provider_order_id == "ORDER-001"
    assert result.provider_transaction_id == "TRACKING-001"
    assert result.status is None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def test_normalize_callback_requires_merchant_reference():
    provider = create_provider()

    with pytest.raises(
        InvalidPaymentCallback,
    ):
        provider.normalize_callback(
            {
                "OrderTrackingId": "TRACKING-001",
            },
        )


# ---------------------------------------------------------------------------
# Status mapping
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("provider_status", "expected"),
    [
        ("COMPLETED", PaymentStatus.COMPLETED),
        ("Complete", PaymentStatus.COMPLETED),
        ("PAID", PaymentStatus.COMPLETED),
        ("FAILED", PaymentStatus.FAILED),
        ("Failure", PaymentStatus.FAILED),
        ("REJECTED", PaymentStatus.FAILED),
        ("CANCELLED", PaymentStatus.CANCELLED),
        ("Canceled", PaymentStatus.CANCELLED),
        ("EXPIRED", PaymentStatus.EXPIRED),
    ],
)
def test_normalize_callback_maps_statuses(
    provider_status,
    expected,
):
    provider = create_provider()

    result = provider.normalize_callback(
        callback_payload(
            notification_type=provider_status,
        ),
    )

    assert result.status == expected


def test_normalize_callback_unknown_status_returns_none():
    provider = create_provider()

    result = provider.normalize_callback(
        callback_payload(
            notification_type="SOMETHING_NEW",
        ),
    )

    assert result.status is None


# ---------------------------------------------------------------------------
# PaymentStatus fallback
# ---------------------------------------------------------------------------


def test_normalize_callback_uses_payment_status_when_notification_missing():
    provider = create_provider()

    payload = {
        "OrderMerchantReference": "ORDER-001",
        "OrderTrackingId": "TRACKING-001",
        "PaymentStatus": "FAILED",
    }

    result = provider.normalize_callback(
        payload,
    )

    assert result.status == PaymentStatus.FAILED


# ---------------------------------------------------------------------------
# Identifier normalization
# ---------------------------------------------------------------------------


def test_normalize_callback_converts_tracking_id_to_string():
    provider = create_provider()

    result = provider.normalize_callback(
        callback_payload(
            tracking_id=123456789,
        ),
    )

    assert result.provider_transaction_id == "123456789"


def test_normalize_callback_converts_reference_to_string():
    provider = create_provider()

    result = provider.normalize_callback(
        callback_payload(
            merchant_reference=987654321,
        ),
    )

    assert result.provider_order_id == "987654321"
