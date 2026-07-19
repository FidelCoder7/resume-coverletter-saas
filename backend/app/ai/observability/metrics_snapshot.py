from pydantic import BaseModel, ConfigDict


class AIObservabilityMetricsSnapshot(BaseModel):
    """
    Immutable snapshot of the current AI observability metrics.
    """

    model_config = ConfigDict(
        frozen=True,
    )

    total_requests: int

    successful_requests: int

    failed_requests: int

    retry_events: int

    completed_requests: int

    total_duration_ms: int

    average_duration_ms: float

    total_prompt_tokens: int

    total_completion_tokens: int

    total_tokens: int

    average_prompt_tokens: float

    average_completion_tokens: float

    average_total_tokens: float

    total_estimated_cost: float

    average_estimated_cost: float

    success_rate: float

    failure_rate: float

    average_retries_per_request: float
