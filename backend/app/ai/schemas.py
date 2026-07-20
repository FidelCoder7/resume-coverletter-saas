from pydantic import BaseModel, Field


class CoverLetterGenerationRequest(BaseModel):
    """
    Internal request used by AI providers.
    """

    company_name: str = Field(min_length=1)
    job_title: str = Field(min_length=1)
    job_description: str = Field(min_length=1)
    resume_content: str = Field(min_length=1)


class ResumeGenerationRequest(BaseModel):
    """
    Internal request used by AI providers.
    """

    resume_content: str = Field(min_length=1)

    target_job_title: str | None = None

    job_description: str | None = None


class ATSOptimizationRequest(BaseModel):
    """
    Internal request used for ATS resume optimization.

    The optimization request is independent from resume generation.
    It compares an existing resume against a target job description
    and produces an optimized ATS-friendly version without inventing
    qualifications or modifying stored resume data.
    """

    resume_content: str = Field(min_length=1)

    job_description: str = Field(min_length=1)

    target_job_title: str | None = None


class ATSOptimizationResult(BaseModel):
    """
    Structured result returned by ATS optimization providers.
    """

    optimized_resume: str = Field(min_length=1)

    ats_score: int = Field(
        ge=0,
        le=100,
    )

    missing_keywords: list[str] = Field(
        default_factory=list,
    )

    matched_keywords: list[str] = Field(
        default_factory=list,
    )

    recommendations: list[str] = Field(
        default_factory=list,
    )
