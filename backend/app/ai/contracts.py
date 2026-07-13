from typing import TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class AIExecutionMetadata(BaseModel):
    """
    Metadata describing a single AI execution.

    This metadata is provider-agnostic and is intended for
    telemetry, auditing, billing, and analytics.
    """

    provider: str
    model: str
    prompt_version: str

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None

    latency_ms: int | None = None

    model_config = ConfigDict(
        frozen=True,
    )


class AIExecutionResult[T](BaseModel):
    """
    Generic result returned by every AI provider.
    """

    content: T

    metadata: AIExecutionMetadata
