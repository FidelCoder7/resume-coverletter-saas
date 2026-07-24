from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.certifications.schemas import CertificationCreate
from app.educations.schemas import EducationCreate
from app.experiences.schemas import CreateExperienceRequest
from app.projects.schemas import ProjectCreate
from app.skills.schemas import CreateSkillRequest


class CreateResumeRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    summary: str | None = Field(
        default=None,
        max_length=5000,
    )


class UpdateResumeRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    summary: str | None = Field(
        default=None,
        max_length=5000,
    )


class ResumeGenerationRequest(BaseModel):
    """
    Request payload for AI resume generation.
    """

    target_job_title: str | None = Field(
        default=None,
        max_length=255,
    )

    job_description: str | None = Field(
        default=None,
        max_length=10000,
    )


class ImportResumeRequest(BaseModel):
    """
    Request payload for importing a complete resume.

    The imported resume is persisted as a new resume with all
    associated child records and an initial IMPORT version.
    """

    title: str = Field(
        min_length=1,
        max_length=255,
    )

    summary: str | None = Field(
        default=None,
        max_length=5000,
    )

    experiences: list[CreateExperienceRequest] = Field(
        default_factory=list,
    )

    educations: list[EducationCreate] = Field(
        default_factory=list,
    )

    skills: list[CreateSkillRequest] = Field(
        default_factory=list,
    )

    projects: list[ProjectCreate] = Field(
        default_factory=list,
    )

    certifications: list[CertificationCreate] = Field(
        default_factory=list,
    )


class ResumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID

    title: str
    summary: str | None

    generated_content: str | None
    generated_at: datetime | None

    is_default: bool

    created_at: datetime
    updated_at: datetime


class ResumeListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    resumes: list[ResumeResponse]
