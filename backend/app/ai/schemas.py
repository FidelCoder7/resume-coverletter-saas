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
