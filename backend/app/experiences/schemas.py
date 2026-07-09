from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.common.constants import EmploymentType


class CreateExperienceRequest(BaseModel):
    company: str = Field(
        min_length=1,
        max_length=255,
    )

    job_title: str = Field(
        min_length=1,
        max_length=255,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    employment_type: EmploymentType

    start_date: date

    end_date: date | None = None

    is_current: bool = False

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    display_order: int = Field(
        default=0,
        ge=0,
    )


class UpdateExperienceRequest(BaseModel):
    company: str = Field(
        min_length=1,
        max_length=255,
    )

    job_title: str = Field(
        min_length=1,
        max_length=255,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    employment_type: EmploymentType

    start_date: date

    end_date: date | None = None

    is_current: bool = False

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    display_order: int = Field(
        default=0,
        ge=0,
    )


class ExperienceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    resume_id: UUID

    company: str
    job_title: str
    location: str | None

    employment_type: EmploymentType

    start_date: date
    end_date: date | None

    is_current: bool

    description: str | None

    display_order: int

    created_at: datetime
    updated_at: datetime


class ExperienceListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    experiences: list[ExperienceResponse]
