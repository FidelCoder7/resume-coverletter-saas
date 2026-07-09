from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.common.constants import (
    AccountStatus,
    SubscriptionPlan,
    UserRole,
)


class UserProfileResponse(BaseModel):
    """
    Returned when fetching the authenticated user's profile.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    full_name: str

    is_email_verified: bool

    role: UserRole
    subscription_plan: SubscriptionPlan
    status: AccountStatus


class UpdateProfileRequest(BaseModel):
    """
    Fields a user is allowed to update.
    """

    full_name: str = Field(
        min_length=2,
        max_length=255,
    )
