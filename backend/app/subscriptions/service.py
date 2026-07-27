from datetime import UTC, datetime

from app.ai_usage.repository import AIUsageRepository
from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)
from app.subscriptions.exceptions import (
    PlanLimitNotFound,
    SubscriptionLimitExceeded,
)
from app.subscriptions.models import PlanLimit
from app.subscriptions.repository import PlanLimitRepository
from app.subscriptions.schemas import (
    FeatureUsageResponse,
    PlanLimitListResponse,
    UsageStatusResponse,
)
from app.users.models import User


class SubscriptionService:
    """
    Coordinates subscription plan limits and AI usage enforcement.

    This service is responsible for:
    - Resolving configured limits for subscription plans.
    - Calculating current usage within the active usage period.
    - Determining remaining quota.
    - Enforcing subscription limits.

    AI usage persistence itself remains the responsibility of
    AIUsageRepository / AIUsageService.
    """

    def __init__(
        self,
        repository: PlanLimitRepository,
        ai_usage_repository: AIUsageRepository,
    ) -> None:
        self.repository = repository
        self.ai_usage_repository = ai_usage_repository

    @staticmethod
    def _get_current_month_period() -> tuple[datetime, datetime]:
        """
        Return the start and exclusive end of the current UTC month.

        Usage limits are currently defined as monthly limits.
        """

        now = datetime.now(UTC)

        period_start = datetime(
            year=now.year,
            month=now.month,
            day=1,
            tzinfo=UTC,
        )

        if now.month == 12:
            period_end = datetime(
                year=now.year + 1,
                month=1,
                day=1,
                tzinfo=UTC,
            )
        else:
            period_end = datetime(
                year=now.year,
                month=now.month + 1,
                day=1,
                tzinfo=UTC,
            )

        return period_start, period_end

    def get_plan_limit(
        self,
        *,
        subscription_plan: SubscriptionPlan,
        feature: AIFeature,
        period: SubscriptionLimitPeriod = SubscriptionLimitPeriod.MONTHLY,
    ) -> PlanLimit:
        """
        Retrieve the configured limit for a subscription plan and feature.

        Raises:
            PlanLimitNotFound:
                If no matching plan limit is configured.
        """

        plan_limit = self.repository.get_by_plan_and_feature(
            subscription_plan=subscription_plan,
            feature=feature,
            period=period,
        )

        if plan_limit is None:
            raise PlanLimitNotFound(
                f"No subscription limit configured for "
                f"plan={subscription_plan}, "
                f"feature={feature}, "
                f"period={period}.",
            )

        return plan_limit

    def list_plan_limits(
        self,
        *,
        subscription_plan: SubscriptionPlan,
    ) -> PlanLimitListResponse:
        """
        Return all configured limits for a subscription plan.
        """

        limits = self.repository.list_by_plan(
            subscription_plan=subscription_plan,
        )

        return PlanLimitListResponse(
            subscription_plan=subscription_plan,
            limits=limits,
        )

    def get_usage_status(
        self,
        *,
        user: User,
        feature: AIFeature,
        period: SubscriptionLimitPeriod = SubscriptionLimitPeriod.MONTHLY,
    ) -> UsageStatusResponse:
        """
        Return the current usage and quota status for a user's feature.

        Usage is calculated from immutable AI usage records created
        within the current usage period.
        """

        plan_limit = self.get_plan_limit(
            subscription_plan=user.subscription_plan,
            feature=feature,
            period=period,
        )

        period_start, period_end = self._get_current_month_period()

        usage = self.ai_usage_repository.count_by_user_and_feature_and_period(
            user_id=user.id,
            feature=feature,
            start_date=period_start,
            end_date=period_end,
        )

        remaining = max(
            plan_limit.limit_value - usage,
            0,
        )

        return UsageStatusResponse(
            subscription_plan=user.subscription_plan,
            feature=feature,
            limit_value=plan_limit.limit_value,
            usage=usage,
            remaining=remaining,
            period=period,
            period_start=period_start,
            period_end=period_end,
        )

    def check_limit(
        self,
        *,
        user: User,
        feature: AIFeature,
        period: SubscriptionLimitPeriod = SubscriptionLimitPeriod.MONTHLY,
    ) -> UsageStatusResponse:
        """
        Check whether the user can perform another request for a feature.

        The current usage is compared against the configured subscription
        limit. A user may perform another request when:

            usage < limit

        Once:

            usage >= limit

        the request is rejected.

        Raises:
            SubscriptionLimitExceeded:
                If the user's configured limit has been reached.
        """

        usage_status = self.get_usage_status(
            user=user,
            feature=feature,
            period=period,
        )

        if usage_status.usage >= usage_status.limit_value:
            raise SubscriptionLimitExceeded(
                subscription_plan=user.subscription_plan.value,
                feature=feature.value,
                limit=usage_status.limit_value,
                usage=usage_status.usage,
                period=period.value,
            )

        return usage_status

    def get_all_usage_status(
        self,
        *,
        user: User,
    ) -> list[FeatureUsageResponse]:
        """
        Return usage status for every configured AI feature
        available under the user's subscription plan.
        """

        limits = self.repository.list_by_plan(
            subscription_plan=user.subscription_plan,
        )

        period_start, period_end = self._get_current_month_period()

        usage_statuses: list[FeatureUsageResponse] = []

        for plan_limit in limits:
            usage = self.ai_usage_repository.count_by_user_and_feature_and_period(
                user_id=user.id,
                feature=plan_limit.feature,
                start_date=period_start,
                end_date=period_end,
            )

            usage_statuses.append(
                FeatureUsageResponse(
                    feature=plan_limit.feature,
                    limit_value=plan_limit.limit_value,
                    usage=usage,
                    remaining=max(
                        plan_limit.limit_value - usage,
                        0,
                    ),
                    period=plan_limit.period,
                )
            )

        return usage_statuses
