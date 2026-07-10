from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.skills.dependencies import get_skill_service
from app.skills.schemas import (
    CreateSkillRequest,
    SkillListResponse,
    SkillResponse,
    UpdateSkillRequest,
)
from app.skills.service import SkillService
from app.users.models import User

router = APIRouter(
    prefix="/skills",
    tags=["Skills"],
)


@router.post(
    "/resume/{resume_id}",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_skill(
    resume_id: UUID,
    payload: CreateSkillRequest,
    current_user: User = Depends(get_current_user),
    service: SkillService = Depends(get_skill_service),
):
    return service.create_skill(
        user_id=current_user.id,
        resume_id=resume_id,
        name=payload.name,
        proficiency=payload.proficiency,
        display_order=payload.display_order,
    )


@router.get(
    "/resume/{resume_id}",
    response_model=SkillListResponse,
)
def list_skills(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    service: SkillService = Depends(get_skill_service),
):
    return SkillListResponse(
        skills=service.list_skills(
            user_id=current_user.id,
            resume_id=resume_id,
        ),
    )


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
)
def get_skill(
    skill_id: UUID,
    current_user: User = Depends(get_current_user),
    service: SkillService = Depends(get_skill_service),
):
    return service.get_skill(
        user_id=current_user.id,
        skill_id=skill_id,
    )


@router.put(
    "/{skill_id}",
    response_model=SkillResponse,
)
def update_skill(
    skill_id: UUID,
    payload: UpdateSkillRequest,
    current_user: User = Depends(get_current_user),
    service: SkillService = Depends(get_skill_service),
):
    return service.update_skill(
        user_id=current_user.id,
        skill_id=skill_id,
        name=payload.name,
        proficiency=payload.proficiency,
        display_order=payload.display_order,
    )


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_skill(
    skill_id: UUID,
    current_user: User = Depends(get_current_user),
    service: SkillService = Depends(get_skill_service),
):
    service.delete_skill(
        user_id=current_user.id,
        skill_id=skill_id,
    )
