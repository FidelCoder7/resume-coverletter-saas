from app.ai.observability.contracts import (
    ExecutionEvent,
    ExecutionStatus,
)
from app.ai.observability.metrics import AIObservabilityMetrics


def build_event(
    *,
    status: ExecutionStatus,
    duration_ms: int | None = None,
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
    total_tokens: int | None = None,
    estimated_cost: float | None = None,
) -> ExecutionEvent:
    return ExecutionEvent(
        execution_id="execution-123",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        status=status,
        attempt=1,
        retry_count=0,
        duration_ms=duration_ms,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        estimated_cost=estimated_cost,
    )


def test_started_increments_total_requests():
    metrics = AIObservabilityMetrics()

    metrics.record(
        build_event(
            status=ExecutionStatus.STARTED,
        ),
    )

    assert metrics.total_requests == 1

    assert metrics.successful_requests == 0
    assert metrics.failed_requests == 0
    assert metrics.retry_events == 0


def test_retrying_increments_retry_counter():
    metrics = AIObservabilityMetrics()

    metrics.record(
        build_event(
            status=ExecutionStatus.RETRYING,
        ),
    )

    assert metrics.retry_events == 1

    assert metrics.total_requests == 0
    assert metrics.successful_requests == 0
    assert metrics.failed_requests == 0


def test_success_records_usage_statistics():
    metrics = AIObservabilityMetrics()

    metrics.record(
        build_event(
            status=ExecutionStatus.SUCCEEDED,
            duration_ms=250,
            prompt_tokens=120,
            completion_tokens=330,
            total_tokens=450,
            estimated_cost=0.0035,
        ),
    )

    assert metrics.successful_requests == 1

    assert metrics.total_duration_ms == 250

    assert metrics.total_prompt_tokens == 120

    assert metrics.total_completion_tokens == 330

    assert metrics.total_tokens == 450

    assert metrics.total_estimated_cost == 0.0035


def test_failed_records_failure_and_duration():
    metrics = AIObservabilityMetrics()

    metrics.record(
        build_event(
            status=ExecutionStatus.FAILED,
            duration_ms=800,
        ),
    )

    assert metrics.failed_requests == 1

    assert metrics.total_duration_ms == 800


def test_multiple_events_are_accumulated():
    metrics = AIObservabilityMetrics()

    metrics.record(
        build_event(
            status=ExecutionStatus.STARTED,
        ),
    )

    metrics.record(
        build_event(
            status=ExecutionStatus.RETRYING,
        ),
    )

    metrics.record(
        build_event(
            status=ExecutionStatus.SUCCEEDED,
            duration_ms=300,
            prompt_tokens=100,
            completion_tokens=200,
            total_tokens=300,
            estimated_cost=0.001,
        ),
    )

    metrics.record(
        build_event(
            status=ExecutionStatus.FAILED,
            duration_ms=500,
        ),
    )

    assert metrics.total_requests == 1

    assert metrics.retry_events == 1

    assert metrics.successful_requests == 1

    assert metrics.failed_requests == 1

    assert metrics.total_duration_ms == 800

    assert metrics.total_prompt_tokens == 100

    assert metrics.total_completion_tokens == 200

    assert metrics.total_tokens == 300

    assert metrics.total_estimated_cost == 0.001


def test_success_without_optional_fields():
    metrics = AIObservabilityMetrics()

    metrics.record(
        build_event(
            status=ExecutionStatus.SUCCEEDED,
        ),
    )

    assert metrics.successful_requests == 1

    assert metrics.total_duration_ms == 0

    assert metrics.total_prompt_tokens == 0

    assert metrics.total_completion_tokens == 0

    assert metrics.total_tokens == 0

    assert metrics.total_estimated_cost == 0.0


def test_failed_without_duration():
    metrics = AIObservabilityMetrics()

    metrics.record(
        build_event(
            status=ExecutionStatus.FAILED,
        ),
    )

    assert metrics.failed_requests == 1

    assert metrics.total_duration_ms == 0


def test_derived_metrics_are_zero_when_empty():
    metrics = AIObservabilityMetrics()

    assert metrics.completed_requests == 0

    assert metrics.success_rate == 0.0
    assert metrics.failure_rate == 0.0

    assert metrics.average_duration_ms == 0.0

    assert metrics.average_prompt_tokens == 0.0
    assert metrics.average_completion_tokens == 0.0
    assert metrics.average_total_tokens == 0.0

    assert metrics.average_estimated_cost == 0.0

    assert metrics.average_retries_per_request == 0.0


def test_derived_metrics_are_calculated_correctly():
    metrics = AIObservabilityMetrics()

    metrics.record(
        build_event(
            status=ExecutionStatus.STARTED,
        ),
    )

    metrics.record(
        build_event(
            status=ExecutionStatus.RETRYING,
        ),
    )

    metrics.record(
        build_event(
            status=ExecutionStatus.SUCCEEDED,
            duration_ms=400,
            prompt_tokens=100,
            completion_tokens=300,
            total_tokens=400,
            estimated_cost=0.002,
        ),
    )

    metrics.record(
        build_event(
            status=ExecutionStatus.FAILED,
            duration_ms=600,
        ),
    )

    assert metrics.completed_requests == 2

    assert metrics.success_rate == 50.0
    assert metrics.failure_rate == 50.0

    assert metrics.average_duration_ms == 500.0

    assert metrics.average_prompt_tokens == 100.0

    assert metrics.average_completion_tokens == 300.0

    assert metrics.average_total_tokens == 400.0

    assert metrics.average_estimated_cost == 0.002

    assert metrics.average_retries_per_request == 1.0
