from app.billing.providers.pesapal.client import PesaPalClient
from app.core.config import settings


def register_ipn() -> str:
    """
    Register the configured PesaPal IPN URL and return its PesaPal ID.

    This is intended for one-off merchant/environment configuration,
    not application startup or individual payment processing.
    """

    client = PesaPalClient()

    response = client.register_ipn(
        url=settings.PESAPAL_IPN_URL,
        notification_type=settings.PESAPAL_IPN_NOTIFICATION_TYPE,
    )

    ipn_id = response["ipn_id"]

    print("PesaPal IPN registration successful.")
    print(f"IPN URL: {settings.PESAPAL_IPN_URL}")
    print(f"Notification type: {settings.PESAPAL_IPN_NOTIFICATION_TYPE}")
    print(f"IPN ID: {ipn_id}")

    return ipn_id


if __name__ == "__main__":
    register_ipn()