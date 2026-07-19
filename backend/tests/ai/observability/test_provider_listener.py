import pytest

from app.ai.observability.contracts import (
    ExecutionEvent,
    ExecutionStatus,
)
from app.ai.observability.provider_listener import (
    ProviderHealthListener,
)
from app.ai.observability.provider_registry import (
    ProviderHealthRegistry,
)


@pytest.fixture
def registry():
    return ProviderHealthRegistry()


@pytest.fixture
def listener(registry):
    return ProviderHealthListener(
        registry,
    )


def build_event(
    status,
    *,
    duration=100,
):
    return ExecutionEvent(
        execution_id="exec",
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
        status=status,
        duration_ms=duration,
    )


def test_started_increments_requests(
    listener,
    registry,
):
    listener.handle(
        build_event(
            ExecutionStatus.STARTED,
        )
    )

    provider = registry.provider(
        "openai",
    )

    assert provider.total_requests == 1


def test_success_records_latency(
    listener,
    registry,
):
    listener.handle(
        build_event(
            ExecutionStatus.STARTED,
        )
    )

    listener.handle(
        build_event(
            ExecutionStatus.SUCCEEDED,
            duration=220,
        )
    )

    provider = registry.provider(
        "openai",
    )

    assert provider.successful_requests == 1

    assert provider.total_latency_ms == 220

    assert provider.consecutive_failures == 0


def test_failure_increments_failure_counter(
    listener,
    registry,
):
    listener.handle(
        build_event(
            ExecutionStatus.STARTED,
        )
    )

    listener.handle(
        build_event(
            ExecutionStatus.FAILED,
        )
    )

    provider = registry.provider(
        "openai",
    )

    assert provider.failed_requests == 1

    assert provider.consecutive_failures == 1


def test_success_resets_consecutive_failures(
    listener,
    registry,
):
    listener.handle(
        build_event(
            ExecutionStatus.STARTED,
        )
    )

    listener.handle(
        build_event(
            ExecutionStatus.FAILED,
        )
    )

    listener.handle(
        build_event(
            ExecutionStatus.FAILED,
        )
    )

    listener.handle(
        build_event(
            ExecutionStatus.SUCCEEDED,
        )
    )

    provider = registry.provider(
        "openai",
    )

    assert provider.consecutive_failures == 0


def test_provider_becomes_unhealthy_after_three_failures(
    listener,
    registry,
):
    listener.handle(build_event(ExecutionStatus.STARTED))

    listener.handle(build_event(ExecutionStatus.FAILED))
    listener.handle(build_event(ExecutionStatus.FAILED))
    listener.handle(build_event(ExecutionStatus.FAILED))

    provider = registry.provider(
        "openai",
    )

    assert provider.healthy is False


def test_success_rate_updates_correctly(
    listener,
    registry,
):
    listener.handle(build_event(ExecutionStatus.STARTED))
    listener.handle(build_event(ExecutionStatus.SUCCEEDED))

    listener.handle(build_event(ExecutionStatus.STARTED))
    listener.handle(build_event(ExecutionStatus.FAILED))

    provider = registry.provider(
        "openai",
    )

    assert provider.total_requests == 2

    assert provider.successful_requests == 1

    assert provider.failed_requests == 1

    assert provider.success_rate == 50.0
