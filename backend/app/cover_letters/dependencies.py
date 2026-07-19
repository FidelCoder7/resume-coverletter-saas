from fastapi import Depends
from sqlalchemy.orm import Session

from app.ai.dependencies import get_ai_service
from app.ai.service import AIService
from app.ai_usage.repository import AIUsageRepository
from app.ai_usage.service import AIUsageService
from app.cover_letters.ai_service import CoverLetterAIService
from app.cover_letters.repository import CoverLetterRepository
from app.cover_letters.service import CoverLetterService
from app.database.session import get_db
from app.resumes.repository import ResumeRepository


def get_cover_letter_service(
    db: Session = Depends(get_db),
) -> CoverLetterService:
    cover_letter_repository = CoverLetterRepository(db)
    resume_repository = ResumeRepository(db)

    return CoverLetterService(
        repository=cover_letter_repository,
        resume_repository=resume_repository,
    )


def get_cover_letter_ai_service(
    db: Session = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service),
) -> CoverLetterAIService:
    cover_letter_repository = CoverLetterRepository(db)
    resume_repository = ResumeRepository(db)

    ai_usage_service = AIUsageService(
        AIUsageRepository(db),
    )

    return CoverLetterAIService(
        repository=cover_letter_repository,
        resume_repository=resume_repository,
        ai_service=ai_service,
        ai_usage_service=ai_usage_service,
    )
