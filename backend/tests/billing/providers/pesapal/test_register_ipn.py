from unittest.mock import Mock, patch

from app.billing.providers.pesapal.register_ipn import register_ipn


@patch(
    "app.billing.providers.pesapal.register_ipn.PesaPalClient",
)
def test_register_ipn_returns_registered_ipn_id(
    mock_client_class: Mock,
    capsys,
):
    """
    The registration utility should return the IPN ID supplied by
    PesaPal and display the registration details.
    """

    client = mock_client_class.return_value

    client.register_ipn.return_value = {
        "url": "https://example.com/api/billing/pesapal/ipn",
        "ipn_id": "84740ab4-3cd9-47da-8a4f-dd1db53494b5",
        "ipn_notification_type_description": "GET",
        "ipn_status": 1,
        "status": "200",
    }

    with patch(
        "app.billing.providers.pesapal.register_ipn.settings.PESAPAL_IPN_URL",
        "https://example.com/api/billing/pesapal/ipn",
    ), patch(
        "app.billing.providers.pesapal.register_ipn.settings.PESAPAL_IPN_NOTIFICATION_TYPE",
        "GET",
    ):
        result = register_ipn()

    assert result == "84740ab4-3cd9-47da-8a4f-dd1db53494b5"

    client.register_ipn.assert_called_once_with(
        url="https://example.com/api/billing/pesapal/ipn",
        notification_type="GET",
    )

    output = capsys.readouterr().out

    assert "PesaPal IPN registration successful." in output
    assert "IPN URL: https://example.com/api/billing/pesapal/ipn" in output
    assert "Notification type: GET" in output
    assert "IPN ID: 84740ab4-3cd9-47da-8a4f-dd1db53494b5" in output