from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.users.models import (
    AccountStatus,
    SubscriptionPlan,
    UserRole,
)


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    full_name: str

    role: UserRole
    subscription_plan: SubscriptionPlan
    status: AccountStatus


class TokenPayload(BaseModel):
    sub: str
    exp: int
    type: str
