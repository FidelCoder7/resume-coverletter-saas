from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.ai_usage.models import AIUsage
from app.common.constants import AIRequestStatus


class AIUsageRepository:
    """
    Repository responsible for AI usage persistence.

    AI usage records are immutable audit records and therefore
    support creation and querying only.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def _period_filter(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> tuple:
        return (
            AIUsage.user_id == user_id,
            AIUsage.created_at >= start_date,
            AIUsage.created_at < end_date,
        )

    def create(
        self,
        usage: AIUsage,
    ) -> AIUsage:
        """
        Persist an AI usage record.
        """

        self.db.add(
            usage,
        )

        self.db.commit()

        self.db.refresh(
            usage,
        )

        return usage

    def get_by_id(
        self,
        usage_id: UUID,
    ) -> AIUsage | None:
        """
        Retrieve an AI usage record by its identifier.
        """

        return self.db.get(
            AIUsage,
            usage_id,
        )

    def list_by_user(
        self,
        user_id: UUID,
    ) -> list[AIUsage]:
        """
        List all AI usage records belonging to a user.

        Most recent records are returned first.
        """

        statement = (
            select(
                AIUsage,
            )
            .where(
                AIUsage.user_id == user_id,
            )
            .order_by(
                AIUsage.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(
                statement,
            )
        )

    def list_by_resume(
        self,
        resume_id: UUID,
    ) -> list[AIUsage]:
        """
        List AI usage associated with a resume.

        Most recent records are returned first.
        """

        statement = (
            select(
                AIUsage,
            )
            .where(
                AIUsage.resume_id == resume_id,
            )
            .order_by(
                AIUsage.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(
                statement,
            )
        )

    def list_by_cover_letter(
        self,
        cover_letter_id: UUID,
    ) -> list[AIUsage]:
        """
        List AI usage associated with a cover letter.

        Most recent records are returned first.
        """

        statement = (
            select(
                AIUsage,
            )
            .where(
                AIUsage.cover_letter_id == cover_letter_id,
            )
            .order_by(
                AIUsage.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(
                statement,
            )
        )

    def count_by_user_and_period(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> int:
        """
        Count AI requests created by a user within a time period.
        """

        statement = select(
            func.count(AIUsage.id),
        ).where(
            *self._period_filter(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            )
        )

        return self.db.scalar(statement) or 0

    def sum_tokens_by_user_and_period(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> int:
        """
        Sum total tokens consumed by a user within a time period.
        """

        statement = select(
            func.sum(AIUsage.total_tokens),
        ).where(
            *self._period_filter(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            )
        )
        return self.db.scalar(statement) or 0

    def sum_cost_by_user_and_period(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> Decimal:
        """
        Sum estimated AI costs incurred by a user within a time period.
        """

        statement = select(
            func.sum(AIUsage.estimated_cost),
        ).where(
            *self._period_filter(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            )
        )

        return self.db.scalar(statement) or Decimal("0")

    def average_latency_by_user_and_period(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> float | None:
        """
        Return the average AI request latency for a user
        within the specified period.
        """

        statement = select(
            func.avg(
                AIUsage.latency_ms,
            )
        ).where(
            *self._period_filter(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            )
        )

        value = self.db.scalar(statement)

        return float(value) if value is not None else None

    def success_count_by_user_and_period(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> int:
        """
        Count successful AI requests for a user
        within the specified period.
        """

        statement = select(
            func.count(
                AIUsage.id,
            )
        ).where(
            *self._period_filter(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            ),
            AIUsage.status == AIRequestStatus.SUCCESS,
        )

        return self.db.scalar(statement) or 0

    def failure_count_by_user_and_period(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> int:
        """
        Count failed AI requests for a user
        within the specified period.
        """

        statement = select(
            func.count(
                AIUsage.id,
            )
        ).where(
            *self._period_filter(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            ),
            AIUsage.status == AIRequestStatus.FAILED,
        )

        return self.db.scalar(statement) or 0

    def requests_grouped_by_feature(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> dict:
        """
        Return request counts grouped by AI feature.
        """

        statement = (
            select(
                AIUsage.feature,
                func.count(
                    AIUsage.id,
                ),
            )
            .where(
                *self._period_filter(
                    user_id=user_id,
                    start_date=start_date,
                    end_date=end_date,
                )
            )
            .group_by(
                AIUsage.feature,
            )
        )

        return {
            feature: count
            for feature, count in self.db.execute(
                statement,
            ).all()
        }

    def tokens_grouped_by_feature(
        self,
        *,
        user_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> dict:
        """
        Return token usage grouped by AI feature.
        """

        statement = (
            select(
                AIUsage.feature,
                func.sum(
                    AIUsage.total_tokens,
                ),
            )
            .where(
                *self._period_filter(
                    user_id=user_id,
                    start_date=start_date,
                    end_date=end_date,
                )
            )
            .group_by(
                AIUsage.feature,
            )
        )

        return {
            feature: total or 0
            for feature, total in self.db.execute(
                statement,
            ).all()
        }
