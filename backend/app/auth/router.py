from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.exceptions import (
    AccountInactive,
    EmailAlreadyRegistered,
    InvalidCredentials,
    InvalidToken,
)
from app.auth.schemas import (
    AccessTokenResponse,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.auth.service import AuthService
from app.database.session import get_db
from app.users.models import User
from app.users.repository import UserRepository
from app.users.service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)
    service = UserService(repository)

    try:
        user = service.register(
            full_name=payload.full_name,
            email=payload.email,
            password=payload.password,
        )

    except EmailAlreadyRegistered as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)
    service = AuthService(repository)

    try:
        access_token, refresh_token, user = service.login(
            email=form_data.username,
            password=form_data.password,
        )

    except InvalidCredentials as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        ) from exc

    except AccountInactive as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        ) from exc

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/refresh",
    response_model=AccessTokenResponse,
)
def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)
    service = AuthService(repository)

    try:
        access_token = service.refresh_access_token(
            request.refresh_token,
        )

    except InvalidToken as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        ) from exc

    except AccountInactive as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        ) from exc

    return AccessTokenResponse(
        access_token=access_token,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """

    return UserResponse.model_validate(current_user)
