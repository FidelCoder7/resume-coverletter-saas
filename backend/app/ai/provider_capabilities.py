from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderCapabilities:
    """
    Describes the features supported by an AI provider.

    Capabilities are provider-level feature flags used to determine
    which AI operations a provider can perform. They allow the AI
    platform to remain provider-agnostic while enabling future
    providers to support different subsets of functionality.
    """

    supports_cover_letters: bool = True

    supports_resume_generation: bool = True

    supports_ats_optimization: bool = True

    supports_streaming: bool = False

    supports_json_mode: bool = False

    supports_vision: bool = False
