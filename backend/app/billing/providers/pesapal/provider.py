from typing import Any

from app.billing.exceptions import InvalidPaymentCallback
from app.billing.providers.base import PaymentProvider
from app.billing.providers.exceptions import (
    PaymentProviderResponseError,
    PaymentProviderUnsupportedOperationError,
)
from app.billing.providers.pesapal.client import PesaPalClient
from app.billing.providers.schemas import (
    PaymentCallbackResult,
    PaymentCancellationResult,
    PaymentInitiationRequest,
    PaymentInitiationResult,
    PaymentStatusResult,
)
from app.common.constants import (
    PaymentMethod,
    PaymentStatus,
)
from app.common.constants import PaymentProvider as PaymentProviderType
from app.core.config import settings


class PesaPalProvider(PaymentProvider):
    """
    PesaPal implementation of the provider-agnostic payment contract.

    This class translates application-level payment requests and
    PesaPal-specific API responses into provider-agnostic schemas.
    """

    def __init__(
        self,
        client: PesaPalClient | None = None,
    ) -> None:
        self.client = client or PesaPalClient()

    @property
    def provider_type(self) -> PaymentProviderType:
        """
        Return the application-level provider identity.
        """

        return PaymentProviderType.PESAPAL

    def initiate_payment(
        self,
        request: PaymentInitiationRequest,
    ) -> PaymentInitiationResult:
        """
        Initiate a payment through PesaPal.
        """

        payload = {
            "id": request.provider_order_id,
            "currency": request.currency or settings.PESAPAL_DEFAULT_CURRENCY,
            "amount": float(request.amount),
            "description": request.description,
            "callback_url": request.callback_url,
            "notification_id": settings.PESAPAL_IPN_URL,
            "billing_address": {
                "email_address": request.customer_email,
                "first_name": request.customer_name,
            },
        }

        response = self.client.submit_order(
            payload=payload,
        )

        order_tracking_id = response.get(
            "order_tracking_id",
        )

        if order_tracking_id is None:
            order_tracking_id = response.get(
                "orderTrackingId",
            )

        redirect_url = response.get(
            "redirect_url",
        )

        if redirect_url is None:
            redirect_url = response.get(
                "redirectUrl",
            )

        if not order_tracking_id:
            raise PaymentProviderResponseError(
                "PesaPal order submission response did not contain "
                "an order tracking ID.",
            )

        status = self._map_initiation_status(
            response,
        )

        return PaymentInitiationResult(
            provider_order_id=request.provider_order_id,
            provider_transaction_id=str(
                order_tracking_id,
            ),
            status=status,
            redirect_url=redirect_url,
            provider_response=response,
        )

    def get_payment_status(
        self,
        *,
        provider_transaction_id: str,
    ) -> PaymentStatusResult:
        """
        Retrieve and normalize payment status from PesaPal.
        """

        response = self.client.get_transaction_status(
            provider_transaction_id=provider_transaction_id,
        )

        provider_transaction_id = self._extract_transaction_id(
            response,
        )

        status = self._map_payment_status(
            response,
        )

        payment_method = self._map_payment_method(
            response,
        )

        failure_reason = self._extract_failure_reason(
            response,
        )

        return PaymentStatusResult(
            provider_order_id=response.get(
                "merchant_reference",
            ),
            provider_transaction_id=provider_transaction_id,
            status=status,
            payment_method=payment_method,
            failure_reason=failure_reason,
            provider_response=response,
        )

    def normalize_callback(
        self,
        payload: dict[str, Any],
    ) -> PaymentCallbackResult:
        """
        Normalize a PesaPal IPN callback payload.

        PesaPal identifies the application transaction using
        OrderMerchantReference and identifies the PesaPal payment
        using OrderTrackingId.
        """

        provider_order_id = payload.get(
            "OrderMerchantReference",
        )

        if not provider_order_id:
            raise InvalidPaymentCallback(
                "PesaPal callback is missing OrderMerchantReference.",
            )

        provider_transaction_id = payload.get(
            "OrderTrackingId",
        )

        if provider_transaction_id is not None:
            provider_transaction_id = str(
                provider_transaction_id,
            )

        status = self._map_callback_status(
            payload,
        )

        return PaymentCallbackResult(
            provider_order_id=str(
                provider_order_id,
            ),
            provider_transaction_id=provider_transaction_id,
            status=status,
            provider_response=payload,
        )

    @staticmethod
    def _map_callback_status(
        payload: dict[str, Any],
    ) -> PaymentStatus | None:
        """
        Map a PesaPal callback status to the application payment status.

        The callback status is informational only. The application
        subsequently retrieves the authoritative status from the
        PesaPal transaction status API.
        """

        status = payload.get(
            "OrderNotificationType",
        )

        if status is None:
            status = payload.get(
                "PaymentStatus",
            )

        if status is None:
            return None

        normalized = str(status).strip().lower()

        status_mapping = {
            "completed": PaymentStatus.COMPLETED,
            "complete": PaymentStatus.COMPLETED,
            "paid": PaymentStatus.COMPLETED,
            "failed": PaymentStatus.FAILED,
            "failure": PaymentStatus.FAILED,
            "rejected": PaymentStatus.FAILED,
            "cancelled": PaymentStatus.CANCELLED,
            "canceled": PaymentStatus.CANCELLED,
            "expired": PaymentStatus.EXPIRED,
        }

        return status_mapping.get(
            normalized,
        )

    @staticmethod
    def _extract_callback_order_tracking_id(
        payload: dict[str, Any],
    ) -> str | None:
        """
        Extract the PesaPal order tracking ID from a callback payload.
        """

        value = payload.get(
            "OrderTrackingId",
        )

        if value is None:
            value = payload.get(
                "orderTrackingId",
            )

        if value is None:
            value = payload.get(
                "order_tracking_id",
            )

        if value is None:
            return None

        value = str(value).strip()

        return value or None

    @staticmethod
    def _extract_callback_order_reference(
        payload: dict[str, Any],
    ) -> str | None:
        """
        Extract the merchant order reference used when the payment
        was originally initiated.
        """

        value = payload.get(
            "OrderMerchantReference",
        )

        if value is None:
            value = payload.get(
                "orderMerchantReference",
            )

        if value is None:
            value = payload.get(
                "order_merchant_reference",
            )

        if value is None:
            value = payload.get(
                "merchant_reference",
            )

        if value is None:
            value = payload.get(
                "merchantReference",
            )

        if value is None:
            return None

        value = str(value).strip()

        return value or None

    def cancel_payment(
        self,
        *,
        provider_order_id: str,
    ) -> PaymentCancellationResult:
        """
        Cancel a payment.

        PesaPal cancellation is not currently supported by the
        provider adapter.
        """

        raise PaymentProviderUnsupportedOperationError(
            "PesaPal payment cancellation is not supported "
            "by the current provider integration.",
        )

    @staticmethod
    def _map_initiation_status(
        response: dict[str, Any],
    ) -> PaymentStatus:
        """
        Map the PesaPal order submission response to an application
        payment status.

        A successfully submitted order is considered PENDING until
        PesaPal confirms the final payment status.
        """

        status = str(
            response.get(
                "status",
                "",
            ),
        ).lower()

        if status in {
            "failed",
            "error",
            "rejected",
        }:
            return PaymentStatus.FAILED

        return PaymentStatus.PENDING

    @staticmethod
    def _map_payment_status(
        response: dict[str, Any],
    ) -> PaymentStatus:
        """
        Map PesaPal transaction status values to application status.
        """

        status = (
            str(
                response.get(
                    "payment_status_description",
                    response.get(
                        "status",
                        "",
                    ),
                ),
            )
            .strip()
            .lower()
        )

        status_mapping = {
            "completed": PaymentStatus.COMPLETED,
            "complete": PaymentStatus.COMPLETED,
            "paid": PaymentStatus.COMPLETED,
            "failed": PaymentStatus.FAILED,
            "failure": PaymentStatus.FAILED,
            "rejected": PaymentStatus.FAILED,
            "cancelled": PaymentStatus.CANCELLED,
            "canceled": PaymentStatus.CANCELLED,
            "expired": PaymentStatus.EXPIRED,
            "invalid": PaymentStatus.FAILED,
        }

        return status_mapping.get(
            status,
            PaymentStatus.PENDING,
        )

    @staticmethod
    def _extract_transaction_id(
        response: dict[str, Any],
    ) -> str | None:
        """
        Extract the provider transaction identifier.
        """

        transaction_id = response.get(
            "confirmation_code",
        )

        if transaction_id is None:
            transaction_id = response.get(
                "confirmationCode",
            )

        if transaction_id is None:
            transaction_id = response.get(
                "order_tracking_id",
            )

        if transaction_id is None:
            transaction_id = response.get(
                "orderTrackingId",
            )

        if transaction_id is None:
            return None

        return str(transaction_id)

    @staticmethod
    def _map_payment_method(
        response: dict[str, Any],
    ) -> PaymentMethod | None:
        """
        Map a PesaPal payment method to the application's enum.
        """

        method = response.get(
            "payment_method",
        )

        if method is None:
            method = response.get(
                "paymentMethod",
            )

        if method is None:
            return None

        normalized = str(method).strip().lower().replace("-", "").replace(" ", "")

        if "mpesa" in normalized:
            return PaymentMethod.MPESA

        if "card" in normalized:
            return PaymentMethod.CARD

        if "bank" in normalized:
            return PaymentMethod.BANK

        return PaymentMethod.OTHER

    @staticmethod
    def _extract_failure_reason(
        response: dict[str, Any],
    ) -> str | None:
        """
        Extract a failure reason from a PesaPal response.
        """

        for key in (
            "payment_status_description",
            "description",
            "message",
            "error",
        ):
            value = response.get(key)

            if value:
                return str(value)

        return None
