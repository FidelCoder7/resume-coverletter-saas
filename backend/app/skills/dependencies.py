from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.resume_versions.dependencies import get_resume_version_service
from app.resume_versions.service import ResumeVersionService
from app.resumes.repository import ResumeRepository
from app.skills.repository import SkillRepository
from app.skills.service import SkillService


def get_skill_service(
    db: Session = Depends(get_db),
    resume_version_service: ResumeVersionService = Depends(
        get_resume_version_service,
    ),
) -> SkillService:
    skill_repository = SkillRepository(db)
    resume_repository = ResumeRepository(db)

    return SkillService(
        repository=skill_repository,
        resume_repository=resume_repository,
        resume_version_service=resume_version_service,
    )
