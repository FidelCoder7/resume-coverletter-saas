from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal

from app.admin.repository import AdminUserRepository
from app.admin.schemas import (
    AdminAIAnalyticsResponse,
    AdminAIAnalyticsTimeSeriesPoint,
    AdminAICostTimeSeriesPoint,
    AdminPaymentAnalyticsResponse,
    AdminPaymentAnalyticsTimeSeriesPoint,
    AdminPaymentRevenueTimeSeriesPoint,
    AdminSubscriptionAnalyticsResponse,
)
from app.ai_usage.repository import AIUsageRepository
from app.billing.repository import PaymentTransactionRepository
from app.common.constants import (
    AIRequestStatus,
    PaymentStatus,
    SubscriptionPlan,
)


class AdminAnalyticsService:
    """
    Service for platform-wide administrative analytics.

    This service is read-only. It coordinates aggregate queries across
    domain repositories and contains no HTTP-specific logic.
    """

    def __init__(
        self,
        *,
        user_repository: AdminUserRepository,
        payment_repository: PaymentTransactionRepository,
        ai_usage_repository: AIUsageRepository,
    ) -> None:
        self.user_repository = user_repository
        self.payment_repository = payment_repository
        self.ai_usage_repository = ai_usage_repository

    @staticmethod
    def _get_period(
        days: int,
    ) -> tuple[datetime, datetime]:
        """
        Return a UTC period containing exactly `days` calendar days.
        """

        today = datetime.now(UTC).date()
        start = today - timedelta(days=days - 1)
        end = today + timedelta(days=1)

        return (
            datetime.combine(
                start,
                time.min,
                tzinfo=UTC,
            ),
            datetime.combine(
                end,
                time.min,
                tzinfo=UTC,
            ),
        )

    @staticmethod
    def _fill_count_series(
        *,
        start_date: date,
        days: int,
        rows: list[tuple[date, int]],
    ) -> list[tuple[date, int]]:
        values = {row_date: count for row_date, count in rows}

        return [
            (
                current_date,
                values.get(
                    current_date,
                    0,
                ),
            )
            for current_date in (
                start_date + timedelta(days=offset) for offset in range(days)
            )
        ]

    @staticmethod
    def _fill_decimal_series(
        *,
        start_date: date,
        days: int,
        rows: list[tuple[date, Decimal]],
    ) -> list[tuple[date, Decimal]]:
        values = {row_date: Decimal(str(amount or 0)) for row_date, amount in rows}

        return [
            (
                current_date,
                values.get(
                    current_date,
                    Decimal("0"),
                ),
            )
            for current_date in (
                start_date + timedelta(days=offset) for offset in range(days)
            )
        ]

    def get_subscription_analytics(
        self,
    ) -> AdminSubscriptionAnalyticsResponse:
        """
        Return current subscription distribution.

        Historical subscription transitions are intentionally excluded
        because subscription history is not currently persisted.
        """

        plan_counts = self.user_repository.count_users_by_subscription_plan()

        free_users = plan_counts.get(
            SubscriptionPlan.FREE,
            0,
        )

        pro_users = plan_counts.get(
            SubscriptionPlan.PRO,
            0,
        )


        return AdminSubscriptionAnalyticsResponse(
            total_users=free_users + pro_users,
            free_users=free_users,
            pro_users=pro_users,
            active_subscriptions=pro_users,
        )

    def get_payment_analytics(
        self,
        *,
        days: int,
    ) -> AdminPaymentAnalyticsResponse:
        """
        Return payment analytics for the selected period.
        """

        start_date, end_date = self._get_period(days)

        total_transactions = self.payment_repository.count_by_period(
            start_date=start_date,
            end_date=end_date,
        )

        completed_transactions = self.payment_repository.count_by_status_and_period(
            status=PaymentStatus.COMPLETED,
            start_date=start_date,
            end_date=end_date,
        )

        pending_transactions = self.payment_repository.count_by_status_and_period(
            status=PaymentStatus.PENDING,
            start_date=start_date,
            end_date=end_date,
        )

        failed_transactions = self.payment_repository.count_by_status_and_period(
            status=PaymentStatus.FAILED,
            start_date=start_date,
            end_date=end_date,
        )

        cancelled_transactions = self.payment_repository.count_by_status_and_period(
            status=PaymentStatus.CANCELLED,
            start_date=start_date,
            end_date=end_date,
        )

        expired_transactions = self.payment_repository.count_by_status_and_period(
            status=PaymentStatus.EXPIRED,
            start_date=start_date,
            end_date=end_date,
        )

        transaction_rows = self.payment_repository.count_by_day(
            start_date=start_date,
            end_date=end_date,
        )

        transaction_rows = self._fill_count_series(
            start_date=start_date.date(),
            days=days,
            rows=transaction_rows,
        )

        revenue_rows = (
            self.payment_repository.sum_completed_amounts_by_day_and_currency(
                start_date=start_date,
                end_date=end_date,
            )
        )

        revenue_activity = {}

        for currency, rows in revenue_rows.items():
            filled_rows = self._fill_decimal_series(
                start_date=start_date.date(),
                days=days,
                rows=rows,
            )

            revenue_activity[currency] = [
                AdminPaymentRevenueTimeSeriesPoint(
                    date=row_date,
                    amount=amount,
                )
                for row_date, amount in filled_rows
            ]

        return AdminPaymentAnalyticsResponse(
            days=days,
            total_transactions=total_transactions,
            completed_transactions=completed_transactions,
            pending_transactions=pending_transactions,
            failed_transactions=failed_transactions,
            cancelled_transactions=cancelled_transactions,
            expired_transactions=expired_transactions,
            total_revenue_by_currency=(
                self.payment_repository.sum_completed_amounts_by_currency_and_period(
                    start_date=start_date,
                    end_date=end_date,
                )
            ),
            transactions_by_plan=self.payment_repository.count_by_plan(
                start_date=start_date,
                end_date=end_date,
            ),
            transactions_by_type=(
                self.payment_repository.count_by_transaction_type(
                    start_date=start_date,
                    end_date=end_date,
                )
            ),
            transactions_by_provider=(
                self.payment_repository.count_by_provider(
                    start_date=start_date,
                    end_date=end_date,
                )
            ),
            transactions_by_payment_method=(
                self.payment_repository.count_by_payment_method(
                    start_date=start_date,
                    end_date=end_date,
                )
            ),
            transaction_activity=[
                AdminPaymentAnalyticsTimeSeriesPoint(
                    date=row_date,
                    count=count,
                )
                for row_date, count in transaction_rows
            ],
            revenue_activity=revenue_activity,
        )

    def get_ai_analytics(
        self,
        *,
        days: int,
    ) -> AdminAIAnalyticsResponse:
        """
        Return AI usage analytics for the selected period.
        """

        start_date, end_date = self._get_period(days)

        total_requests = self.ai_usage_repository.count_by_period(
            start_date=start_date,
            end_date=end_date,
        )

        successful_requests = self.ai_usage_repository.count_by_status_and_period(
            status=AIRequestStatus.SUCCESS,
            start_date=start_date,
            end_date=end_date,
        )

        failed_requests = self.ai_usage_repository.count_by_status_and_period(
            status=AIRequestStatus.FAILED,
            start_date=start_date,
            end_date=end_date,
        )

        cancelled_requests = self.ai_usage_repository.count_by_status_and_period(
            status=AIRequestStatus.CANCELLED,
            start_date=start_date,
            end_date=end_date,
        )

        request_rows = self.ai_usage_repository.count_by_day(
            start_date=start_date,
            end_date=end_date,
        )

        token_rows = self.ai_usage_repository.sum_tokens_by_day(
            start_date=start_date,
            end_date=end_date,
        )

        cost_rows = self.ai_usage_repository.sum_cost_by_day(
            start_date=start_date,
            end_date=end_date,
        )

        request_rows = self._fill_count_series(
            start_date=start_date.date(),
            days=days,
            rows=request_rows,
        )

        token_rows = self._fill_count_series(
            start_date=start_date.date(),
            days=days,
            rows=token_rows,
        )

        cost_rows = self._fill_decimal_series(
            start_date=start_date.date(),
            days=days,
            rows=cost_rows,
        )

        return AdminAIAnalyticsResponse(
            days=days,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            cancelled_requests=cancelled_requests,
            total_tokens=self.ai_usage_repository.sum_total_tokens_by_period(
                start_date=start_date,
                end_date=end_date,
            ),
            estimated_cost=(
                self.ai_usage_repository.sum_estimated_cost_by_period(
                    start_date=start_date,
                    end_date=end_date,
                )
            ),
            average_latency_ms=(
                self.ai_usage_repository.average_latency_by_period(
                    start_date=start_date,
                    end_date=end_date,
                )
            ),
            requests_by_feature=(
                self.ai_usage_repository.requests_grouped_by_feature_and_period(
                    start_date=start_date,
                    end_date=end_date,
                )
            ),
            requests_by_status=(
                self.ai_usage_repository.requests_grouped_by_status(
                    start_date=start_date,
                    end_date=end_date,
                )
            ),
            tokens_by_feature=(
                self.ai_usage_repository.tokens_grouped_by_feature_and_period(
                    start_date=start_date,
                    end_date=end_date,
                )
            ),
            request_activity=[
                AdminAIAnalyticsTimeSeriesPoint(
                    date=row_date,
                    count=count,
                )
                for row_date, count in request_rows
            ],
            token_activity=[
                AdminAIAnalyticsTimeSeriesPoint(
                    date=row_date,
                    count=count,
                )
                for row_date, count in token_rows
            ],
            cost_activity=[
                AdminAICostTimeSeriesPoint(
                    date=row_date,
                    amount=amount,
                )
                for row_date, amount in cost_rows
            ],
        )
