from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.certifications.dependencies import get_certification_service
from app.certifications.schemas import (
    CertificationCreate,
    CertificationListResponse,
    CertificationResponse,
    CertificationUpdate,
)
from app.certifications.service import CertificationService
from app.users.models import User

router = APIRouter(
    prefix="/certifications",
    tags=["Certifications"],
)


@router.post(
    "/resume/{resume_id}",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_certification(
    resume_id: UUID,
    payload: CertificationCreate,
    current_user: User = Depends(get_current_user),
    service: CertificationService = Depends(get_certification_service),
):
    return service.create_certification(
        user_id=current_user.id,
        resume_id=resume_id,
        name=payload.name,
        issuing_organization=payload.issuing_organization,
        credential_id=payload.credential_id,
        credential_url=str(payload.credential_url) if payload.credential_url else None,
        issue_date=payload.issue_date,
        expiration_date=payload.expiration_date,
        does_not_expire=payload.does_not_expire,
        display_order=payload.display_order,
    )


@router.get(
    "/resume/{resume_id}",
    response_model=CertificationListResponse,
)
def list_certifications(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    service: CertificationService = Depends(get_certification_service),
):
    return CertificationListResponse(
        certifications=service.list_certifications(
            user_id=current_user.id,
            resume_id=resume_id,
        ),
    )


@router.get(
    "/{certification_id}",
    response_model=CertificationResponse,
)
def get_certification(
    certification_id: UUID,
    current_user: User = Depends(get_current_user),
    service: CertificationService = Depends(get_certification_service),
):
    return service.get_certification(
        user_id=current_user.id,
        certification_id=certification_id,
    )


@router.put(
    "/{certification_id}",
    response_model=CertificationResponse,
)
def update_certification(
    certification_id: UUID,
    payload: CertificationUpdate,
    current_user: User = Depends(get_current_user),
    service: CertificationService = Depends(get_certification_service),
):
    return service.update_certification(
        user_id=current_user.id,
        certification_id=certification_id,
        name=payload.name,
        issuing_organization=payload.issuing_organization,
        credential_id=payload.credential_id,
        credential_url=str(payload.credential_url) if payload.credential_url else None,
        issue_date=payload.issue_date,
        expiration_date=payload.expiration_date,
        does_not_expire=payload.does_not_expire,
        display_order=payload.display_order,
    )


@router.delete(
    "/{certification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_certification(
    certification_id: UUID,
    current_user: User = Depends(get_current_user),
    service: CertificationService = Depends(get_certification_service),
):
    service.delete_certification(
        user_id=current_user.id,
        certification_id=certification_id,
    )
