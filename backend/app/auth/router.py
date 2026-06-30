from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.schemas import RegisterRequest, UserResponse
from app.auth.service import AuthService
from app.database.session import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    user = service.register(data)

    return UserResponse.model_validate(user)
