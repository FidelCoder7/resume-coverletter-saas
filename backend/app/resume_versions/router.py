from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.resume_versions.dependencies import (
    get_owned_resume,
    get_resume_version_service,
)
from app.resume_versions.schemas import (
    ResumeVersionResponse,
)
from app.resume_versions.service import ResumeVersionService
from app.resumes.dependencies import get_resume_service
from app.resumes.models import Resume
from app.resumes.schemas import ResumeResponse
from app.resumes.service import ResumeService

router = APIRouter(
    prefix="/resumes/{resume_id}/versions",
    tags=["Resume Versions"],
)


@router.get(
    "",
    response_model=list[ResumeVersionResponse],
)
def list_resume_versions(
    resume: Resume = Depends(get_owned_resume),
    service: ResumeVersionService = Depends(
        get_resume_version_service,
    ),
):
    """
    Return the complete version history for a user's resume.

    Versions are returned from newest to oldest.
    """

    return service.get_version_history(
        resume_id=resume.id,
    )


@router.get(
    "/latest",
    response_model=ResumeVersionResponse,
)
def get_latest_resume_version(
    resume: Resume = Depends(get_owned_resume),
    service: ResumeVersionService = Depends(
        get_resume_version_service,
    ),
):
    """
    Return the latest version of a user's resume.
    """

    version = service.get_latest_version(
        resume_id=resume.id,
    )

    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No versions found for this resume.",
        )

    return version


@router.post(
    "/{version_id}/restore",
    response_model=ResumeResponse,
)
def restore_version(
    version_id: UUID,
    resume: Resume = Depends(get_owned_resume),
    service: ResumeService = Depends(
        get_resume_service,
    ),
):
    """
    Restore the requested resume to a historical version.

    The historical version remains immutable. A new RESTORE
    version is created for the restored state.
    """

    return service.restore_version(
        user_id=resume.user_id,
        resume_id=resume.id,
        version_id=version_id,
    )


@router.get(
    "/{version_id}",
    response_model=ResumeVersionResponse,
)
def get_resume_version(
    version_id: UUID,
    resume: Resume = Depends(get_owned_resume),
    service: ResumeVersionService = Depends(
        get_resume_version_service,
    ),
):
    """
    Return an individual version belonging to the requested resume.

    The parent resume must belong to the authenticated user.
    """

    version = service.get_version(
        version_id=version_id,
    )

    if version is None or version.resume_id != resume.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume version not found.",
        )

    return version
