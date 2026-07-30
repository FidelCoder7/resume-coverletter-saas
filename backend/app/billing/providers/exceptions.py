class PaymentProviderError(Exception):
    """
    Base exception for all payment provider errors.

    Application code can catch this exception when it needs to handle
    any provider-related failure without depending on a specific
    provider implementation.
    """


class PaymentProviderConfigurationError(PaymentProviderError):
    """
    Raised when a payment provider is incorrectly configured.

    Examples include missing credentials, invalid configuration values,
    or an invalid provider environment configuration.
    """


class PaymentProviderAuthenticationError(PaymentProviderError):
    """
    Raised when authentication with a payment provider fails.

    Examples include invalid credentials, expired credentials,
    or failure to obtain an access token.
    """


class PaymentProviderRequestError(PaymentProviderError):
    """
    Raised when a request sent to a payment provider is invalid.

    This generally represents a client-side request problem, such as
    invalid payment data or missing required provider parameters.
    """


class PaymentProviderCommunicationError(PaymentProviderError):
    """
    Raised when communication with a payment provider fails.

    Examples include connection errors, timeouts, DNS failures,
    or other transport-level problems.
    """


class PaymentProviderResponseError(PaymentProviderError):
    """
    Raised when a provider returns an unexpected or invalid response.

    This is used when the provider responds but the response cannot
    be safely interpreted by the application.
    """


class PaymentProviderOperationError(PaymentProviderError):
    """
    Raised when the provider rejects or fails a requested operation.

    This represents a provider-side operational failure rather than
    a transport or authentication failure.
    """


class PaymentProviderUnsupportedOperationError(PaymentProviderError):
    """
    Raised when a payment provider does not support a requested operation.

    For example, a provider may not support cancellation of a payment
    after it has reached a particular lifecycle state.
    """
