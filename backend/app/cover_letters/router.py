from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.cover_letters.dependencies import get_cover_letter_service
from app.cover_letters.schemas import (
    CoverLetterCreate,
    CoverLetterListResponse,
    CoverLetterResponse,
    CoverLetterUpdate,
)
from app.cover_letters.service import CoverLetterService
from app.users.models import User

router = APIRouter(
    prefix="/cover-letters",
    tags=["Cover Letters"],
)


@router.post(
    "/resume/{resume_id}",
    response_model=CoverLetterResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_cover_letter(
    resume_id: UUID,
    payload: CoverLetterCreate,
    current_user: User = Depends(get_current_user),
    service: CoverLetterService = Depends(get_cover_letter_service),
):
    return service.create_cover_letter(
        user_id=current_user.id,
        resume_id=resume_id,
        title=payload.title,
        company_name=payload.company_name,
        job_title=payload.job_title,
        content=payload.content,
    )


@router.get(
    "/resume/{resume_id}",
    response_model=CoverLetterListResponse,
)
def list_cover_letters(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    service: CoverLetterService = Depends(get_cover_letter_service),
):
    return CoverLetterListResponse(
        cover_letters=service.list_cover_letters(
            user_id=current_user.id,
            resume_id=resume_id,
        ),
    )


@router.get(
    "/{cover_letter_id}",
    response_model=CoverLetterResponse,
)
def get_cover_letter(
    cover_letter_id: UUID,
    current_user: User = Depends(get_current_user),
    service: CoverLetterService = Depends(get_cover_letter_service),
):
    return service.get_cover_letter(
        user_id=current_user.id,
        cover_letter_id=cover_letter_id,
    )


@router.put(
    "/{cover_letter_id}",
    response_model=CoverLetterResponse,
)
def update_cover_letter(
    cover_letter_id: UUID,
    payload: CoverLetterUpdate,
    current_user: User = Depends(get_current_user),
    service: CoverLetterService = Depends(get_cover_letter_service),
):
    return service.update_cover_letter(
        user_id=current_user.id,
        cover_letter_id=cover_letter_id,
        title=payload.title,
        company_name=payload.company_name,
        job_title=payload.job_title,
        content=payload.content,
    )


@router.delete(
    "/{cover_letter_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_cover_letter(
    cover_letter_id: UUID,
    current_user: User = Depends(get_current_user),
    service: CoverLetterService = Depends(get_cover_letter_service),
):
    service.delete_cover_letter(
        user_id=current_user.id,
        cover_letter_id=cover_letter_id,
    )
