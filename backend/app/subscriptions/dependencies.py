from fastapi import Depends
from sqlalchemy.orm import Session

from app.ai_usage.repository import AIUsageRepository
from app.database.session import get_db
from app.subscriptions.repository import PlanLimitRepository
from app.subscriptions.service import SubscriptionService


def get_plan_limit_repository(
    db: Session = Depends(get_db),
) -> PlanLimitRepository:
    """
    Return the plan limit repository.
    """

    return PlanLimitRepository(
        db=db,
    )


def get_ai_usage_repository(
    db: Session = Depends(get_db),
) -> AIUsageRepository:
    """
    Return the AI usage repository.
    """

    return AIUsageRepository(
        db=db,
    )


def get_subscription_service(
    plan_limit_repository: PlanLimitRepository = Depends(
        get_plan_limit_repository,
    ),
    ai_usage_repository: AIUsageRepository = Depends(
        get_ai_usage_repository,
    ),
) -> SubscriptionService:
    """
    Return the subscription service.
    """

    return SubscriptionService(
        repository=plan_limit_repository,
        ai_usage_repository=ai_usage_repository,
    )
