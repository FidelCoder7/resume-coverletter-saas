from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.projects.dependencies import get_project_service
from app.projects.schemas import (
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)
from app.projects.service import ProjectService
from app.users.models import User

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "/resume/{resume_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    resume_id: UUID,
    payload: ProjectCreate,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    return service.create_project(
        user_id=current_user.id,
        resume_id=resume_id,
        name=payload.name,
        description=payload.description,
        technologies=payload.technologies,
        project_url=str(payload.project_url) if payload.project_url else None,
        repository_url=str(payload.repository_url) if payload.repository_url else None,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_ongoing=payload.is_ongoing,
        display_order=payload.display_order,
    )


@router.get(
    "/resume/{resume_id}",
    response_model=ProjectListResponse,
)
def list_projects(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    return ProjectListResponse(
        projects=service.list_projects(
            user_id=current_user.id,
            resume_id=resume_id,
        ),
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    return service.get_project(
        user_id=current_user.id,
        project_id=project_id,
    )


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    return service.update_project(
        user_id=current_user.id,
        project_id=project_id,
        name=payload.name,
        description=payload.description,
        technologies=payload.technologies,
        project_url=str(payload.project_url) if payload.project_url else None,
        repository_url=str(payload.repository_url) if payload.repository_url else None,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_ongoing=payload.is_ongoing,
        display_order=payload.display_order,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
):
    service.delete_project(
        user_id=current_user.id,
        project_id=project_id,
    )
