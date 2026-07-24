from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.common.constants import ResumeVersionSource


class ResumeVersionBase(BaseModel):
    change_summary: str | None = Field(
        default=None,
        max_length=1000,
    )


class ResumeVersionCreate(ResumeVersionBase):
    snapshot: dict[str, Any]
    source: ResumeVersionSource = ResumeVersionSource.USER
    change_summary: str | None = None


class ResumeVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    resume_id: UUID
    version_number: int
    snapshot: dict[str, Any]
    change_summary: str | None
    source: ResumeVersionSource
    created_at: datetime
    updated_at: datetime
