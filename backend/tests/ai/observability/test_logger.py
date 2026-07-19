from unittest.mock import patch

from app.ai.observability.contracts import (
    ExecutionEvent,
    ExecutionStatus,
)
from app.ai.observability.logger import AIObservabilityLogger


def create_event(status: ExecutionStatus = ExecutionStatus.STARTED):
    return ExecutionEvent(
        execution_id="exec-1",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        status=status,
        attempt=1,
        retry_count=0,
    )


def test_execution_started_logs():
    event = create_event()

    with patch("app.ai.observability.logger.logger") as mock_logger:
        AIObservabilityLogger.execution_started(event)

    mock_logger.info.assert_called_once()

    args, kwargs = mock_logger.info.call_args

    assert args[0] == "AI execution started."

    extra = kwargs["extra"]

    assert extra["execution_id"] == "exec-1"
    assert extra["provider"] == "openai"
    assert extra["model"] == "gpt-5"
    assert extra["operation"] == "resume_generation"
    assert extra["status"] == "started"
    assert extra["attempt"] == 1
    assert extra["retry_count"] == 0


def test_retry_scheduled_logs():

    event = create_event(ExecutionStatus.RETRYING)

    with patch("app.ai.observability.logger.logger") as mock_logger:
        AIObservabilityLogger.retry_scheduled(
            event,
            delay_ms=500,
        )
    mock_logger.warning.assert_called_once()

    args, kwargs = mock_logger.warning.call_args

    assert args[0] == "AI execution retry scheduled."

    extra = kwargs["extra"]

    assert extra["delay_ms"] == 500
    assert extra["status"] == "retrying"
    assert extra["attempt"] == 1
    assert extra["retry_count"] == 0


def test_execution_succeeded_logs():

    event = ExecutionEvent(
        execution_id="exec-1",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        status=ExecutionStatus.SUCCEEDED,
        duration_ms=125,
    )

    with patch("app.ai.observability.logger.logger") as mock_logger:
        AIObservabilityLogger.execution_succeeded(event)

    mock_logger.info.assert_called_once()

    args, kwargs = mock_logger.info.call_args

    assert args[0] == "AI execution completed."

    extra = kwargs["extra"]

    assert extra["duration_ms"] == 125
    assert extra["status"] == "succeeded"
    assert extra["execution_id"] == "exec-1"
    assert extra["provider"] == "openai"
    assert extra["model"] == "gpt-5"


def test_execution_failed_logs():
    event = ExecutionEvent(
        execution_id="exec-1",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        status=ExecutionStatus.FAILED,
        exception_type="RuntimeError",
        error_message="failure",
    )

    with patch("app.ai.observability.logger.logger") as mock_logger:
        AIObservabilityLogger.execution_failed(event)

    mock_logger.exception.assert_called_once()

    args, kwargs = mock_logger.exception.call_args

    assert args[0] == "AI execution failed."

    extra = kwargs["extra"]

    assert extra["exception_type"] == "RuntimeError"
    assert extra["error_message"] == "failure"
    assert extra["status"] == "failed"
