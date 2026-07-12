from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class CertificationBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=200,
    )

    issuing_organization: str = Field(
        min_length=1,
        max_length=200,
    )

    credential_id: str | None = Field(
        default=None,
        max_length=200,
    )

    credential_url: HttpUrl | None = None

    issue_date: date

    expiration_date: date | None = None

    does_not_expire: bool = False

    display_order: int = Field(
        default=0,
        ge=0,
    )


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(CertificationBase):
    pass


class CertificationResponse(CertificationBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    resume_id: UUID

    created_at: datetime
    updated_at: datetime


class CertificationListResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    certifications: list[CertificationResponse]
