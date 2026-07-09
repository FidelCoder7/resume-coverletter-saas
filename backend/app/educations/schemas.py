from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EducationBase(BaseModel):
    institution: str = Field(
        min_length=1,
        max_length=255,
    )

    degree: str = Field(
        min_length=1,
        max_length=255,
    )

    field_of_study: str = Field(
        min_length=1,
        max_length=255,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    grade: str | None = Field(
        default=None,
        max_length=100,
    )

    start_date: date

    end_date: date | None = None

    is_current: bool = False

    description: str | None = None

    display_order: int = Field(
        default=0,
        ge=0,
    )


class EducationCreate(EducationBase):
    pass


class EducationUpdate(EducationBase):
    pass


class EducationResponse(EducationBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    resume_id: UUID

    created_at: datetime
    updated_at: datetime
