from logging import getLogger

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.auth.exceptions import (
    AccountInactive,
    EmailAlreadyRegistered,
    EmailNotVerified,
    InvalidCredentials,
    InvalidToken,
    OAuthAccountConflict,
)
from app.certifications.exceptions import (
    CertificationAccessDenied,
    CertificationNotFound,
    DuplicateCertification,
    InvalidCertificationDate,
)
from app.educations.exceptions import (
    EducationAccessDenied,
    EducationNotFound,
)
from app.email_verification.exceptions import (
    VerificationTokenExpired,
    VerificationTokenInvalid,
)
from app.experiences.exceptions import (
    ExperienceAccessDenied,
    ExperienceNotFound,
)
from app.oauth.exceptions import (
    GoogleAuthenticationFailed,
    GoogleAuthorizationCancelled,
    GoogleEmailNotAvailable,
    GoogleEmailNotVerified,
)
from app.password_reset.exceptions import (
    PasswordResetTokenExpired,
    PasswordResetTokenInvalid,
)
from app.projects.exceptions import (
    InvalidProjectDate,
    ProjectAccessDenied,
    ProjectNotFound,
)
from app.resumes.exceptions import (
    ResumeAccessDenied,
    ResumeNotFound,
)
from app.skills.exceptions import (
    SkillAccessDenied,
    SkillNotFound,
)

logger = getLogger(__name__)


EXCEPTION_HANDLERS: tuple[tuple[type[Exception], int], ...] = (
    # Authentication
    (InvalidCredentials, 401),
    (InvalidToken, 401),
    (EmailAlreadyRegistered, 409),
    (EmailNotVerified, 403),
    (AccountInactive, 403),
    (OAuthAccountConflict, 409),
    # Google OAuth
    (GoogleAuthenticationFailed, 401),
    (GoogleAuthorizationCancelled, 400),
    (GoogleEmailNotAvailable, 400),
    (GoogleEmailNotVerified, 403),
    # Email verification
    (VerificationTokenInvalid, 400),
    (VerificationTokenExpired, 400),
    # Password reset
    (PasswordResetTokenInvalid, 400),
    (PasswordResetTokenExpired, 400),
    # Resume management
    (ResumeNotFound, 404),
    (ResumeAccessDenied, 403),
    # Experience management
    (ExperienceNotFound, 404),
    (ExperienceAccessDenied, 403),
    # Education management
    (EducationNotFound, 404),
    (EducationAccessDenied, 403),
    # Skills management
    (SkillNotFound, 404),
    (SkillAccessDenied, 403),
    # Projects management
    (ProjectNotFound, 404),
    (ProjectAccessDenied, 403),
    (InvalidProjectDate, 400),
    # Certifications management
    (CertificationAccessDenied, 403),
    (CertificationNotFound, 404),
    (InvalidCertificationDate, 400),
    (DuplicateCertification, 409),
)


def _add_handler(
    app: FastAPI,
    exc_type: type[Exception],
    status_code: int,
) -> None:
    @app.exception_handler(exc_type)
    async def handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.warning(
            "%s: %s",
            exc_type.__name__,
            exc,
        )

        return JSONResponse(
            status_code=status_code,
            content={
                "detail": str(exc),
            },
        )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.
    """
    for exc_type, status_code in EXCEPTION_HANDLERS:
        _add_handler(
            app,
            exc_type,
            status_code,
        )