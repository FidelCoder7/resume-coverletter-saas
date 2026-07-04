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
    EmailNotVerified,
    InvalidCredentials,
    InvalidToken,
)
from app.auth.schemas import (
    AccessTokenResponse,
    LogoutRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
    VerifyEmailRequest,
)
from app.auth.service import AuthService
from app.database.session import get_db
from app.email_verification.exceptions import (
    VerificationTokenExpired,
    VerificationTokenInvalid,
)
from app.email_verification.repository import (
    EmailVerificationRepository,
)
from app.email_verification.service import (
    EmailVerificationService,
)
from app.mail.service import MailService
from app.refresh_tokens.repository import RefreshTokenRepository
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
    user_repository = UserRepository(db)

    verification_repository = EmailVerificationRepository(db)

    service = UserService(
        user_repository,
        verification_repository,
    )

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
    "/verify-email",
    status_code=204,
)
def verify_email(
    request: VerifyEmailRequest,
    db: Session = Depends(get_db),
):
    verification_repository = EmailVerificationRepository(db)

    user_repository = UserRepository(db)

    service = EmailVerificationService(
        verification_repository,
        user_repository,
        MailService(),
    )

    try:
        service.verify_email(
            request.token,
        )

    except VerificationTokenInvalid as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except VerificationTokenExpired as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    refresh_repository = RefreshTokenRepository(db)

    service = AuthService(
        user_repository,
        refresh_repository,
    )

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

    except EmailNotVerified as exc:
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
    user_repository = UserRepository(db)
    refresh_repository = RefreshTokenRepository(db)

    service = AuthService(
        user_repository,
        refresh_repository,
    )

    try:
        access_token, refresh_token = service.refresh_access_token(
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
        refresh_token=refresh_token,
    )


@router.post(
    "/logout",
    status_code=204,
)
def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    refresh_repository = RefreshTokenRepository(db)

    service = AuthService(
        user_repository,
        refresh_repository,
    )

    try:
        service.logout(
            request.refresh_token,
        )

    except InvalidToken as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        ) from exc


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
