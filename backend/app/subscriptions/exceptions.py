class SubscriptionError(Exception):
    """
    Base exception for subscription domain errors.
    """


class PlanLimitNotFound(SubscriptionError):
    """
    Raised when no limit configuration exists for a plan and feature.
    """


class SubscriptionLimitExceeded(SubscriptionError):
    """
    Raised when a user has reached or exceeded their subscription limit.
    """

    def __init__(
        self,
        *,
        subscription_plan: str,
        feature: str,
        limit: int,
        usage: int,
        period: str,
    ) -> None:
        self.subscription_plan = subscription_plan
        self.feature = feature
        self.limit = limit
        self.usage = usage
        self.period = period

        super().__init__(
            f"Subscription limit exceeded for "
            f"plan={subscription_plan}, "
            f"feature={feature}, "
            f"period={period}. "
            f"Limit={limit}, usage={usage}.",
        )
