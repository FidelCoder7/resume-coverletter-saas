from dataclasses import dataclass
from decimal import Decimal

from app.common.constants import SubscriptionPlan


@dataclass(frozen=True)
class SubscriptionPrice:
    """
    Server-side authoritative price for a subscription plan.
    """

    plan: SubscriptionPlan
    amount: Decimal
    currency: str


SUBSCRIPTION_PRICES: dict[
    SubscriptionPlan,
    SubscriptionPrice,
] = {
    SubscriptionPlan.FREE: SubscriptionPrice(
        plan=SubscriptionPlan.FREE,
        amount=Decimal("0.00"),
        currency="KES",
    ),
    SubscriptionPlan.PRO: SubscriptionPrice(
        plan=SubscriptionPlan.PRO,
        amount=Decimal("1000.00"),
        currency="KES",
    ),
}


def get_subscription_price(
    subscription_plan: SubscriptionPlan,
) -> SubscriptionPrice:
    """
    Return the authoritative server-side price for a subscription plan.
    """

    try:
        return SUBSCRIPTION_PRICES[subscription_plan]
    except KeyError as exc:
        raise ValueError(
            f"No price configured for subscription plan " f"{subscription_plan.value}.",
        ) from exc
