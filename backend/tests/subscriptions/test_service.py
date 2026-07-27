import pytest

from app.ai.contracts import AIExecutionMetadata
from app.ai_usage.repository import AIUsageRepository
from app.ai_usage.service import AIUsageService
from app.common.constants import (
    AIFeature,
    SubscriptionLimitPeriod,
    SubscriptionPlan,
)
from app.subscriptions.exceptions import (
    SubscriptionLimitExceeded,
)
from app.subscriptions.repository import PlanLimitRepository
from app.subscriptions.service import SubscriptionService
from tests.factories.user_factory import create_user


def create_service(
    db_session,
) -> SubscriptionService:
    return SubscriptionService(
        repository=PlanLimitRepository(
            db_session,
        ),
        ai_usage_repository=AIUsageRepository(
            db_session,
        ),
    )


def test_get_plan_limit_returns_configured_limit(
    db_session,
):

    service = create_service(
        db_session,
    )

    result = service.get_plan_limit(
        subscription_plan=SubscriptionPlan.FREE,
        feature=AIFeature.RESUME_GENERATION,
    )

    assert result.subscription_plan == SubscriptionPlan.FREE
    assert result.feature == AIFeature.RESUME_GENERATION
    assert result.limit_value == 3
    assert result.period == SubscriptionLimitPeriod.MONTHLY


def test_check_limit_allows_request_when_usage_is_below_limit(
    db_session,
):
    user = create_user(
        db_session,
        subscription_plan=SubscriptionPlan.FREE,
        verified=True,
    )

    service = create_service(
        db_session,
    )

    result = service.check_limit(
        user=user,
        feature=AIFeature.RESUME_GENERATION,
    )

    assert result.limit_value == 3
    assert result.usage == 0
    assert result.remaining == 3


def test_check_limit_raises_when_usage_reaches_limit(
    db_session,
):
    user = create_user(
        db_session,
        subscription_plan=SubscriptionPlan.FREE,
        verified=True,
    )

    usage_service = AIUsageService(
        AIUsageRepository(db_session),
    )

    metadata = AIExecutionMetadata(
        provider="fake",
        model="fake",
        prompt_version="v1",
        prompt_tokens=1,
        completion_tokens=1,
        total_tokens=2,
        latency_ms=1,
        estimated_cost=0,
    )

    for _ in range(3):
        usage_service.record_success(
            user_id=user.id,
            resume_id=None,
            feature=AIFeature.RESUME_GENERATION,
            metadata=metadata,
        )

    service = create_service(
        db_session,
    )

    with pytest.raises(
        SubscriptionLimitExceeded,
    ) as exc_info:
        service.check_limit(
            user=user,
            feature=AIFeature.RESUME_GENERATION,
        )

    exception = exc_info.value

    assert exception.limit == 3
    assert exception.usage == 3


def test_check_limit_tracks_features_independently(
    db_session,
):
    user = create_user(
        db_session,
        subscription_plan=SubscriptionPlan.FREE,
        verified=True,
    )

    service = create_service(
        db_session,
    )

    resume_status = service.check_limit(
        user=user,
        feature=AIFeature.RESUME_GENERATION,
    )

    ats_status = service.check_limit(
        user=user,
        feature=AIFeature.ATS_OPTIMIZATION,
    )

    assert resume_status.usage == 0
    assert resume_status.remaining == 3

    assert ats_status.usage == 0
    assert ats_status.remaining == 1


def test_list_plan_limits_returns_only_requested_plan_limits(
    db_session,
):

    service = create_service(
        db_session,
    )

    result = service.list_plan_limits(
        subscription_plan=SubscriptionPlan.FREE,
    )

    assert result.subscription_plan == SubscriptionPlan.FREE
    assert len(result.limits) == 4
    assert result.limits[0].limit_value == 3
    assert result.limits[0].subscription_plan == SubscriptionPlan.FREE
