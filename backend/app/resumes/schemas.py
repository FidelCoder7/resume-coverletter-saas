from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


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
