from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.educations.repository import EducationRepository
from app.educations.service import EducationService
from app.resumes.repository import ResumeRepository


def get_education_service(
    db: Session = Depends(get_db),
) -> EducationService:
    return EducationService(
        repository=EducationRepository(db),
        resume_repository=ResumeRepository(db),
    )
