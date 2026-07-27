from datetime import UTC, datetime

from app.ai.formatters import ResumeFormatter
from app.ats.ai_service import ATSAIService
from app.ats.schemas import ATSOptimizationResponse
from app.common.constants import (
    AIFeature,
    ResumeVersionSource,
)
from app.resume_versions.service import ResumeVersionService
from app.resumes.exceptions import (
    ResumeAccessDenied,
    ResumeNotFound,
)
from app.resumes.repository import ResumeRepository
from app.subscriptions.service import SubscriptionService
from app.users.models import User


class ATSService:
    """
    Coordinates ATS optimization workflows.
    """

    def __init__(
        self,
        repository: ResumeRepository,
        ai_service: ATSAIService,
        resume_version_service: ResumeVersionService,
        subscription_service: SubscriptionService,
    ) -> None:
        self.repository = repository
        self.ai_service = ai_service
        self.resume_version_service = resume_version_service
        self.subscription_service = subscription_service

    def optimize_resume(
        self,
        *,
        user: User,
        resume_id,
        job_description: str,
        target_job_title: str | None,
    ) -> ATSOptimizationResponse:
        """
        Optimize a resume for a target job.

        A successful ATS optimization:
        1. Verifies resume ownership.
        2. Checks the user's ATS optimization subscription limit.
        3. Generates an optimized resume.
        4. Persists the optimized content.
        5. Creates an immutable ATS resume version.
        6. Returns the ATS optimization analysis.

        Subscription limits are checked before AI execution.
        """

        resume = self.repository.get_for_generation(
            resume_id,
        )

        if resume is None:
            raise ResumeNotFound(
                "Resume not found.",
            )

        if resume.user_id != user.id:
            raise ResumeAccessDenied(
                "You do not have permission to access this resume.",
            )

        self.subscription_service.check_limit(
            user=user,
            feature=AIFeature.ATS_OPTIMIZATION,
        )

        result = self.ai_service.optimize(
            user_id=user.id,
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
