from datetime import UTC, datetime

from app.ai.contracts import AIExecutionResult
from app.ai.formatters import ResumeFormatter
from app.ai.schemas import ResumeGenerationRequest
from app.ai.service import AIService
from app.ai_usage.service import AIUsageService
from app.common.constants import (
    AIFeature,
    ResumeVersionSource,
)
from app.resume_versions.service import ResumeVersionService
from app.resumes.exceptions import (
    ResumeAccessDenied,
    ResumeNotFound,
)
from app.resumes.models import Resume
from app.resumes.repository import ResumeRepository
from app.subscriptions.service import SubscriptionService
from app.users.models import User


class ResumeAIService:
    """
    Coordinates AI-powered resume generation.
    """

    def __init__(
        self,
        repository: ResumeRepository,
        ai_service: AIService,
        ai_usage_service: AIUsageService,
        resume_version_service: ResumeVersionService,
        subscription_service: SubscriptionService,
    ) -> None:
        self.repository = repository
        self.ai_service = ai_service
        self.ai_usage_service = ai_usage_service
        self.resume_version_service = resume_version_service
        self.subscription_service = subscription_service

    def _verify_resume_owner(
        self,
        *,
        resume_id,
        user: User,
    ) -> Resume:
        """
        Retrieve a resume with all related entities loaded and
        verify ownership.
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

        return resume

    def _check_generation_limit(
        self,
        *,
        user: User,
    ) -> None:
        """
        Enforce the user's subscription limit for AI resume generation.
        """

        self.subscription_service.check_limit(
            user=user,
            feature=AIFeature.RESUME_GENERATION,
        )

    def _record_ai_usage(
        self,
        *,
        user_id,
        resume_id,
        result: AIExecutionResult[str],
    ) -> None:
        """
        Persist telemetry for a successful AI resume generation.
        """

        self.ai_usage_service.record_success(
            user_id=user_id,
            resume_id=resume_id,
            feature=AIFeature.RESUME_GENERATION,
            metadata=result.metadata,
        )

    def generate_resume(
        self,
        *,
        user: User,
        resume_id,
        target_job_title: str | None,
        job_description: str | None,
    ) -> Resume:
        """
        Generate or refresh the AI-rendered version of a resume.

        A successful generation creates an immutable AI version snapshot.

        Subscription limits are checked before any AI execution occurs.
        """

        resume = self._verify_resume_owner(
            resume_id=resume_id,
            user=user,
        )

        self._check_generation_limit(
            user=user,
        )

        ai_request = ResumeGenerationRequest(
            resume_content=ResumeFormatter.format(
                resume,
            ),
            target_job_title=target_job_title,
            job_description=job_description,
        )

        try:
            ai_result = self.ai_service.generate_resume(
                ai_request,
                user_id=user.id,
                resume_id=resume_id,
            )

        except Exception as exc:
            self.ai_usage_service.record_failure(
                user_id=user.id,
                resume_id=resume.id,
                feature=AIFeature.RESUME_GENERATION,
                metadata=self.ai_service.provider.execution_metadata(),
                error_message=str(exc),
            )

            raise

        resume.generated_content = ai_result.content
        resume.generated_at = datetime.now(
            UTC,
        )

        resume = self.repository.update(
            resume,
        )

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.AI,
            change_summary="Resume generated using AI.",
        )

        self._record_ai_usage(
            user_id=user.id,
            resume_id=resume.id,
            result=ai_result,
        )

        return resume
