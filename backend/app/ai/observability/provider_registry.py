from app.ai.observability.provider_health import (
    ProviderHealthState,
)


class ProviderHealthRegistry:
    """
    Stores runtime health for all providers.
    """

    def __init__(self) -> None:
        self._providers: dict[
            str,
            ProviderHealthState,
        ] = {}

    def provider(
        self,
        name: str,
    ) -> ProviderHealthState:
        """
        Return the runtime health object for a provider.

        Lazily creates the provider entry on first access.
        """
        if name not in self._providers:
            self._providers[name] = ProviderHealthState(
                provider=name,
            )

        return self._providers[name]

    def snapshot(
        self,
    ) -> dict[str, ProviderHealthState]:
        """
        Return a read-only snapshot of the current registry.

        The returned dictionary is a shallow copy, preventing callers
        from mutating the registry structure.
        """
        return dict(
            self._providers,
        )
