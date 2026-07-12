from fastapi import Depends
from sqlalchemy.orm import Session

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
