from app.ai.observability.service import (
    AIObservabilityService,
)


def test_successful_execution_updates_metrics_and_provider_health():
    service = AIObservabilityService()

    context = service.execution_started(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    context.prompt_tokens = 120
    context.completion_tokens = 480
    context.total_tokens = 600
    context.estimated_cost = 0.0032

    service.execution_succeeded(
        context,
    )

    metrics = service.metrics_snapshot

    assert metrics.total_requests == 1
    assert metrics.successful_requests == 1
    assert metrics.failed_requests == 0
    assert metrics.retry_events == 0

    assert metrics.total_prompt_tokens == 120
    assert metrics.total_completion_tokens == 480
    assert metrics.total_tokens == 600
    assert metrics.total_estimated_cost == 0.0032

    provider = service.provider_health_snapshot["openai"]

    assert provider.provider == "openai"
    assert provider.total_requests == 1
    assert provider.successful_requests == 1
    assert provider.failed_requests == 0
    assert provider.consecutive_failures == 0
    assert provider.healthy


def test_failed_execution_updates_metrics_and_provider_health():
    service = AIObservabilityService()

    context = service.execution_started(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    service.execution_failed(
        context,
        RuntimeError("provider failure"),
    )

    metrics = service.metrics_snapshot

    assert metrics.total_requests == 1
    assert metrics.successful_requests == 0
    assert metrics.failed_requests == 1

    provider = service.provider_health_snapshot["openai"]

    assert provider.total_requests == 1
    assert provider.successful_requests == 0
    assert provider.failed_requests == 1
    assert provider.consecutive_failures == 1


def test_retry_execution_updates_all_components():
    service = AIObservabilityService()

    context = service.execution_started(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        operation="resume_generation",
    )

    service.execution_retry(
        context,
    )

    context.prompt_tokens = 50
    context.completion_tokens = 150
    context.total_tokens = 200
    context.estimated_cost = 0.001

    service.execution_succeeded(
        context,
    )

    metrics = service.metrics_snapshot

    assert metrics.total_requests == 1
    assert metrics.retry_events == 1
    assert metrics.successful_requests == 1

    provider = service.provider_health_snapshot["openai"]

    assert provider.total_requests == 1
    assert provider.successful_requests == 1
    assert provider.failed_requests == 0


def test_multiple_executions_accumulate_runtime_state():
    service = AIObservabilityService()

    for _ in range(3):
        context = service.execution_started(
            provider="openai",
            model="gpt-5",
            prompt_version="v1",
            operation="resume_generation",
        )

        service.execution_succeeded(
            context,
        )

    metrics = service.metrics_snapshot

    assert metrics.total_requests == 3
    assert metrics.successful_requests == 3
    assert metrics.failed_requests == 0

    provider = service.provider_health_snapshot["openai"]

    assert provider.total_requests == 3
    assert provider.successful_requests == 3
    assert provider.failed_requests == 0
