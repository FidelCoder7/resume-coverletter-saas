from enum import StrEnum


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class AccountStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class SubscriptionPlan(StrEnum):
    FREE = "free"
    PRO = "pro"
