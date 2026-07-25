from fastapi import Depends
from sqlalchemy.orm import Session

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


def get_subscription_service(
    repository: PlanLimitRepository = Depends(
        get_plan_limit_repository,
    ),
) -> SubscriptionService:
    """
    Return the subscription service.
    """

    return SubscriptionService(
        repository=repository,
    )