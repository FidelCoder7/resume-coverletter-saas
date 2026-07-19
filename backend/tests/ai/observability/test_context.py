from datetime import UTC, datetime, timedelta

from app.ai.observability.context import AIExecutionContext
from app.ai.observability.contracts import ExecutionStatus


def test_context_initialization():
    context = AIExecutionContext(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    assert context.execution_id
    assert context.provider == "openai"
    assert context.attempt == 1
    assert context.retry_count == 0
    assert context.status is ExecutionStatus.STARTED
    assert context.duration_ms is None


def test_mark_retry():
    context = AIExecutionContext(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    context.mark_retry()

    assert context.retry_count == 1
    assert context.attempt == 2
    assert context.status is ExecutionStatus.RETRYING


def test_mark_success():
    context = AIExecutionContext(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    context.started_at = datetime.now(UTC) - timedelta(milliseconds=150)

    context.mark_success()

    assert context.status is ExecutionStatus.SUCCEEDED
    assert context.ended_at is not None
    assert context.duration_ms >= 150


def test_mark_failure():
    context = AIExecutionContext(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    context.mark_failure(ValueError("boom"))

    assert context.status is ExecutionStatus.FAILED
    assert context.exception_type == "ValueError"
    assert context.error_message == "boom"
    assert context.ended_at is not None


def test_to_event():
    context = AIExecutionContext(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    context.mark_retry()
    context.mark_success()

    context.prompt_tokens = 120
    context.completion_tokens = 480
    context.total_tokens = 600
    context.estimated_cost = 0.0032

    event = context.to_event()

    assert event.execution_id == context.execution_id
    assert event.provider == context.provider
    assert event.retry_count == 1
    assert event.attempt == 2
    assert event.status is ExecutionStatus.SUCCEEDED
    assert event.prompt_tokens == 120
    assert event.completion_tokens == 480
    assert event.total_tokens == 600
    assert event.estimated_cost == 0.0032


def test_attach_usage():
    context = AIExecutionContext(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    context.attach_usage(
        prompt_tokens=125,
        completion_tokens=510,
        total_tokens=635,
        estimated_cost=0.0042,
    )

    assert context.prompt_tokens == 125
    assert context.completion_tokens == 510
    assert context.total_tokens == 635
    assert context.estimated_cost == 0.0042
