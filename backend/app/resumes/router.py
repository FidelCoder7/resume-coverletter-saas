from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.resumes.dependencies import get_resume_service
from app.resumes.schemas import (
    CreateResumeRequest,
    ResumeListResponse,
    ResumeResponse,
    UpdateResumeRequest,
)
from app.resumes.service import ResumeService
from app.users.models import User

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_resume(
    payload: CreateResumeRequest,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.create_resume(
        user_id=current_user.id,
        title=payload.title,
        summary=payload.summary,
    )


@router.get(
    "",
    response_model=ResumeListResponse,
)
def list_resumes(
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    return ResumeListResponse(
        resumes=service.list_resumes(current_user.id),
    )


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def get_resume(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.get_resume(
        user_id=current_user.id,
        resume_id=resume_id,
    )


@router.put(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def update_resume(
    resume_id: UUID,
    payload: UpdateResumeRequest,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.update_resume(
        user_id=current_user.id,
        resume_id=resume_id,
        title=payload.title,
        summary=payload.summary,
    )


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_resume(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    service.delete_resume(
        user_id=current_user.id,
        resume_id=resume_id,
    )
