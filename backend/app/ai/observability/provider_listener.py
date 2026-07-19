from app.ai.observability.contracts import (
    ExecutionEvent,
    ExecutionStatus,
)
from app.ai.observability.listeners import (
    AIObservabilityListener,
)
from app.ai.observability.provider_registry import (
    ProviderHealthRegistry,
)


class ProviderHealthListener(
    AIObservabilityListener,
):
    """
    Updates runtime provider health.
    """

    def __init__(
        self,
        registry: ProviderHealthRegistry,
    ) -> None:
        self.registry = registry

    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        provider = self.registry.provider(
            event.provider,
        )

        match event.status:

            case ExecutionStatus.STARTED:
                provider.total_requests += 1

            case ExecutionStatus.SUCCEEDED:
                provider.successful_requests += 1
                provider.consecutive_failures = 0

                if event.duration_ms is not None:
                    provider.total_latency_ms += event.duration_ms

            case ExecutionStatus.FAILED:
                provider.failed_requests += 1
                provider.consecutive_failures += 1
