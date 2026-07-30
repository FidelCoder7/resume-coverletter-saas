from typing import Any

import requests

from app.billing.providers.exceptions import (
    PaymentProviderAuthenticationError,
    PaymentProviderCommunicationError,
    PaymentProviderConfigurationError,
    PaymentProviderOperationError,
    PaymentProviderRequestError,
    PaymentProviderResponseError,
)
from app.core.config import settings


class PesaPalClient:
    """
    Low-level HTTP client for the PesaPal API.

    This client is responsible only for communicating with PesaPal.
    Provider-agnostic payment translation belongs to PesaPalProvider.
    """

    def __init__(
        self,
        *,
        consumer_key: str | None = None,
        consumer_secret: str | None = None,
        timeout: int | None = None,
        oauth_url: str | None = None,
        order_submission_url: str | None = None,
        order_status_url: str | None = None,
    ) -> None:
        self.consumer_key = (
            consumer_key if consumer_key is not None else settings.PESAPAL_CONSUMER_KEY
        )

        self.consumer_secret = (
            consumer_secret
            if consumer_secret is not None
            else settings.PESAPAL_CONSUMER_SECRET
        )

        self.timeout = timeout if timeout is not None else settings.PESAPAL_TIMEOUT
        self.oauth_url = (
            oauth_url if oauth_url is not None else settings.PESAPAL_OAUTH_URL
        )

        self.order_submission_url = (
            order_submission_url
            if order_submission_url is not None
            else settings.PESAPAL_ORDER_SUBMISSION_URL
        )

        self.order_status_url = (
            order_status_url
            if order_status_url is not None
            else settings.PESAPAL_ORDER_STATUS_URL
        )

        self._access_token: str | None = None

    def authenticate(self) -> str:
        """
        Obtain an OAuth access token from PesaPal.

        Returns:
            A valid PesaPal access token.

        Raises:
            PaymentProviderConfigurationError:
                If required credentials are missing.

            PaymentProviderAuthenticationError:
                If PesaPal rejects authentication.

            PaymentProviderCommunicationError:
                If communication with PesaPal fails.

            PaymentProviderResponseError:
                If the authentication response is invalid.
        """

        if not self.consumer_key or not self.consumer_secret:
            raise PaymentProviderConfigurationError(
                "PesaPal consumer credentials are not configured.",
            )

        payload = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret,
        }

        try:
            response = requests.post(
                self.oauth_url,
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise PaymentProviderCommunicationError(
                "Failed to communicate with PesaPal authentication API.",
            ) from exc

        if response.status_code in {401, 403}:
            raise PaymentProviderAuthenticationError(
                "PesaPal authentication failed.",
            )

        if not response.ok:
            raise PaymentProviderAuthenticationError(
                "PesaPal authentication request was rejected "
                f"with status {response.status_code}.",
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise PaymentProviderResponseError(
                "PesaPal authentication returned invalid JSON.",
            ) from exc

        token = data.get("token")

        if not isinstance(token, str) or not token:
            raise PaymentProviderResponseError(
                "PesaPal authentication response did not contain "
                "a valid access token.",
            )

        self._access_token = token

        return token

    def get_access_token(self) -> str:
        """
        Return a cached access token or authenticate with PesaPal.
        """

        if self._access_token:
            return self._access_token

        return self.authenticate()

    def submit_order(
        self,
        *,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Submit a payment order to PesaPal.

        Raises:
            PaymentProviderRequestError:
                If PesaPal rejects the request as invalid.

            PaymentProviderCommunicationError:
                If communication fails.

            PaymentProviderAuthenticationError:
                If authentication fails.

            PaymentProviderOperationError:
                If PesaPal rejects the operation.

            PaymentProviderResponseError:
                If the response is invalid.
        """

        token = self.get_access_token()

        try:
            response = requests.post(
                self.order_submission_url,
                json=payload,
                headers=self._authorization_headers(token),
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise PaymentProviderCommunicationError(
                "Failed to communicate with PesaPal order API.",
            ) from exc

        if response.status_code in {401, 403}:
            self._access_token = None

            raise PaymentProviderAuthenticationError(
                "PesaPal rejected the authentication token.",
            )

        if response.status_code in {400, 422}:
            raise PaymentProviderRequestError(
                "PesaPal rejected the payment order request.",
            )

        if not response.ok:
            raise PaymentProviderOperationError(
                "PesaPal failed to submit the payment order. "
                f"HTTP status: {response.status_code}.",
            )

        return self._parse_json_response(
            response,
            operation="payment order submission",
        )

    def get_transaction_status(
        self,
        *,
        provider_transaction_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve transaction status from PesaPal.
        """

        token = self.get_access_token()

        params = {
            "orderTrackingId": provider_transaction_id,
        }

        try:
            response = requests.get(
                self.order_status_url,
                params=params,
                headers=self._authorization_headers(token),
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise PaymentProviderCommunicationError(
                "Failed to communicate with PesaPal transaction " "status API.",
            ) from exc

        if response.status_code in {401, 403}:
            self._access_token = None

            raise PaymentProviderAuthenticationError(
                "PesaPal rejected the authentication token.",
            )

        if response.status_code == 404:
            raise PaymentProviderRequestError(
                "PesaPal could not find the requested transaction.",
            )

        if not response.ok:
            raise PaymentProviderOperationError(
                "PesaPal failed to retrieve transaction status. "
                f"HTTP status: {response.status_code}.",
            )

        return self._parse_json_response(
            response,
            operation="transaction status lookup",
        )

    @staticmethod
    def _authorization_headers(
        token: str,
    ) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @staticmethod
    def _parse_json_response(
        response: requests.Response,
        *,
        operation: str,
    ) -> dict[str, Any]:
        try:
            data = response.json()
        except ValueError as exc:
            raise PaymentProviderResponseError(
                f"PesaPal returned invalid JSON during " f"{operation}.",
            ) from exc

        if not isinstance(data, dict):
            raise PaymentProviderResponseError(
                f"PesaPal returned an invalid response format " f"during {operation}.",
            )

        return data
