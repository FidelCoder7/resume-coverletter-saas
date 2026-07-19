from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ExecutionStatus(StrEnum):
    """
    Lifecycle status for a single AI execution.
    """

    STARTED = "started"
    RETRYING = "retrying"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class ExecutionEvent(BaseModel):
    """
    Immutable event describing the lifecycle of an AI execution.

    These events are provider-agnostic and intended for structured
    logging, metrics, and future telemetry integrations.
    """

    execution_id: str

    provider: str
    model: str
    prompt_version: str
    operation: str

    status: ExecutionStatus

    attempt: int = 1
    retry_count: int = 0

    duration_ms: int | None = None

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    estimated_cost: float | None = None

    exception_type: str | None = None
    error_message: str | None = None

    # Correlation
    request_id: str | None = None
    user_id: str | None = None
    resume_id: str | None = None
    cover_letter_id: str | None = None

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    model_config = ConfigDict(
        frozen=True,
    )
