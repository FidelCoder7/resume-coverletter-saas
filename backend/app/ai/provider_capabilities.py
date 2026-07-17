from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderCapabilities:
    """
    Describes the features supported by an AI provider.
    """

    supports_cover_letters: bool = True
    supports_resume_generation: bool = True
    supports_streaming: bool = False
    supports_json_mode: bool = False
    supports_vision: bool = False
