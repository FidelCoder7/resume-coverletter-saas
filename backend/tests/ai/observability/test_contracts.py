import pytest
from pydantic import ValidationError

from app.ai.observability.contracts import (
    ExecutionEvent,
    ExecutionStatus,
)


def test_execution_event_creation():
    event = ExecutionEvent(
        execution_id="exec-123",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        status=ExecutionStatus.STARTED,
    )

    assert event.execution_id == "exec-123"
    assert event.provider == "openai"
    assert event.status is ExecutionStatus.STARTED
    assert event.attempt == 1
    assert event.retry_count == 0
    assert event.duration_ms is None


def test_execution_event_is_frozen():
    event = ExecutionEvent(
        execution_id="exec-123",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        status=ExecutionStatus.STARTED,
    )

    with pytest.raises(ValidationError):
        event.provider = "anthropic"


@pytest.mark.parametrize(
    "status",
    list(ExecutionStatus),
)
def test_execution_status_enum(status):
    event = ExecutionEvent(
        execution_id="id",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="generate",
        status=status,
    )

    assert event.status is status
