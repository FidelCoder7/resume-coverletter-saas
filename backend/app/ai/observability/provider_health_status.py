from enum import StrEnum


class ProviderHealthStatus(StrEnum):
    """
    Overall runtime health of an AI provider.
    """

    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNHEALTHY = "unhealthy"
