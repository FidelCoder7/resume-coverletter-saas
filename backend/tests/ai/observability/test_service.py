from unittest.mock import patch

import pytest

from app.ai.observability.context import AIExecutionContext
from app.ai.observability.contracts import ExecutionStatus
from app.ai.observability.service import AIObservabilityService


@pytest.fixture
def service() -> AIObservabilityService:
    return AIObservabilityService()


def test_execution_started_creates_context_and_emits(service):
    with patch.object(
        service.emitter,
        "emit",
    ) as mock_emit:
        context = service.execution_started(
            provider="openai",
            model="gpt-5",
            prompt_version="v1",
            operation="resume_generation",
        )

    assert isinstance(
        context,
        AIExecutionContext,
    )

    assert context.provider == "openai"
    assert context.model == "gpt-5"
    assert context.prompt_version == "v1"
    assert context.operation == "resume_generation"
    assert context.status is ExecutionStatus.STARTED

    mock_emit.assert_called_once()

    event = mock_emit.call_args.args[0]

    assert event.execution_id == context.execution_id
    assert event.provider == context.provider
    assert event.model == context.model
    assert event.prompt_version == context.prompt_version
    assert event.operation == context.operation
    assert event.status is ExecutionStatus.STARTED


def test_execution_retry_marks_context_and_emits(service):
    context = AIExecutionContext(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    with patch.object(
        service.emitter,
        "emit",
    ) as mock_emit:
        service.execution_retry(context)

    assert context.status is ExecutionStatus.RETRYING
    assert context.retry_count == 1
    assert context.attempt == 2

    mock_emit.assert_called_once()

    event = mock_emit.call_args.args[0]

    assert event.retry_count == 1
    assert event.attempt == 2


def test_execution_succeeded_marks_context_and_emits(service):
    context = AIExecutionContext(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    with patch.object(
        service.emitter,
        "emit",
    ) as mock_emit:
        service.execution_succeeded(context)

    assert context.status is ExecutionStatus.SUCCEEDED
    assert context.ended_at is not None
    assert context.duration_ms is not None

    mock_emit.assert_called_once()

    event = mock_emit.call_args.args[0]

    assert event.status is ExecutionStatus.SUCCEEDED
    assert event.duration_ms == context.duration_ms


def test_execution_failed_marks_context_and_emits(service):
    context = AIExecutionContext(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    exception = RuntimeError("provider failure")

    with patch.object(
        service.emitter,
        "emit",
    ) as mock_emit:
        service.execution_failed(
            context,
            exception,
        )

    assert context.status is ExecutionStatus.FAILED
    assert context.exception_type == "RuntimeError"
    assert context.error_message == "provider failure"

    mock_emit.assert_called_once()

    event = mock_emit.call_args.args[0]

    assert event.status is ExecutionStatus.FAILED
    assert event.exception_type == "RuntimeError"
    assert event.error_message == "provider failure"
