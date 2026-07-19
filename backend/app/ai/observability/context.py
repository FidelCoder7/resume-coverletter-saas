from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from app.ai.observability.contracts import ExecutionEvent, ExecutionStatus


@dataclass(slots=True)
class AIExecutionContext:
    """
    Runtime context for a single AI execution.

    This object exists only for the lifetime of an execution and tracks
    execution state independently from provider-specific metadata.
    """

    provider: str
    model: str
    prompt_version: str
    operation: str
    request_id: str | None = None
    user_id: str | None = None
    resume_id: str | None = None
    cover_letter_id: str | None = None

    execution_id: str = field(default_factory=lambda: str(uuid4()))

    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
    ended_at: datetime | None = None

    attempt: int = 1
    retry_count: int = 0

    status: ExecutionStatus = ExecutionStatus.STARTED

    exception_type: str | None = None
    error_message: str | None = None

    prompt_tokens: int | None = field(
        default=None,
    )

    completion_tokens: int | None = field(
        default=None,
    )

    total_tokens: int | None = field(
        default=None,
    )

    estimated_cost: float | None = field(
        default=None,
    )

    @property
    def duration_ms(self) -> int | None:
        """
        Returns the execution duration in milliseconds once the execution
        has completed.
        """
        if self.ended_at is None:
            return None

        delta = self.ended_at - self.started_at
        return int(delta.total_seconds() * 1000)

    def mark_retry(self) -> None:
        """
        Record a retry attempt.
        """
        self.retry_count += 1
        self.attempt += 1
        self.status = ExecutionStatus.RETRYING

    def mark_success(self) -> None:
        """
        Mark the execution as successful.
        """
        self.ended_at = datetime.now(UTC)
        self.status = ExecutionStatus.SUCCEEDED

    def mark_failure(
        self,
        exception: Exception,
    ) -> None:
        """
        Mark the execution as failed.
        """
        self.ended_at = datetime.now(UTC)
        self.status = ExecutionStatus.FAILED
        self.exception_type = type(exception).__name__
        self.error_message = str(exception)

    def attach_usage(
        self,
        *,
        prompt_tokens: int | None,
        completion_tokens: int | None,
        total_tokens: int | None,
        estimated_cost: float | None,
    ) -> None:
        """
        Attach provider usage statistics to the execution context.
        """

        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens
        self.estimated_cost = estimated_cost

    def to_event(self) -> ExecutionEvent:
        """
        Convert the runtime context into an immutable execution event.
        """
        return ExecutionEvent(
            execution_id=self.execution_id,
            provider=self.provider,
            model=self.model,
            prompt_version=self.prompt_version,
            operation=self.operation,
            status=self.status,
            attempt=self.attempt,
            retry_count=self.retry_count,
            duration_ms=self.duration_ms,
            prompt_tokens=self.prompt_tokens,
            completion_tokens=self.completion_tokens,
            total_tokens=self.total_tokens,
            estimated_cost=self.estimated_cost,
            exception_type=self.exception_type,
            error_message=self.error_message,
            request_id=self.request_id,
            user_id=self.user_id,
            resume_id=self.resume_id,
            cover_letter_id=self.cover_letter_id,
        )
