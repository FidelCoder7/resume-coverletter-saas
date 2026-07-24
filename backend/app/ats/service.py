from datetime import UTC, datetime
from uuid import UUID

from app.ai.formatters import ResumeFormatter
from app.ats.ai_service import ATSAIService
from app.ats.schemas import ATSOptimizationResponse
from app.common.constants import ResumeVersionSource
from app.resume_versions.service import ResumeVersionService
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
        resume_version_service: ResumeVersionService,
    ) -> None:
        self.repository = repository
        self.ai_service = ai_service
        self.resume_version_service = resume_version_service

    def optimize_resume(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        job_description: str,
        target_job_title: str | None,
    ) -> ATSOptimizationResponse:
        """
        Optimize a resume for a target job.

        A successful ATS optimization:
        1. Verifies resume ownership.
        2. Generates an optimized resume.
        3. Persists the optimized content.
        4. Creates an immutable ATS resume version.
        5. Returns the ATS optimization analysis.
        """

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

        resume.generated_content = result.optimized_resume
        resume.generated_at = datetime.now(UTC)

        resume = self.repository.update(
            resume,
        )

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.ATS,
            change_summary=(
                "Resume optimized for ATS"
                + (f" for {target_job_title}." if target_job_title else ".")
            ),
        )

        return ATSOptimizationResponse(
            resume_id=resume.id,
            **result.model_dump(),
        )
