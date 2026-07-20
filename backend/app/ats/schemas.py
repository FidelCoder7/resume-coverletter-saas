from uuid import UUID

from pydantic import BaseModel, Field


class ATSOptimizationRequest(BaseModel):
    """
    Request payload for ATS resume optimization.
    """

    job_description: str = Field(
        min_length=1,
        max_length=10000,
    )

    target_job_title: str | None = Field(
        default=None,
        max_length=255,
    )


class ATSOptimizationResponse(BaseModel):
    """
    Response returned after ATS optimization.
    """

    resume_id: UUID

    optimized_resume: str

    ats_score: int = Field(
        ge=0,
        le=100,
    )

    matched_keywords: list[str]

    missing_keywords: list[str]

    recommendations: list[str]
