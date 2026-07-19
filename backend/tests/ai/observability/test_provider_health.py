from app.ai.observability.provider_health import (
    ProviderHealthState,
)
from app.ai.observability.provider_health_status import (
    ProviderHealthStatus,
)


def test_success_rate():
    state = ProviderHealthState(provider="openai")

    state.total_requests = 10
    state.successful_requests = 9

    assert state.success_rate == 90.0


def test_average_latency():
    state = ProviderHealthState(provider="openai")

    state.successful_requests = 4
    state.total_latency_ms = 400

    assert state.average_latency_ms == 100.0


def test_status_healthy():
    state = ProviderHealthState(provider="openai")

    state.total_requests = 100
    state.successful_requests = 98

    assert state.status is ProviderHealthStatus.HEALTHY


def test_status_degraded():
    state = ProviderHealthState(provider="openai")

    state.total_requests = 100
    state.successful_requests = 90

    assert state.status is ProviderHealthStatus.DEGRADED


def test_status_unhealthy_due_to_success_rate():
    state = ProviderHealthState(provider="openai")

    state.total_requests = 100
    state.successful_requests = 70

    assert state.status is ProviderHealthStatus.UNHEALTHY


def test_status_unhealthy_due_to_consecutive_failures():
    state = ProviderHealthState(provider="openai")

    state.total_requests = 100
    state.successful_requests = 99
    state.consecutive_failures = 3

    assert state.status is ProviderHealthStatus.UNHEALTHY


def test_healthy_property():
    state = ProviderHealthState(provider="openai")

    state.total_requests = 20
    state.successful_requests = 20

    assert state.healthy is True
