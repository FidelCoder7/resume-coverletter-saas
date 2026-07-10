from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.common.constants import SkillLevel


class CreateSkillRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )

    proficiency: SkillLevel

    display_order: int = Field(
        default=0,
        ge=0,
    )


class UpdateSkillRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )

    proficiency: SkillLevel

    display_order: int = Field(
        default=0,
        ge=0,
    )


class SkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    resume_id: UUID

    name: str
    proficiency: SkillLevel
    display_order: int

    created_at: datetime
    updated_at: datetime


class SkillListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skills: list[SkillResponse]
