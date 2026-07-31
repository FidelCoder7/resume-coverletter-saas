from dataclasses import dataclass


@dataclass(frozen=True)
class RenderedResume:
    """
    Represents a completed resume export produced by a renderer.
    """

    content: bytes
    filename: str
    media_type: str
