from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.experiences.repository import ExperienceRepository
from app.experiences.service import ExperienceService
from app.resumes.repository import ResumeRepository


def get_experience_service(
    db: Session = Depends(get_db),
) -> ExperienceService:
    experience_repository = ExperienceRepository(db)
    resume_repository = ResumeRepository(db)

    return ExperienceService(
        repository=experience_repository,
        resume_repository=resume_repository,
    )
