from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.common.constants import (
    BillingTransactionType,
    PaymentMethod,
    PaymentProvider,
    PaymentStatus,
    SubscriptionPlan,
)


class PaymentInitiationRequest(BaseModel):
    """
    Request payload for initiating a subscription payment.

    The subscription plan is used by the application to resolve the
    authoritative server-side price.

    User identity, customer contact information, payment amount,
    currency, and provider identity are controlled by the application
    and are not accepted from the client.
    """

    subscription_plan: SubscriptionPlan

    transaction_type: BillingTransactionType = (
        BillingTransactionType.SUBSCRIPTION_PURCHASE
    )

    payment_method: PaymentMethod | None = None


class PaymentTransactionResponse(BaseModel):
    """
    API representation of a payment transaction.
    """

    id: UUID
    user_id: UUID
    subscription_plan: SubscriptionPlan
    transaction_type: BillingTransactionType
    provider: PaymentProvider
    provider_order_id: str
    provider_transaction_id: str | None
    amount: Decimal
    currency: str
    payment_method: PaymentMethod | None
    status: PaymentStatus
    failure_reason: str | None
    provider_response: dict | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class PaymentInitiationResponse(BaseModel):
    """
    Response returned after initiating a payment.
    """

    transaction: PaymentTransactionResponse
    redirect_url: str | None


class PaymentTransactionListResponse(BaseModel):
    """
    Response containing the authenticated user's payment transactions.
    """

    transactions: list[PaymentTransactionResponse]


class PaymentStatusResponse(BaseModel):
    """
    Response returned after synchronizing a payment status.
    """

    transaction: PaymentTransactionResponse
