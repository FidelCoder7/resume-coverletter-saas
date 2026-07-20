from fastapi import Depends
from sqlalchemy.orm import Session

from app.ai.dependencies import get_ai_service
from app.ai.service import AIService
from app.ai_usage.repository import AIUsageRepository
from app.ai_usage.service import AIUsageService
from app.ats.ai_service import ATSAIService
from app.ats.service import ATSService
from app.database.session import get_db
from app.resumes.repository import ResumeRepository


def get_ats_ai_service(
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service),
) -> ATSAIService:
    """
    Dependency for AI-powered ATS optimization.
    """

    ai_usage_service = AIUsageService(
        AIUsageRepository(db),
    )

    return ATSAIService(
        ai_service=ai_service,
        ai_usage_service=ai_usage_service,
    )


def get_ats_service(
    db: Session = Depends(get_db),
    ai_service: ATSAIService = Depends(get_ats_ai_service),
) -> ATSService:
    """
    Dependency for ATS optimization workflows.
    """

    repository = ResumeRepository(db)

    return ATSService(
        repository=repository,
        ai_service=ai_service,
    )
