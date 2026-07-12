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


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.
    """

    def add_handler(exc_type, status_code: int):
        @app.exception_handler(exc_type)
        async def handler(
            request: Request,
            exc: Exception,
        ):
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

    # Authentication

    add_handler(
        InvalidCredentials,
        401,
    )

    add_handler(
        InvalidToken,
        401,
    )

    add_handler(
        EmailAlreadyRegistered,
        409,
    )

    add_handler(
        EmailNotVerified,
        403,
    )

    add_handler(
        AccountInactive,
        403,
    )

    add_handler(
        OAuthAccountConflict,
        409,
    )

    # Google OAuth

    add_handler(
        GoogleAuthenticationFailed,
        401,
    )

    add_handler(
        GoogleAuthorizationCancelled,
        400,
    )

    add_handler(
        GoogleEmailNotAvailable,
        400,
    )

    add_handler(
        GoogleEmailNotVerified,
        403,
    )

    # Email verification

    add_handler(
        VerificationTokenInvalid,
        400,
    )

    add_handler(
        VerificationTokenExpired,
        400,
    )

    # Password reset

    add_handler(
        PasswordResetTokenInvalid,
        400,
    )

    add_handler(
        PasswordResetTokenExpired,
        400,
    )

    # Resume Management

    add_handler(
        ResumeNotFound,
        404,
    )

    add_handler(
        ResumeAccessDenied,
        403,
    )

    # Experience management

    add_handler(
        ExperienceNotFound,
        404,
    )

    add_handler(
        ExperienceAccessDenied,
        403,
    )

    # Education management

    add_handler(
        EducationNotFound,
        404,
    )

    add_handler(
        EducationAccessDenied,
        403,
    )

    # Skills management

    add_handler(
        SkillNotFound,
        404,
    )

    add_handler(
        SkillAccessDenied,
        403,
    )

    # Projects management

    add_handler(
        ProjectNotFound,
        404,
    )

    add_handler(
        ProjectAccessDenied,
        403,
    )

    add_handler(
        InvalidProjectDate,
        400,
    )

    # certification management
    add_handler(
        CertificationAccessDenied,
        403,
    )

    add_handler(
        CertificationNotFound,
        404,
    )

    add_handler(
        InvalidCertificationDate,
        400,
    )

    add_handler(
        DuplicateCertification,
        409,
    )
