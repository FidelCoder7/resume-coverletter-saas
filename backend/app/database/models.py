"""
Import every ORM model here.

Alembic imports this module to discover
all SQLAlchemy metadata.
"""

from app.database.base import Base
from app.educations.models import Education
from app.email_verification.models import EmailVerificationToken
from app.experiences.models import Experience
from app.password_reset.models import PasswordResetToken
from app.projects.models import Project
from app.refresh_tokens.models import RefreshToken
from app.resumes.models import Resume
from app.skills.models import Skill
from app.users.models import User

# Future imports

__all__ = (
    "Base",
    "Education",
    "User",
    "Resume",
    "Experience",
    "RefreshToken",
    "EmailVerificationToken",
    "PasswordResetToken",
    "Skill",
    "Project",
)
