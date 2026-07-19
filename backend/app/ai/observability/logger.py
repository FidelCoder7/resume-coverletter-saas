import logging

from app.ai.observability.contracts import ExecutionEvent, ExecutionStatus

logger = logging.getLogger(__name__)


class AIObservabilityLogger:
    """
    Centralized structured logger for AI execution lifecycle events.

    This logger is provider-agnostic and operates exclusively on immutable
    execution events.
    """

    @staticmethod
    def execution_started(event: ExecutionEvent) -> None:
        """
        Log the start of an AI execution.
        """
        logger.info(
            "AI execution started.",
            extra={
                "execution_id": event.execution_id,
                "provider": event.provider,
                "model": event.model,
                "prompt_version": event.prompt_version,
                "operation": event.operation,
                "status": event.status.value,
                "attempt": event.attempt,
                "retry_count": event.retry_count,
                "request_id": event.request_id,
                "user_id": event.user_id,
                "resume_id": event.resume_id,
                "cover_letter_id": event.cover_letter_id,
            },
        )

    @staticmethod
    def retry_scheduled(
        event: ExecutionEvent,
        *,
        delay_ms: int | None = None,
    ) -> None:
        """
        Log a retry attempt.
        """
        logger.warning(
            "AI execution retry scheduled.",
            extra={
                "execution_id": event.execution_id,
                "provider": event.provider,
                "model": event.model,
                "prompt_version": event.prompt_version,
                "operation": event.operation,
                "status": event.status.value,
                "attempt": event.attempt,
                "retry_count": event.retry_count,
                "delay_ms": delay_ms,
            },
        )

    @staticmethod
    def execution_succeeded(event: ExecutionEvent) -> None:
        """
        Log a successful AI execution.
        """
        logger.info(
            "AI execution completed.",
            extra={
                "execution_id": event.execution_id,
                "provider": event.provider,
                "model": event.model,
                "prompt_version": event.prompt_version,
                "operation": event.operation,
                "status": event.status.value,
                "attempt": event.attempt,
                "retry_count": event.retry_count,
                "duration_ms": event.duration_ms,
            },
        )

    @staticmethod
    def execution_failed(event: ExecutionEvent) -> None:
        """
        Log a failed AI execution.
        """
        logger.exception(
            "AI execution failed.",
            extra={
                "execution_id": event.execution_id,
                "provider": event.provider,
                "model": event.model,
                "prompt_version": event.prompt_version,
                "operation": event.operation,
                "status": event.status.value,
                "attempt": event.attempt,
                "retry_count": event.retry_count,
                "duration_ms": event.duration_ms,
                "exception_type": event.exception_type,
                "error_message": event.error_message,
            },
        )

    def handle(
        self,
        event: ExecutionEvent,
    ) -> None:
        match event.status:
            case ExecutionStatus.STARTED:
                self.execution_started(event)

            case ExecutionStatus.RETRYING:
                self.retry_scheduled(event)

            case ExecutionStatus.SUCCEEDED:
                self.execution_succeeded(event)

            case ExecutionStatus.FAILED:
                self.execution_failed(event)

            case _:
                raise AssertionError(
                    f"Unhandled execution status: {event.status!r}",
                )
