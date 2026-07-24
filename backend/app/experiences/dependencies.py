from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.experiences.repository import ExperienceRepository
from app.experiences.service import ExperienceService
from app.resume_versions.dependencies import get_resume_version_service
from app.resume_versions.service import ResumeVersionService
from app.resumes.repository import ResumeRepository


def get_experience_service(
    db: Session = Depends(get_db),
    resume_version_service: ResumeVersionService = Depends(
        get_resume_version_service,
    ),
) -> ExperienceService:
    experience_repository = ExperienceRepository(db)
    resume_repository = ResumeRepository(db)

    return ExperienceService(
        repository=experience_repository,
        resume_repository=resume_repository,
        resume_version_service=resume_version_service,
    )
