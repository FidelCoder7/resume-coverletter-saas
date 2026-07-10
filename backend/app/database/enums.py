from sqlalchemy import Enum

from app.common.constants import (
    AccountStatus,
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
