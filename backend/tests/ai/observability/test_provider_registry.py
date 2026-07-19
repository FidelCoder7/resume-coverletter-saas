from app.ai.observability.provider_registry import (
    ProviderHealthRegistry,
)


def test_provider_returns_same_instance():
    registry = ProviderHealthRegistry()

    first = registry.provider("openai")
    second = registry.provider("openai")

    assert first is second


def test_provider_creates_new_provider():
    registry = ProviderHealthRegistry()

    provider = registry.provider("anthropic")

    assert provider.provider == "anthropic"


def test_snapshot_contains_registered_providers():
    registry = ProviderHealthRegistry()

    registry.provider("openai")
    registry.provider("anthropic")

    snapshot = registry.snapshot()

    assert set(snapshot.keys()) == {
        "openai",
        "anthropic",
    }


def test_snapshot_returns_copy():
    registry = ProviderHealthRegistry()

    registry.provider("openai")

    snapshot = registry.snapshot()

    snapshot["new"] = registry.provider("anthropic")

    assert "new" not in registry.snapshot()


def test_snapshot_preserves_provider_state():
    registry = ProviderHealthRegistry()

    provider = registry.provider("openai")

    provider.total_requests = 12
    provider.successful_requests = 10
    provider.failed_requests = 2

    snapshot = registry.snapshot()

    assert snapshot["openai"].total_requests == 12
    assert snapshot["openai"].successful_requests == 10
    assert snapshot["openai"].failed_requests == 2
