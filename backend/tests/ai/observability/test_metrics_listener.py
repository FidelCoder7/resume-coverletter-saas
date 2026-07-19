from unittest.mock import MagicMock

from app.ai.observability.contracts import (
    ExecutionEvent,
    ExecutionStatus,
)
from app.ai.observability.listeners import MetricsListener


def build_event() -> ExecutionEvent:
    return ExecutionEvent(
        execution_id="execution-1",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        status=ExecutionStatus.STARTED,
    )


def test_metrics_listener_records_event():
    metrics = MagicMock()

    listener = MetricsListener(
        metrics=metrics,
    )

    event = build_event()

    listener.handle(
        event,
    )

    metrics.record.assert_called_once_with(
        event,
    )
