from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CoverLetterBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    company_name: str = Field(
        min_length=1,
        max_length=255,
    )

    job_title: str = Field(
        min_length=1,
        max_length=255,
    )

    content: str = Field(
        min_length=50,
    )


class CoverLetterCreate(CoverLetterBase):
    pass


class CoverLetterUpdate(CoverLetterBase):
    pass


class CoverLetterResponse(CoverLetterBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    resume_id: UUID

    created_at: datetime
    updated_at: datetime


class CoverLetterListResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    cover_letters: list[CoverLetterResponse]


class CoverLetterGenerateRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    company_name: str = Field(
        min_length=1,
        max_length=255,
    )

    job_title: str = Field(
        min_length=1,
        max_length=255,
    )

    job_description: str = Field(
        min_length=20,
    )


class CoverLetterRegenerateRequest(BaseModel):
    job_description: str = Field(
        min_length=20,
    )
