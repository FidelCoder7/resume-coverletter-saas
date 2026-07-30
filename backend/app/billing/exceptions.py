class BillingException(Exception):
    """
    Base exception for billing-related errors.
    """


class PaymentTransactionNotFound(BillingException):
    """
    Raised when a requested payment transaction does not exist.
    """


class InvalidPaymentTransactionState(BillingException):
    """
    Raised when an invalid payment transaction state transition
    is attempted.
    """


class PaymentTransactionAlreadyCompleted(BillingException):
    """
    Raised when an operation attempts to modify a transaction
    that has already been completed.
    """


class InvalidSubscriptionPaymentPlan(BillingException):
    """
    Raised when a payment is attempted for a subscription plan
    that cannot be purchased through the payment flow.
    """


class InvalidPaymentCallback(BillingException):
    """
    Raised when a payment provider callback is missing required
    information or contains an invalid payload.
    """


class UnsupportedPaymentCallback(BillingException):
    """
    Raised when a payment provider callback notification type is not
    supported by the application.
    """
