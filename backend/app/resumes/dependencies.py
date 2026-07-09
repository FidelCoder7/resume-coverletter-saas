from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.resumes.repository import ResumeRepository
from app.resumes.service import ResumeService


def get_resume_service(
    db: Session = Depends(get_db),
) -> ResumeService:
    repository = ResumeRepository(db)

    return ResumeService(repository)
