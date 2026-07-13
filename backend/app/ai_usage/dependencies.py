from fastapi import Depends
from sqlalchemy.orm import Session

from app.ai_usage.repository import AIUsageRepository
from app.ai_usage.service import AIUsageService
from app.database.session import get_db


def get_ai_usage_repository(
    db: Session = Depends(get_db),
) -> AIUsageRepository:
    """
    Return the AI usage repository.
    """

    return AIUsageRepository(
        db=db,
    )


def get_ai_usage_service(
    repository: AIUsageRepository = Depends(
        get_ai_usage_repository,
    ),
) -> AIUsageService:
    """
    Return the AI usage service.
    """

    return AIUsageService(
        repository=repository,
    )
