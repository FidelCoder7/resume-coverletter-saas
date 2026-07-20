from uuid import UUID

from app.ai.formatters import ResumeFormatter
from app.ats.ai_service import ATSAIService
from app.ats.schemas import ATSOptimizationResponse
from app.resumes.exceptions import (
    ResumeAccessDenied,
    ResumeNotFound,
)
from app.resumes.repository import ResumeRepository


class ATSService:
    """
    Coordinates ATS optimization workflows.
    """

    def __init__(
        self,
        repository: ResumeRepository,
        ai_service: ATSAIService,
    ):
        self.repository = repository
        self.ai_service = ai_service

    def optimize_resume(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        job_description: str,
        target_job_title: str | None,
    ) -> ATSOptimizationResponse:

        resume = self.repository.get_for_generation(
            resume_id,
        )

        if resume is None:
            raise ResumeNotFound(
                "Resume not found.",
            )

        if resume.user_id != user_id:
            raise ResumeAccessDenied(
                "You do not have permission to access this resume.",
            )

        result = self.ai_service.optimize(
            user_id=user_id,
            resume_id=resume_id,
            resume_content=ResumeFormatter.format(resume),
            job_description=job_description,
            target_job_title=target_job_title,
        )

        return ATSOptimizationResponse(
            resume_id=resume_id,
            **result.model_dump(),
        )
