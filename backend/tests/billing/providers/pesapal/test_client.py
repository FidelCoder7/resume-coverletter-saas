from unittest.mock import Mock, patch

import pytest
import requests

from app.billing.providers.exceptions import (
    PaymentProviderAuthenticationError,
    PaymentProviderCommunicationError,
    PaymentProviderConfigurationError,
    PaymentProviderOperationError,
    PaymentProviderRequestError,
    PaymentProviderResponseError,
)
from app.billing.providers.pesapal.client import PesaPalClient


@pytest.fixture()
def client():
    return PesaPalClient(
        consumer_key="test-consumer-key",
        consumer_secret="test-consumer-secret",
        timeout=10,
        oauth_url="https://example.com/oauth",
        order_submission_url="https://example.com/orders",
        order_status_url="https://example.com/status",
    )


def make_response(
    *,
    status_code: int = 200,
    json_data=None,
    ok: bool | None = None,
):
    response = Mock()

    response.status_code = status_code

    if ok is None:
        response.ok = 200 <= status_code < 400
    else:
        response.ok = ok

    if isinstance(json_data, Exception):
        response.json.side_effect = json_data
    else:
        response.json.return_value = json_data

    return response


# ------------------------------------------------------------------
# Authentication
# ------------------------------------------------------------------


def test_authenticate_returns_and_caches_access_token(
    client,
):
    response = make_response(
        json_data={
            "token": "access-token-123",
        },
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ) as mock_post:
        token = client.authenticate()

        assert token == "access-token-123"
        assert client._access_token == "access-token-123"

        mock_post.assert_called_once_with(
            "https://example.com/oauth",
            json={
                "consumer_key": "test-consumer-key",
                "consumer_secret": "test-consumer-secret",
            },
            timeout=10,
        )


def test_get_access_token_uses_cached_token(
    client,
):
    client._access_token = "cached-token"

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
    ) as mock_post:
        token = client.get_access_token()

    assert token == "cached-token"
    mock_post.assert_not_called()


def test_get_access_token_authenticates_when_token_is_not_cached(
    client,
):
    response = make_response(
        json_data={
            "token": "new-access-token",
        },
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ) as mock_post:
        token = client.get_access_token()

    assert token == "new-access-token"
    mock_post.assert_called_once()


def test_authenticate_raises_configuration_error_when_credentials_are_missing():
    client = PesaPalClient(
        consumer_key="",
        consumer_secret="",
        oauth_url="https://example.com/oauth",
    )
    with pytest.raises(
        PaymentProviderConfigurationError,
        match="consumer credentials are not configured",
    ):
        client.authenticate()


@pytest.mark.parametrize(
    "status_code",
    [401, 403],
)
def test_authenticate_raises_authentication_error_for_auth_failure(
    client,
    status_code,
):
    response = make_response(
        status_code=status_code,
        json_data={
            "error": "invalid credentials",
        },
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderAuthenticationError,
        ):
            client.authenticate()


def test_authenticate_raises_authentication_error_for_other_failed_response(
    client,
):
    response = make_response(
        status_code=500,
        json_data={
            "error": "server error",
        },
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderAuthenticationError,
            match="status 500",
        ):
            client.authenticate()


def test_authenticate_raises_communication_error_on_request_failure(
    client,
):
    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        side_effect=requests.RequestException(
            "connection failed",
        ),
    ):
        with pytest.raises(
            PaymentProviderCommunicationError,
        ):
            client.authenticate()


def test_authenticate_raises_response_error_for_invalid_json(
    client,
):
    response = make_response(
        json_data=ValueError("invalid json"),
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderResponseError,
            match="invalid JSON",
        ):
            client.authenticate()


@pytest.mark.parametrize(
    "response_data",
    [
        {},
        {"token": ""},
        {"token": None},
        {"token": 123},
    ],
)
def test_authenticate_raises_response_error_when_token_is_invalid(
    client,
    response_data,
):
    response = make_response(
        json_data=response_data,
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderResponseError,
            match="valid access token",
        ):
            client.authenticate()


# ------------------------------------------------------------------
# Submit Order
# ------------------------------------------------------------------


def test_submit_order_returns_provider_response(
    client,
):
    client._access_token = "access-token"

    response_data = {
        "order_tracking_id": "TRACK-001",
        "redirect_url": "https://example.com/pay",
    }

    response = make_response(
        json_data=response_data,
    )

    payload = {
        "id": "ORDER-001",
        "amount": 1000,
        "currency": "KES",
    }

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ) as mock_post:
        result = client.submit_order(
            payload=payload,
        )

    assert result == response_data

    mock_post.assert_called_once_with(
        "https://example.com/orders",
        json=payload,
        headers={
            "Authorization": "Bearer access-token",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        timeout=10,
    )


def test_submit_order_authenticates_when_token_is_missing(
    client,
):
    auth_response = make_response(
        json_data={
            "token": "fresh-token",
        },
    )

    order_response = make_response(
        json_data={
            "order_tracking_id": "TRACK-001",
        },
    )

    payload = {
        "id": "ORDER-001",
        "amount": 1000,
    }

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        side_effect=[
            auth_response,
            order_response,
        ],
    ) as mock_post:
        result = client.submit_order(
            payload=payload,
        )

    assert result == {
        "order_tracking_id": "TRACK-001",
    }

    assert mock_post.call_count == 2


@pytest.mark.parametrize(
    "status_code",
    [401, 403],
)
def test_submit_order_raises_authentication_error_and_clears_token(
    client,
    status_code,
):
    client._access_token = "expired-token"

    response = make_response(
        status_code=status_code,
        json_data={
            "error": "unauthorized",
        },
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderAuthenticationError,
        ):
            client.submit_order(
                payload={
                    "id": "ORDER-001",
                },
            )

    assert client._access_token is None


