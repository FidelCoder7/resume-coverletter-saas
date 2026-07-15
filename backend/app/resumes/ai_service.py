from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from app.ai.contracts import AIExecutionResult
from app.ai.formatters import ResumeFormatter
from app.ai.schemas import ResumeGenerationRequest
from app.ai.service import AIService
from app.ai_usage.models import AIUsage
from app.ai_usage.repository import AIUsageRepository
from app.common.constants import (
    AIFeature,
    AIRequestStatus,
)
from app.resumes.exceptions import (
    ResumeAccessDenied,
    ResumeNotFound,
)
from app.resumes.models import Resume
from app.resumes.repository import ResumeRepository


class ResumeAIService:
    """
    Coordinates AI-powered resume generation.
    """

    def __init__(
        self,
        repository: ResumeRepository,
        ai_service: AIService,
        ai_usage_repository: AIUsageRepository,
    ) -> None:
        self.repository = repository
        self.ai_service = ai_service
        self.ai_usage_repository = ai_usage_repository

    def _verify_resume_owner(
        self,
        *,
        resume_id: UUID,
        user_id: UUID,
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

        if resume.user_id != user_id:
            raise ResumeAccessDenied(
                "You do not have permission to access this resume.",
            )

        return resume

    def _record_ai_usage(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        result: AIExecutionResult[str],
    ) -> None:
        """
        Persist telemetry for a successful AI resume generation.
        """

        metadata = result.metadata

        usage = AIUsage(
            user_id=user_id,
            resume_id=resume_id,
            cover_letter_id=None,
            feature=AIFeature.RESUME_GENERATION,
            provider=metadata.provider,
            model=metadata.model,
            prompt_version=metadata.prompt_version,
            prompt_tokens=metadata.prompt_tokens,
            completion_tokens=metadata.completion_tokens,
            total_tokens=metadata.total_tokens,
            estimated_cost=Decimal("0"),
            latency_ms=metadata.latency_ms,
            status=AIRequestStatus.SUCCESS,
            error_message=None,
        )

        self.ai_usage_repository.create(
            usage,
        )

    def generate_resume(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        target_job_title: str | None,
        job_description: str | None,
    ) -> Resume:
        """
        Generate or refresh the AI-rendered version of a resume.
        """

        resume = self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        ai_request = ResumeGenerationRequest(
            resume_content=ResumeFormatter.format(
                resume,
            ),
            target_job_title=target_job_title,
            job_description=job_description,
        )

        ai_result = self.ai_service.generate_resume(
            ai_request,
        )

        resume.generated_content = ai_result.content
        resume.generated_at = datetime.now(
            UTC,
        )

        resume = self.repository.update(
            resume,
        )

        self._record_ai_usage(
            user_id=user_id,
            resume_id=resume.id,
            result=ai_result,
        )

        return resume
