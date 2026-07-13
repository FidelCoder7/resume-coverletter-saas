from sqlalchemy import Enum

from app.common.constants import (
    AccountStatus,
    AIFeature,
    AIRequestStatus,
    EmploymentType,
    SkillLevel,
    SubscriptionPlan,
    UserRole,
)

user_role_enum = Enum(
    UserRole,
    name="user_role",
)

account_status_enum = Enum(
    AccountStatus,
    name="account_status",
)

subscription_plan_enum = Enum(
    SubscriptionPlan,
    name="subscription_plan",
)

employment_type_enum = Enum(
    EmploymentType,
    name="employment_type",
)

skill_level_enum = Enum(
    SkillLevel,
    name="skill_level",
    create_type=True,
)

ai_feature_enum = Enum(
    AIFeature,
    name="ai_feature",
    create_type=True,
)

ai_request_status_enum = Enum(
    AIRequestStatus,
    name="ai_request_status",
    create_type=True,
)
