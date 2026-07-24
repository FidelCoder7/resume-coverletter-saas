from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.resume_versions.repository import ResumeVersionRepository
from app.resume_versions.service import ResumeVersionService
from app.resumes.models import Resume
from app.resumes.repository import ResumeRepository
from app.users.models import User


def get_resume_version_repository(
    session: Session = Depends(get_db),
) -> ResumeVersionRepository:
    return ResumeVersionRepository(session)


def get_resume_version_service(
    repository: ResumeVersionRepository = Depends(
        get_resume_version_repository,
    ),
) -> ResumeVersionService:
    return ResumeVersionService(
        repository=repository,
    )


def get_owned_resume(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Resume:
    """
    Resolve a resume only when it belongs to the authenticated user.

    This dependency provides the ownership boundary for all
    resume-version endpoints.
    """

    repository = ResumeRepository(db)

    resume = repository.get_by_id(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    return resume
