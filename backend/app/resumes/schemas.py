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


class ResumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID

    title: str
    summary: str | None

    is_default: bool

    created_at: datetime
    updated_at: datetime


class ResumeListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    resumes: list[ResumeResponse]
