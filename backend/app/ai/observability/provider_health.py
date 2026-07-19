from dataclasses import dataclass

from app.ai.observability.provider_health_status import (
    ProviderHealthStatus,
)


@dataclass(slots=True)
class ProviderHealthState:
    """
    Runtime health information for a single AI provider.
    """

    provider: str

    total_requests: int = 0

    successful_requests: int = 0

    failed_requests: int = 0

    consecutive_failures: int = 0

    total_latency_ms: int = 0

    @property
    def success_rate(self) -> float:
        """
        Percentage of successful requests.
        """
        if self.total_requests == 0:
            return 100.0

        return (self.successful_requests / self.total_requests) * 100

    @property
    def average_latency_ms(self) -> float:
        """
        Average latency for successful requests.
        """
        if self.successful_requests == 0:
            return 0.0

        return self.total_latency_ms / self.successful_requests

    @property
    def status(
        self,
    ) -> ProviderHealthStatus:
        """
        Current provider health.

        Phase 2 rules:

        • UNHEALTHY:
            3 or more consecutive failures
            OR success rate below 80%.

        • DEGRADED:
            success rate below 95%.

        • HEALTHY:
            everything else.
        """

        if self.consecutive_failures >= 3:
            return ProviderHealthStatus.UNHEALTHY

        if self.success_rate < 80:
            return ProviderHealthStatus.UNHEALTHY

        if self.success_rate < 95:
            return ProviderHealthStatus.DEGRADED

        return ProviderHealthStatus.HEALTHY

    @property
    def healthy(
        self,
    ) -> bool:
        """
        Convenience helper retained for backwards compatibility.
        """
        return self.status is ProviderHealthStatus.HEALTHY
