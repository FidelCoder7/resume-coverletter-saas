from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.projects.repository import ProjectRepository
from app.projects.service import ProjectService
from app.resumes.repository import ResumeRepository


def get_project_service(
    db: Session = Depends(get_db),
) -> ProjectService:
    project_repository = ProjectRepository(db)
    resume_repository = ResumeRepository(db)

    return ProjectService(
        repository=project_repository,
        resume_repository=resume_repository,
    )
