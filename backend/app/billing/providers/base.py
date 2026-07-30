from abc import ABC, abstractmethod
from typing import Any

from app.billing.providers.schemas import (
    PaymentCallbackResult,
    PaymentCancellationResult,
    PaymentInitiationRequest,
    PaymentInitiationResult,
    PaymentStatusResult,
)
from app.common.constants import PaymentProvider as PaymentProviderType


class PaymentProvider(ABC):
    """
    Abstract contract for payment provider integrations.

    Implementations of this interface are responsible for translating
    provider-specific APIs into the application's provider-agnostic
    payment contract.

    Billing business logic must depend on this abstraction rather than
    directly depending on a specific payment provider such as PesaPal.
    """

    @property
    @abstractmethod
    def provider_type(self) -> PaymentProviderType:
        """
        Return the application-level identity of this payment provider.
        """

        raise NotImplementedError

    @abstractmethod
    def initiate_payment(
        self,
        request: PaymentInitiationRequest,
    ) -> PaymentInitiationResult:
        """
        Initiate a payment with the provider.
        """

        raise NotImplementedError

    @abstractmethod
    def get_payment_status(
        self,
        *,
        provider_transaction_id: str,
    ) -> PaymentStatusResult:
        """
        Retrieve the current payment status from the provider.
        """

        raise NotImplementedError

    @abstractmethod
    def normalize_callback(
        self,
        *,
        payload: dict[str, Any],
    ) -> PaymentCallbackResult:
        """
        Process and normalize a provider callback or webhook payload.

        Provider-specific callback formats must be translated into
        the provider-agnostic callback result.
        """

        raise NotImplementedError

    @abstractmethod
    def cancel_payment(
        self,
        *,
        provider_order_id: str,
    ) -> PaymentCancellationResult:
        """
        Cancel a payment with the provider.

        Providers that don't support cancellation should raise the
        appropriate provider-specific unsupported-operation exception.
        """

        raise NotImplementedError
