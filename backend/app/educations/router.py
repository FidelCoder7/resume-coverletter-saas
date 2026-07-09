from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.educations.dependencies import get_education_service
from app.educations.schemas import (
    EducationCreate,
    EducationResponse,
    EducationUpdate,
)
from app.educations.service import EducationService
from app.users.models import User

router = APIRouter(
    prefix="/educations",
    tags=["Educations"],
)


@router.post(
    "/resume/{resume_id}",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_education(
    resume_id: UUID,
    payload: EducationCreate,
    current_user: User = Depends(get_current_user),
    service: EducationService = Depends(
        get_education_service,
    ),
):
    education = service.create_education(
        user_id=current_user.id,
        resume_id=resume_id,
        institution=payload.institution,
        degree=payload.degree,
        field_of_study=payload.field_of_study,
        location=payload.location,
        grade=payload.grade,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_current=payload.is_current,
        description=payload.description,
        display_order=payload.display_order,
    )

    return EducationResponse.model_validate(
        education,
    )


@router.get(
    "/resume/{resume_id}",
    response_model=list[EducationResponse],
)
def list_educations(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    service: EducationService = Depends(
        get_education_service,
    ),
):
    educations = service.list_educations(
        user_id=current_user.id,
        resume_id=resume_id,
    )

    return [
        EducationResponse.model_validate(
            education,
        )
        for education in educations
    ]


@router.get(
    "/{education_id}",
    response_model=EducationResponse,
)
def get_education(
    education_id: UUID,
    current_user: User = Depends(get_current_user),
    service: EducationService = Depends(
        get_education_service,
    ),
):
    education = service.get_education(
        user_id=current_user.id,
        education_id=education_id,
    )

    return EducationResponse.model_validate(
        education,
    )


@router.put(
    "/{education_id}",
    response_model=EducationResponse,
)
def update_education(
    education_id: UUID,
    payload: EducationUpdate,
    current_user: User = Depends(get_current_user),
    service: EducationService = Depends(
        get_education_service,
    ),
):
    education = service.update_education(
        user_id=current_user.id,
        education_id=education_id,
        institution=payload.institution,
        degree=payload.degree,
        field_of_study=payload.field_of_study,
        location=payload.location,
        grade=payload.grade,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_current=payload.is_current,
        description=payload.description,
        display_order=payload.display_order,
    )

    return EducationResponse.model_validate(
        education,
    )


@router.delete(
    "/{education_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_education(
    education_id: UUID,
    current_user: User = Depends(get_current_user),
    service: EducationService = Depends(
        get_education_service,
    ),
):
    service.delete_education(
        user_id=current_user.id,
        education_id=education_id,
    )
