from dataclasses import dataclass

from app.ai.observability.contracts import (
    ExecutionEvent,
    ExecutionStatus,
)
from app.ai.observability.metrics_snapshot import (
    AIObservabilityMetricsSnapshot,
)


@dataclass(slots=True)
class AIObservabilityMetrics:
    """
    In-memory metrics collector for AI execution events.

    This implementation intentionally remains storage-agnostic.
    It can later back Prometheus, OpenTelemetry, CloudWatch,
    Azure Monitor, or any other metrics backend.
    """

    total_requests: int = 0

    successful_requests: int = 0

    failed_requests: int = 0

    retry_events: int = 0

    total_duration_ms: int = 0

    total_prompt_tokens: int = 0

    total_completion_tokens: int = 0

    total_tokens: int = 0

    total_estimated_cost: float = 0.0

    def record(
        self,
        event: ExecutionEvent,
    ) -> None:
        """
        Record a single execution lifecycle event.
        """

        match event.status:

            case ExecutionStatus.STARTED:
                self.total_requests += 1

            case ExecutionStatus.RETRYING:
                self.retry_events += 1

            case ExecutionStatus.SUCCEEDED:
                self.successful_requests += 1

                if event.duration_ms is not None:
                    self.total_duration_ms += event.duration_ms

                if event.prompt_tokens is not None:
                    self.total_prompt_tokens += event.prompt_tokens

                if event.completion_tokens is not None:
                    self.total_completion_tokens += event.completion_tokens

                if event.total_tokens is not None:
                    self.total_tokens += event.total_tokens

                if event.estimated_cost is not None:
                    self.total_estimated_cost += event.estimated_cost

            case ExecutionStatus.FAILED:
                self.failed_requests += 1

                if event.duration_ms is not None:
                    self.total_duration_ms += event.duration_ms

    @property
    def completed_requests(self) -> int:
        """
        Total completed executions (successes + failures).
        """
        return self.successful_requests + self.failed_requests

    @property
    def success_rate(self) -> float:
        """
        Success rate as a percentage.
        """
        if self.completed_requests == 0:
            return 0.0

        return (self.successful_requests / self.completed_requests) * 100

    @property
    def failure_rate(self) -> float:
        """
        Failure rate as a percentage.
        """
        if self.completed_requests == 0:
            return 0.0

        return (self.failed_requests / self.completed_requests) * 100

    @property
    def average_duration_ms(self) -> float:
        """
        Average execution duration.
        """
        if self.completed_requests == 0:
            return 0.0

        return self.total_duration_ms / self.completed_requests

    @property
    def average_prompt_tokens(self) -> float:
        if self.successful_requests == 0:
            return 0.0

        return self.total_prompt_tokens / self.successful_requests

    @property
    def average_completion_tokens(self) -> float:
        if self.successful_requests == 0:
            return 0.0

        return self.total_completion_tokens / self.successful_requests

    @property
    def average_total_tokens(self) -> float:
        if self.successful_requests == 0:
            return 0.0

        return self.total_tokens / self.successful_requests

    @property
    def average_estimated_cost(self) -> float:
        if self.successful_requests == 0:
            return 0.0

        return self.total_estimated_cost / self.successful_requests

    @property
    def average_retries_per_request(self) -> float:
        if self.total_requests == 0:
            return 0.0

        return self.retry_events / self.total_requests

    def snapshot(
        self,
    ) -> AIObservabilityMetricsSnapshot:
        """
        Return an immutable snapshot of the current metrics.
        """
        return AIObservabilityMetricsSnapshot(
            total_requests=self.total_requests,
            successful_requests=self.successful_requests,
            failed_requests=self.failed_requests,
            retry_events=self.retry_events,
            completed_requests=self.completed_requests,
            total_duration_ms=self.total_duration_ms,
            average_duration_ms=self.average_duration_ms,
            total_prompt_tokens=self.total_prompt_tokens,
            total_completion_tokens=self.total_completion_tokens,
            total_tokens=self.total_tokens,
            average_prompt_tokens=self.average_prompt_tokens,
            average_completion_tokens=self.average_completion_tokens,
            average_total_tokens=self.average_total_tokens,
            total_estimated_cost=self.total_estimated_cost,
            average_estimated_cost=self.average_estimated_cost,
            success_rate=self.success_rate,
            failure_rate=self.failure_rate,
            average_retries_per_request=self.average_retries_per_request,
        )
