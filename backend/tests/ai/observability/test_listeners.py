from unittest.mock import patch

from app.ai.observability.contracts import (
    ExecutionEvent,
    ExecutionStatus,
)
from app.ai.observability.listeners import StructuredLoggingListener


def build_event(status: ExecutionStatus) -> ExecutionEvent:
    return ExecutionEvent(
        execution_id="execution-123",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        status=status,
    )


def test_started_event_logs():
    listener = StructuredLoggingListener()
    event = build_event(ExecutionStatus.STARTED)

    with patch(
        "app.ai.observability.listeners.AIObservabilityLogger.execution_started"
    ) as mock_logger:
        listener.handle(event)

    mock_logger.assert_called_once_with(event)


def test_retry_event_logs():
    listener = StructuredLoggingListener()
    event = build_event(ExecutionStatus.RETRYING)

    with patch(
        "app.ai.observability.listeners.AIObservabilityLogger.retry_scheduled"
    ) as mock_logger:
        listener.handle(event)

    mock_logger.assert_called_once_with(event)


def test_success_event_logs():
    listener = StructuredLoggingListener()
    event = build_event(ExecutionStatus.SUCCEEDED)

    with patch(
        "app.ai.observability.listeners.AIObservabilityLogger.execution_succeeded"
    ) as mock_logger:
        listener.handle(event)

    mock_logger.assert_called_once_with(event)


def test_failed_event_logs():
    listener = StructuredLoggingListener()
    event = build_event(ExecutionStatus.FAILED)

    with patch(
        "app.ai.observability.listeners.AIObservabilityLogger.execution_failed"
    ) as mock_logger:
        listener.handle(event)

    mock_logger.assert_called_once_with(event)
