from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.subscriptions.dependencies import get_subscription_service
from app.subscriptions.schemas import PlanLimitListResponse
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
):
    """
    Return the AI usage limits applicable to the authenticated user.
    """

    limits = service.list_plan_limits(
        subscription_plan=current_user.subscription_plan,
    )

    return PlanLimitListResponse(
        subscription_plan=current_user.subscription_plan,
        limits=limits,
    )