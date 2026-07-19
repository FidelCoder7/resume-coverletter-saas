from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.common.constants import (
    AIFeature,
    AIRequestStatus,
)


class AIUsageResponse(BaseModel):
    """
    API representation of an AI usage record.
    """

    id: UUID

    user_id: UUID

    resume_id: UUID | None

    cover_letter_id: UUID | None

    feature: AIFeature

    provider: str

    model: str

    prompt_version: str

    prompt_tokens: int | None

    completion_tokens: int | None

    total_tokens: int | None

    estimated_cost: Decimal | None

    latency_ms: int | None

    status: AIRequestStatus

    error_message: str | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class AIUsageListResponse(BaseModel):
    """
    Response returned when listing AI usage history.
    """

    items: list[AIUsageResponse]


class AIUsageSummary(BaseModel):
    """
    Aggregated AI usage statistics for a user during a period.
    """

    total_requests: int

    successful_requests: int

    failed_requests: int

    total_tokens: int

    estimated_cost: Decimal

    average_latency_ms: float | None


class AIFeatureUsage(BaseModel):
    """
    Usage statistics grouped by AI feature.
    """

    feature: AIFeature

    requests: int

    total_tokens: int


class AIUsageDashboard(BaseModel):
    """
    Dashboard response returned by the analytics service.
    """

    summary: AIUsageSummary

    features: list[AIFeatureUsage]
