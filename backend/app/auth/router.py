from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.schemas import (
    AccessTokenResponse,
    ForgotPasswordRequest,
    LogoutRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserResponse,
    VerifyEmailRequest,
)
from app.auth.service import AuthService
from app.core.config import settings
from app.core.rate_limit import limiter
from app.database.session import get_db
from app.email_verification.repository import (
    EmailVerificationRepository,
)
from app.email_verification.service import (
    EmailVerificationService,
)
from app.mail.service import MailService
from app.oauth.service import GoogleOAuthService
from app.password_reset.repository import (
    PasswordResetRepository,
)
from app.password_reset.service import (
    PasswordResetService,
)
from app.refresh_tokens.repository import RefreshTokenRepository
from app.users.models import User
from app.users.repository import UserRepository
from app.users.service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def get_user_service(db: Session) -> UserService:
    return UserService(
        UserRepository(db),
        EmailVerificationRepository(db),
    )


def get_auth_service(db: Session) -> AuthService:
    return AuthService(
        UserRepository(db),
        RefreshTokenRepository(db),
    )


def get_google_service(db: Session) -> GoogleOAuthService:
    return GoogleOAuthService(
        UserRepository(db),
        RefreshTokenRepository(db),
    )


def get_password_reset_service(db: Session) -> PasswordResetService:
    return PasswordResetService(
        PasswordResetRepository(db),
        UserRepository(db),
        MailService(),
    )


def get_email_verification_service(db: Session) -> EmailVerificationService:
    return EmailVerificationService(
        EmailVerificationRepository(db),
        UserRepository(db),
        MailService(),
    )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
@limiter.limit("3/minute")
def register(
    request: Request,
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    service = get_user_service(db)
    user = service.register(
        full_name=payload.full_name,
        email=payload.email,
        password=payload.password,
    )

    return UserResponse.model_validate(user)


@router.post(
    "/verify-email",
    status_code=204,
)
def verify_email(
    request: Request,
    payload: VerifyEmailRequest,
    db: Session = Depends(get_db),
):
    get_email_verification_service(db).verify_email(
        payload.token,
    )


@router.get(
    "/google/login",
    summary="Start Google OAuth login",
)
@limiter.limit("10/minute")
async def google_login(
    request: Request,
    db: Session = Depends(get_db),
):
    return await get_google_service(db).authorize_redirect(
        request=request,
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
    )


@router.get(
    "/google/callback",
    response_model=TokenResponse,
)
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    access_token, refresh_token, user = await get_google_service(db).authenticate(
        request
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/forgot-password",
    status_code=204,
)
@limiter.limit("3/minute")
def forgot_password(
    request: Request,
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    service = get_password_reset_service(db)

    user = service.user_repository.get_by_email(
        payload.email,
    )

    if user:
        service.request_password_reset(user)


@router.post(
    "/reset-password",
    status_code=204,
)
def reset_password(
    request: Request,
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    get_password_reset_service(db).reset_password(
        raw_token=payload.token,
        new_password=payload.new_password,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    service = get_auth_service(db)
    access_token, refresh_token, user = service.login(
        email=form_data.username,
        password=form_data.password,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/refresh",
    response_model=AccessTokenResponse,
)
@limiter.limit("20/minute")
def refresh(
    request: Request,
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    service = get_auth_service(db)
    access_token, refresh_token = service.refresh_access_token(
        payload.refresh_token,
    )

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
    get_auth_service(db).logout(
        request.refresh_token,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return UserResponse.model_validate(current_user)
