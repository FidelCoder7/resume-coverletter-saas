from abc import ABC, abstractmethod

from app.ai.observability.contracts import (
    ExecutionEvent,
    ExecutionStatus,
)
from app.ai.observability.logger import AIObservabilityLogger
from app.ai.observability.metrics import AIObservabilityMetrics


class AIObservabilityListener(ABC):
    """
    Base interface for observability event listeners.
    """

    @abstractmethod
    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        """
        Process an execution event.
        """


class StructuredLoggingListener(AIObservabilityListener):
    """
    Emits execution events to the structured logger.
    """

    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        match event.status:
            case ExecutionStatus.STARTED:
                AIObservabilityLogger.execution_started(event)

            case ExecutionStatus.RETRYING:
                AIObservabilityLogger.retry_scheduled(event)

            case ExecutionStatus.SUCCEEDED:
                AIObservabilityLogger.execution_succeeded(event)

            case ExecutionStatus.FAILED:
                AIObservabilityLogger.execution_failed(event)

            case _:
                raise AssertionError(
                    f"Unhandled execution status: {event.status!r}",
                )


class MetricsListener(AIObservabilityListener):
    """
    Records execution events into the metrics collector.
    """

    def __init__(
        self,
        metrics: AIObservabilityMetrics | None = None,
    ) -> None:
        self.metrics = metrics or AIObservabilityMetrics()

    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        self.metrics.record(
            event,
        )
