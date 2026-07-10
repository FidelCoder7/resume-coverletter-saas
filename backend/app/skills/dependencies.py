from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.resumes.repository import ResumeRepository
from app.skills.repository import SkillRepository
from app.skills.service import SkillService


def get_skill_service(
    db: Session = Depends(get_db),
) -> SkillService:
    skill_repository = SkillRepository(db)
    resume_repository = ResumeRepository(db)

    return SkillService(
        repository=skill_repository,
        resume_repository=resume_repository,
    )
