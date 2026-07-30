from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from app.common.constants import PaymentMethod, PaymentStatus


@dataclass(frozen=True)
class PaymentInitiationRequest:
    """
    Provider-agnostic payment initiation request.

    This object contains the information required to initiate
    a payment with any supported payment provider.
    """

    provider_order_id: str
    amount: Decimal
    currency: str
    description: str
    callback_url: str
    customer_email: str
    customer_name: str
    payment_method: PaymentMethod | None = None


@dataclass(frozen=True)
class PaymentInitiationResult:
    """
    Provider-agnostic result returned after initiating a payment.
    """

    provider_order_id: str
    provider_transaction_id: str | None
    status: PaymentStatus
    redirect_url: str | None = None
    provider_response: dict[str, Any] | None = None


@dataclass(frozen=True)
class PaymentStatusResult:
    """
    Provider-agnostic payment status result.
    """

    provider_order_id: str | None
    provider_transaction_id: str | None
    status: PaymentStatus
    payment_method: PaymentMethod | None = None
    failure_reason: str | None = None
    provider_response: dict[str, Any] | None = None


@dataclass(frozen=True)
class PaymentCancellationResult:
    """
    Provider-agnostic result returned after a payment cancellation.
    """

    provider_order_id: str
    provider_transaction_id: str | None
    status: PaymentStatus
    provider_response: dict[str, Any] | None = None


@dataclass(frozen=True)
class PaymentCallbackResult:
    """
    Provider-agnostic result returned after processing a provider
    callback or webhook notification.

    The callback identifies the payment using the provider-specific
    order tracking ID and merchant reference. The application then
    uses those identifiers to locate and synchronize the local
    payment transaction.
    """

    provider_order_id: str
    provider_transaction_id: str | None
    status: PaymentStatus | None
    provider_response: dict[str, Any] | None = None
