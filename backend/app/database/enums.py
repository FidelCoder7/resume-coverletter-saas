from sqlalchemy import Enum

from app.common.constants import (
    AccountStatus,
    AdminAuditAction,
    AIFeature,
    AIRequestStatus,
    BillingTransactionType,
    EmploymentType,
    PaymentMethod,
    PaymentProvider,
    PaymentStatus,
    ResumeVersionSource,
    SkillLevel,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
    UserRole,
)

user_role_enum = Enum(
    UserRole,
    name="user_role",
)

admin_audit_action_enum = Enum(
    AdminAuditAction,
    name="admin_audit_action",
    values_callable=lambda enum_class: [member.value for member in enum_class],
    create_type=True,
)

account_status_enum = Enum(
    AccountStatus,
    name="account_status",
)

subscription_plan_enum = Enum(
    SubscriptionPlan,
    name="subscription_plan",
)

subscription_limit_period_enum = Enum(
    SubscriptionLimitPeriod,
    name="subscription_limit_period",
    values_callable=lambda enum_class: [member.value for member in enum_class],
    create_type=True,
)

payment_provider_enum = Enum(
    PaymentProvider,
    name="payment_provider",
    values_callable=lambda enum_class: [member.value for member in enum_class],
    create_type=True,
)

payment_status_enum = Enum(
    PaymentStatus,
    name="payment_status",
    values_callable=lambda enum_class: [member.value for member in enum_class],
    create_type=True,
)

payment_method_enum = Enum(
    PaymentMethod,
    name="payment_method",
    values_callable=lambda enum_class: [member.value for member in enum_class],
    create_type=True,
)

billing_transaction_type_enum = Enum(
    BillingTransactionType,
    name="billing_transaction_type",
    values_callable=lambda enum_class: [member.value for member in enum_class],
    create_type=True,
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

resume_version_source_enum = Enum(
    ResumeVersionSource,
    name="resume_version_source",
    values_callable=lambda enum_class: [member.value for member in enum_class],
    create_type=True,
)
