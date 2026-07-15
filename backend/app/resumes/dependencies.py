from fastapi import Depends
from sqlalchemy.orm import Session

from app.ai.dependencies import get_ai_service
from app.ai.service import AIService
from app.ai_usage.repository import AIUsageRepository
from app.database.session import get_db
from app.resumes.ai_service import ResumeAIService
from app.resumes.repository import ResumeRepository
from app.resumes.service import ResumeService


def get_resume_service(
    db: Session = Depends(get_db),
) -> ResumeService:
    """
    Dependency for standard resume CRUD operations.
    """
    repository = ResumeRepository(db)

    return ResumeService(repository)


def get_resume_ai_service(
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service),
) -> ResumeAIService:
    """
    Dependency for AI-powered resume generation.
    """
    repository = ResumeRepository(db)
    ai_usage_repository = AIUsageRepository(db)

    return ResumeAIService(
        repository=repository,
        ai_service=ai_service,
        ai_usage_repository=ai_usage_repository,
    )
