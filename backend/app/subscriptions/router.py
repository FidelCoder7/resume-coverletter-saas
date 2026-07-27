from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.subscriptions.dependencies import get_subscription_service
from app.subscriptions.schemas import (
    PlanLimitListResponse,
    UsageSummaryResponse,
)
from app.subscriptions.service import SubscriptionService
from app.users.models import User

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"],
)


@router.get(
    "/limits",
    response_model=PlanLimitListResponse,
)
def get_my_subscription_limits(
    current_user: User = Depends(get_current_user),
    service: SubscriptionService = Depends(
        get_subscription_service,
    ),
) -> PlanLimitListResponse:
    """
    Return the AI usage limits applicable to the authenticated user.
    """

    return service.list_plan_limits(
        subscription_plan=current_user.subscription_plan,
    )


@router.get(
    "/usage",
    response_model=UsageSummaryResponse,
)
def get_my_subscription_usage(
    current_user: User = Depends(get_current_user),
    service: SubscriptionService = Depends(
        get_subscription_service,
    ),
) -> UsageSummaryResponse:
    """
    Return the authenticated user's current monthly AI usage.
    """

    period_start, period_end = service._get_current_month_period()

    return UsageSummaryResponse(
        subscription_plan=current_user.subscription_plan,
        period_start=period_start,
        period_end=period_end,
        features=service.get_all_usage_status(
            user=current_user,
        ),
    )
