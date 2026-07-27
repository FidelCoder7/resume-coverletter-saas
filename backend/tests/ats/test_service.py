from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.ats.ai_service import ATSAIService
from app.ats.service import ATSService
from app.common.constants import AIFeature
from app.resume_versions.service import ResumeVersionService
from app.resumes.repository import ResumeRepository
from app.subscriptions.exceptions import SubscriptionLimitExceeded
from app.subscriptions.service import SubscriptionService


@pytest.fixture
def repository():
    return MagicMock(spec=ResumeRepository)


@pytest.fixture
def ai_service():
    return MagicMock(spec=ATSAIService)


@pytest.fixture
def resume_version_service():
    return MagicMock(spec=ResumeVersionService)


@pytest.fixture
def subscription_service():
    return MagicMock(spec=SubscriptionService)


@pytest.fixture
def ats_service(
    repository,
    ai_service,
    resume_version_service,
    subscription_service,
):
    return ATSService(
        repository=repository,
        ai_service=ai_service,
        resume_version_service=resume_version_service,
        subscription_service=subscription_service,
    )


def test_ats_optimization_checks_subscription_limit_before_ai_execution(
    ats_service,
    repository,
    ai_service,
    subscription_service,
):
    user = MagicMock()
    user.id = uuid4()

    resume = MagicMock()
    resume.id = uuid4()
    resume.user_id = user.id

    repository.get_for_generation.return_value = resume

    subscription_service.check_limit.side_effect = SubscriptionLimitExceeded(
        subscription_plan="free",
        feature=AIFeature.ATS_OPTIMIZATION.value,
        limit=5,
        usage=5,
        period="monthly",
    )

    with pytest.raises(
        SubscriptionLimitExceeded,
    ):
        ats_service.optimize_resume(
            user=user,
            resume_id=resume.id,
            job_description="Python FastAPI Docker",
            target_job_title="Backend Engineer",
        )

    subscription_service.check_limit.assert_called_once_with(
        user=user,
        feature=AIFeature.ATS_OPTIMIZATION,
    )

    ai_service.optimize.assert_not_called()
