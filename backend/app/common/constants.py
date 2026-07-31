from enum import StrEnum


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class AdminAuditAction(StrEnum):
    USER_SUSPENDED = "user_suspended"
    USER_ACTIVATED = "user_activated"
    USER_DELETED = "user_deleted"
    USER_RESTORED = "user_restored"
    USER_ROLE_CHANGED = "user_role_changed"
    USER_SUBSCRIPTION_CHANGED = "user_subscription_changed"


class AccountStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class SubscriptionPlan(StrEnum):
    FREE = "free"
    PRO = "pro"


class PaymentProvider(StrEnum):
    PESAPAL = "pesapal"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class PaymentMethod(StrEnum):
    MPESA = "mpesa"
    CARD = "card"
    BANK = "bank"
    OTHER = "other"


class BillingTransactionType(StrEnum):
    SUBSCRIPTION_PURCHASE = "subscription_purchase"
    SUBSCRIPTION_RENEWAL = "subscription_renewal"
    SUBSCRIPTION_UPGRADE = "subscription_upgrade"
    SUBSCRIPTION_DOWNGRADE = "subscription_downgrade"


class SubscriptionLimitPeriod(StrEnum):
    MONTHLY = "monthly"


class EmploymentType(StrEnum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"
    APPRENTICESHIP = "apprenticeship"
    TEMPORARY = "temporary"
    SEASONAL = "seasonal"
    VOLUNTEER = "volunteer"


class SkillLevel(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class AIFeature(StrEnum):
    COVER_LETTER_GENERATION = "cover_letter_generation"
    COVER_LETTER_REGENERATION = "cover_letter_regeneration"

    RESUME_GENERATION = "resume_generation"

    ATS_OPTIMIZATION = "ats_optimization"


class AIRequestStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ResumeVersionSource(StrEnum):
    USER = "user"
    AI = "ai"
    ATS = "ats"
    RESTORE = "restore"
    IMPORT = "import"