@pytest.mark.parametrize(
    "status_code",
    [400, 422],
)
def test_submit_order_raises_request_error_for_invalid_request(
    client,
    status_code,
):
    client._access_token = "access-token"

    response = make_response(
        status_code=status_code,
        json_data={
            "error": "invalid request",
        },
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderRequestError,
        ):
            client.submit_order(
                payload={
                    "id": "ORDER-001",
                },
            )


def test_submit_order_raises_operation_error_for_provider_failure(
    client,
):
    client._access_token = "access-token"

    response = make_response(
        status_code=500,
        json_data={
            "error": "internal server error",
        },
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderOperationError,
            match="HTTP status: 500",
        ):
            client.submit_order(
                payload={
                    "id": "ORDER-001",
                },
            )


def test_submit_order_raises_communication_error_on_request_failure(
    client,
):
    client._access_token = "access-token"

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        side_effect=requests.RequestException(
            "connection failed",
        ),
    ):
        with pytest.raises(
            PaymentProviderCommunicationError,
        ):
            client.submit_order(
                payload={
                    "id": "ORDER-001",
                },
            )


def test_submit_order_raises_response_error_for_invalid_json(
    client,
):
    client._access_token = "access-token"

    response = make_response(
        json_data=ValueError("invalid json"),
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderResponseError,
            match="payment order submission",
        ):
            client.submit_order(
                payload={
                    "id": "ORDER-001",
                },
            )


def test_submit_order_raises_response_error_for_non_dict_response(
    client,
):
    client._access_token = "access-token"

    response = make_response(
        json_data=[
            "unexpected",
            "response",
        ],
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.post",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderResponseError,
            match="invalid response format",
        ):
            client.submit_order(
                payload={
                    "id": "ORDER-001",
                },
            )


# ------------------------------------------------------------------
# Transaction Status
# ------------------------------------------------------------------


def test_get_transaction_status_returns_provider_response(
    client,
):
    client._access_token = "access-token"

    response_data = {
        "payment_status_description": "Completed",
        "payment_method": "Mpesa",
    }

    response = make_response(
        json_data=response_data,
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.get",
        return_value=response,
    ) as mock_get:
        result = client.get_transaction_status(
            provider_transaction_id="TRACK-001",
        )

    assert result == response_data

    mock_get.assert_called_once_with(
        "https://example.com/status",
        params={
            "orderTrackingId": "TRACK-001",
        },
        headers={
            "Authorization": "Bearer access-token",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        timeout=10,
    )


@pytest.mark.parametrize(
    "status_code",
    [401, 403],
)
def test_get_transaction_status_raises_authentication_error_and_clears_token(
    client,
    status_code,
):
    client._access_token = "expired-token"

    response = make_response(
        status_code=status_code,
        json_data={
            "error": "unauthorized",
        },
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.get",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderAuthenticationError,
        ):
            client.get_transaction_status(
                provider_transaction_id="TRACK-001",
            )

    assert client._access_token is None


def test_get_transaction_status_raises_request_error_for_missing_transaction(
    client,
):
    client._access_token = "access-token"

    response = make_response(
        status_code=404,
        json_data={
            "error": "not found",
        },
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.get",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderRequestError,
        ):
            client.get_transaction_status(
                provider_transaction_id="TRACK-001",
            )


def test_get_transaction_status_raises_operation_error_for_provider_failure(
    client,
):
    client._access_token = "access-token"

    response = make_response(
        status_code=500,
        json_data={
            "error": "server error",
        },
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.get",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderOperationError,
            match="HTTP status: 500",
        ):
            client.get_transaction_status(
                provider_transaction_id="TRACK-001",
            )


def test_get_transaction_status_raises_communication_error_on_request_failure(
    client,
):
    client._access_token = "access-token"

    with patch(
        "app.billing.providers.pesapal.client.requests.get",
        side_effect=requests.RequestException(
            "connection failed",
        ),
    ):
        with pytest.raises(
            PaymentProviderCommunicationError,
        ):
            client.get_transaction_status(
                provider_transaction_id="TRACK-001",
            )


def test_get_transaction_status_raises_response_error_for_invalid_json(
    client,
):
    client._access_token = "access-token"

    response = make_response(
        json_data=ValueError("invalid json"),
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.get",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderResponseError,
            match="transaction status lookup",
        ):
            client.get_transaction_status(
                provider_transaction_id="TRACK-001",
            )


def test_get_transaction_status_raises_response_error_for_non_dict_response(
    client,
):
    client._access_token = "access-token"

    response = make_response(
        json_data=[
            "unexpected",
            "response",
        ],
    )

    with patch(
        "app.billing.providers.pesapal.client.requests.get",
        return_value=response,
    ):
        with pytest.raises(
            PaymentProviderResponseError,
            match="invalid response format",
        ):
            client.get_transaction_status(
                provider_transaction_id="TRACK-001",
            )


# ------------------------------------------------------------------
# Helper Methods
# ------------------------------------------------------------------


def test_authorization_headers_build_expected_headers():
    headers = PesaPalClient._authorization_headers(
        "access-token",
    )

    assert headers == {
        "Authorization": "Bearer access-token",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


@pytest.mark.parametrize(
    "json_data",
    [
        ValueError("invalid json"),
        None,
        [],
        "invalid",
    ],
)
def test_parse_json_response_raises_response_error_for_invalid_response(
    json_data,
):
    response = make_response(
        json_data=json_data,
    )

    if isinstance(json_data, ValueError):
        response.json.side_effect = json_data

    with pytest.raises(
        PaymentProviderResponseError,
    ):
        PesaPalClient._parse_json_response(
            response,
            operation="test operation",
        )
