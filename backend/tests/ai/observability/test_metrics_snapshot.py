import pytest
from pydantic import ValidationError

from app.ai.observability.contracts import (
    ExecutionEvent,
    ExecutionStatus,
)
from app.ai.observability.metrics import AIObservabilityMetrics


def build_event(
    *,
    status: ExecutionStatus,
) -> ExecutionEvent:
    return ExecutionEvent(
        execution_id="exec-1",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        status=status,
        duration_ms=200,
        prompt_tokens=100,
        completion_tokens=200,
        total_tokens=300,
        estimated_cost=0.001,
    )


def test_snapshot_contains_current_metrics():
    metrics = AIObservabilityMetrics()

    metrics.record(
        build_event(
            status=ExecutionStatus.STARTED,
        ),
    )

    metrics.record(
        build_event(
            status=ExecutionStatus.SUCCEEDED,
        ),
    )

    snapshot = metrics.snapshot()

    assert snapshot.total_requests == 1

    assert snapshot.successful_requests == 1

    assert snapshot.failed_requests == 0

    assert snapshot.retry_events == 0

    assert snapshot.completed_requests == 1

    assert snapshot.total_tokens == 300

    assert snapshot.success_rate == 100.0


def test_snapshot_is_immutable():
    metrics = AIObservabilityMetrics()

    snapshot = metrics.snapshot()

    with pytest.raises(ValidationError):
        snapshot.total_requests = 99
