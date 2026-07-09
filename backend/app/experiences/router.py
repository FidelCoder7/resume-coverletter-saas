from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.experiences.dependencies import get_experience_service
from app.experiences.schemas import (
    CreateExperienceRequest,
    ExperienceListResponse,
    ExperienceResponse,
    UpdateExperienceRequest,
)
from app.experiences.service import ExperienceService
from app.users.models import User

router = APIRouter(
    prefix="/experiences",
    tags=["Experiences"],
)


@router.post(
    "/resume/{resume_id}",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_experience(
    resume_id: UUID,
    payload: CreateExperienceRequest,
    current_user: User = Depends(get_current_user),
    service: ExperienceService = Depends(get_experience_service),
):
    return service.create_experience(
        user_id=current_user.id,
        resume_id=resume_id,
        company=payload.company,
        job_title=payload.job_title,
        location=payload.location,
        employment_type=payload.employment_type,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_current=payload.is_current,
        description=payload.description,
        display_order=payload.display_order,
    )


@router.get(
    "/resume/{resume_id}",
    response_model=ExperienceListResponse,
)
def list_experiences(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ExperienceService = Depends(get_experience_service),
):
    return ExperienceListResponse(
        experiences=service.list_experiences(
            user_id=current_user.id,
            resume_id=resume_id,
        ),
    )


@router.get(
    "/{experience_id}",
    response_model=ExperienceResponse,
)
def get_experience(
    experience_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ExperienceService = Depends(get_experience_service),
):
    return service.get_experience(
        user_id=current_user.id,
        experience_id=experience_id,
    )


@router.put(
    "/{experience_id}",
    response_model=ExperienceResponse,
)
def update_experience(
    experience_id: UUID,
    payload: UpdateExperienceRequest,
    current_user: User = Depends(get_current_user),
    service: ExperienceService = Depends(get_experience_service),
):
    return service.update_experience(
        user_id=current_user.id,
        experience_id=experience_id,
        company=payload.company,
        job_title=payload.job_title,
        location=payload.location,
        employment_type=payload.employment_type,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_current=payload.is_current,
        description=payload.description,
        display_order=payload.display_order,
    )


@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_experience(
    experience_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ExperienceService = Depends(get_experience_service),
):
    service.delete_experience(
        user_id=current_user.id,
        experience_id=experience_id,
    )
