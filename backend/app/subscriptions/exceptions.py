class SubscriptionError(Exception):
    """
    Base exception for subscription domain errors.
    """


class PlanLimitNotFound(SubscriptionError):
    """
    Raised when no limit configuration exists for a plan and feature.
    """