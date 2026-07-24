from fastapi import Depends
from sqlalchemy.orm import Session

from app.certifications.repository import CertificationRepository
from app.certifications.service import CertificationService
from app.database.session import get_db
from app.resume_versions.dependencies import get_resume_version_service
from app.resume_versions.service import ResumeVersionService
from app.resumes.repository import ResumeRepository


def get_certification_service(
    db: Session = Depends(get_db),
    resume_version_service: ResumeVersionService = Depends(
        get_resume_version_service,
    ),
) -> CertificationService:
    certification_repository = CertificationRepository(db)
    resume_repository = ResumeRepository(db)

    return CertificationService(
        repository=certification_repository,
        resume_repository=resume_repository,
        resume_version_service=resume_version_service,
    )
