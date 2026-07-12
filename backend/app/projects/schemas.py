from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ProjectBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=200,
    )

    description: str = Field(
        min_length=1,
    )

    technologies: str = Field(
        min_length=1,
    )

    project_url: HttpUrl | None = None

    repository_url: HttpUrl | None = None

    start_date: date | None = None

    end_date: date | None = None

    is_ongoing: bool = False

    display_order: int = Field(
        default=0,
        ge=0,
    )


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    resume_id: UUID

    created_at: datetime
    updated_at: datetime


class ProjectListResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    projects: list[ProjectResponse]
