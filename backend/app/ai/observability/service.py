from app.ai.observability.context import AIExecutionContext
from app.ai.observability.emitter import AIObservabilityEmitter
from app.ai.observability.listeners import (
    MetricsListener,
    StructuredLoggingListener,
)
from app.ai.observability.metrics import AIObservabilityMetrics
from app.ai.observability.metrics_snapshot import (
    AIObservabilityMetricsSnapshot,
)
from app.ai.observability.provider_health import (
    ProviderHealthState,
)
from app.ai.observability.provider_listener import (
    ProviderHealthListener,
)
from app.ai.observability.provider_registry import (
    ProviderHealthRegistry,
)


class AIObservabilityService:
    """
    Coordinates the observability lifecycle for AI executions.

    This service owns all runtime observability state.
    """

    def __init__(
        self,
        metrics: AIObservabilityMetrics | None = None,
        provider_registry: ProviderHealthRegistry | None = None,
        emitter: AIObservabilityEmitter | None = None,
    ) -> None:
        self.metrics = metrics if metrics is not None else AIObservabilityMetrics()

        self.provider_registry = (
            provider_registry
            if provider_registry is not None
            else ProviderHealthRegistry()
        )

        self.emitter = (
            emitter
            if emitter is not None
            else AIObservabilityEmitter(
                listeners=[
                    StructuredLoggingListener(),
                    MetricsListener(
                        self.metrics,
                    ),
                    ProviderHealthListener(
                        self.provider_registry,
                    ),
                ],
            )
        )

    @property
    def metrics_snapshot(
        self,
    ) -> AIObservabilityMetricsSnapshot:
        """
        Current immutable metrics snapshot.
        """
        return self.metrics.snapshot()

    @property
    def provider_health_snapshot(
        self,
    ) -> dict[str, ProviderHealthState]:
        """
        Current immutable provider health snapshot.
        """
        return self.provider_registry.snapshot()

    def execution_started(
        self,
        *,
        provider: str,
        model: str,
        prompt_version: str,
        operation: str,
        request_id: str | None = None,
        user_id: str | None = None,
        resume_id: str | None = None,
        cover_letter_id: str | None = None,
    ) -> AIExecutionContext:
        context = AIExecutionContext(
            provider=provider,
            model=model,
            prompt_version=prompt_version,
            operation=operation,
            request_id=request_id,
            user_id=user_id,
            resume_id=resume_id,
            cover_letter_id=cover_letter_id,
        )

        self.emitter.emit(
            context.to_event(),
        )

        return context

    def execution_retry(
        self,
        context: AIExecutionContext,
    ) -> None:
        context.mark_retry()

        self.emitter.emit(
            context.to_event(),
        )

    def execution_succeeded(
        self,
        context: AIExecutionContext,
    ) -> None:
        context.mark_success()

        self.emitter.emit(
            context.to_event(),
        )

    def execution_failed(
        self,
        context: AIExecutionContext,
        exception: Exception,
    ) -> None:
        context.mark_failure(
            exception,
        )

        self.emitter.emit(
            context.to_event(),
        )
