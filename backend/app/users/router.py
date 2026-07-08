from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.users.dependencies import get_user_service
from app.users.models import User
from app.users.schemas import (
    UpdateProfileRequest,
    UserProfileResponse,
)
from app.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserProfileResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.get_profile(current_user.id)


@router.patch(
    "/me",
    response_model=UserProfileResponse,
)
def update_my_profile(
    payload: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.update_profile(
        user_id=current_user.id,
        full_name=payload.full_name,
    )


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_account(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    service.delete_account(current_user.id)
