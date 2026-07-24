from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.educations.repository import EducationRepository
from app.educations.service import EducationService
from app.resume_versions.dependencies import get_resume_version_service
from app.resume_versions.service import ResumeVersionService
from app.resumes.repository import ResumeRepository


def get_education_service(
    db: Session = Depends(get_db),
    resume_version_service: ResumeVersionService = Depends(
        get_resume_version_service,
    ),
) -> EducationService:
    return EducationService(
        repository=EducationRepository(db),
        resume_repository=ResumeRepository(db),
        resume_version_service=resume_version_service,
    )
