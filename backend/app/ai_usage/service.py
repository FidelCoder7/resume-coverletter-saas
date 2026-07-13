from uuid import UUID

from app.ai.contracts import AIExecutionMetadata
from app.ai_usage.models import AIUsage
from app.ai_usage.repository import AIUsageRepository
from app.common.constants import (
    AIFeature,
    AIRequestStatus,
)


class AIUsageService:
    """
    Business logic for AI usage tracking.

    This service records immutable AI execution events and
    exposes read-only access to AI usage history.
    """

    def __init__(
        self,
        repository: AIUsageRepository,
    ) -> None:
        self.repository = repository

    def _create_usage(
        self,
        *,
        user_id: UUID,
        feature: AIFeature,
        metadata: AIExecutionMetadata,
        status: AIRequestStatus,
        error_message: str | None = None,
        resume_id: UUID | None = None,
        cover_letter_id: UUID | None = None,
    ) -> AIUsage:
        """
        Create and persist an immutable AI usage record.
        """

        usage = AIUsage(
            user_id=user_id,
            resume_id=resume_id,
            cover_letter_id=cover_letter_id,
            feature=feature,
            provider=metadata.provider,
            model=metadata.model,
            prompt_version=metadata.prompt_version,
            prompt_tokens=metadata.prompt_tokens,
            completion_tokens=metadata.completion_tokens,
            total_tokens=metadata.total_tokens,
            estimated_cost=None,
            latency_ms=metadata.latency_ms,
            status=status,
            error_message=error_message,
        )

        return self.repository.create(
            usage,
        )

    def record_success(
        self,
        *,
        user_id: UUID,
        feature: AIFeature,
        metadata: AIExecutionMetadata,
        resume_id: UUID | None = None,
        cover_letter_id: UUID | None = None,
    ) -> AIUsage:
        """
        Record a successful AI execution.
        """

        return self._create_usage(
            user_id=user_id,
            feature=feature,
            metadata=metadata,
            status=AIRequestStatus.SUCCESS,
            resume_id=resume_id,
            cover_letter_id=cover_letter_id,
        )

    def record_failure(
        self,
        *,
        user_id: UUID,
        feature: AIFeature,
        metadata: AIExecutionMetadata,
        error_message: str,
        resume_id: UUID | None = None,
        cover_letter_id: UUID | None = None,
    ) -> AIUsage:
        """
        Record a failed AI execution.
        """

        return self._create_usage(
            user_id=user_id,
            feature=feature,
            metadata=metadata,
            status=AIRequestStatus.FAILED,
            error_message=error_message,
            resume_id=resume_id,
            cover_letter_id=cover_letter_id,
        )

    def get_usage(
        self,
        *,
        usage_id: UUID,
    ) -> AIUsage | None:
        """
        Retrieve an AI usage record by its identifier.
        """

        return self.repository.get_by_id(
            usage_id,
        )

    def list_user_history(
        self,
        *,
        user_id: UUID,
    ) -> list[AIUsage]:
        """
        Return the AI execution history for a user.
        """

        return self.repository.list_by_user(
            user_id,
        )

    def list_resume_history(
        self,
        *,
        resume_id: UUID,
    ) -> list[AIUsage]:
        """
        Return the AI execution history associated with a resume.
        """

        return self.repository.list_by_resume(
            resume_id,
        )

    def list_cover_letter_history(
        self,
        *,
        cover_letter_id: UUID,
    ) -> list[AIUsage]:
        """
        Return the AI execution history associated with a cover letter.
        """

        return self.repository.list_by_cover_letter(
            cover_letter_id,
        )
