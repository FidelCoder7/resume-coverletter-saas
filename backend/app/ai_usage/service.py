from datetime import datetime
from uuid import UUID

from app.ai.contracts import AIExecutionMetadata
from app.ai_usage.models import AIUsage
from app.ai_usage.repository import AIUsageRepository
from app.ai_usage.schemas import (
    AIFeatureUsage,
    AIUsageDashboard,
    AIUsageSummary,
)
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

    def _build_feature_usage(
        self,
        *,
        request_counts: dict,
        token_counts: dict,
    ) -> list[AIFeatureUsage]:
        """
        Build feature usage DTOs from repository aggregations.
        """

        features = sorted(
            set(request_counts) | set(token_counts),
            key=lambda feature: feature.value,
        )

        return [
            AIFeatureUsage(
                feature=feature,
                requests=request_counts.get(
                    feature,
                    0,
                ),
                total_tokens=token_counts.get(
                    feature,
                    0,
                ),
            )
            for feature in features
        ]

    def get_usage_summary(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> AIUsageSummary:
        """
        Return aggregated AI usage statistics for a user.
        """

        return AIUsageSummary(
            total_requests=self.repository.count_by_user_and_period(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            ),
            successful_requests=self.repository.success_count_by_user_and_period(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            ),
            failed_requests=self.repository.failure_count_by_user_and_period(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            ),
            total_tokens=self.repository.sum_tokens_by_user_and_period(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            ),
            estimated_cost=self.repository.sum_cost_by_user_and_period(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            ),
            average_latency_ms=self.repository.average_latency_by_user_and_period(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            ),
        )

    def get_feature_breakdown(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> list[AIFeatureUsage]:
        """
        Return AI usage grouped by feature.
        """

        request_counts = self.repository.requests_grouped_by_feature(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        token_counts = self.repository.tokens_grouped_by_feature(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        return self._build_feature_usage(
            request_counts=request_counts,
            token_counts=token_counts,
        )

    def get_dashboard(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> AIUsageDashboard:
        """
        Build a complete AI usage dashboard for a user.
        """

        return AIUsageDashboard(
            summary=self.get_usage_summary(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            ),
            features=self.get_feature_breakdown(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            ),
        )
