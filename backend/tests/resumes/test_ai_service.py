from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.ai.contracts import (
    AIExecutionMetadata,
    AIExecutionResult,
)
from app.ai.service import AIService
from app.ai_usage.service import AIUsageService
from app.common.constants import AIFeature
from app.resume_versions.service import ResumeVersionService
from app.resumes.ai_service import ResumeAIService
from app.subscriptions.exceptions import SubscriptionLimitExceeded
from app.subscriptions.service import SubscriptionService


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def ai_service():
    return MagicMock(spec=AIService)


@pytest.fixture
def ai_usage_service():
    return MagicMock(spec=AIUsageService)


@pytest.fixture
def resume_version_service():
    return MagicMock(spec=ResumeVersionService)


@pytest.fixture
def subscription_service():
    return MagicMock(spec=SubscriptionService)


@pytest.fixture
def resume_ai_service(
    repository,
    ai_service,
    ai_usage_service,
    resume_version_service,
    subscription_service,
):
    return ResumeAIService(
        repository=repository,
        ai_service=ai_service,
        ai_usage_service=ai_usage_service,
        resume_version_service=resume_version_service,
        subscription_service=subscription_service,
    )


def test_generate_resume_checks_subscription_limit_before_ai_execution(
    resume_ai_service,
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
        feature=AIFeature.RESUME_GENERATION.value,
        limit=5,
        usage=5,
        period="monthly",
    )

    with pytest.raises(
        SubscriptionLimitExceeded,
    ):
        resume_ai_service.generate_resume(
            user=user,
            resume_id=resume.id,
            target_job_title="Backend Engineer",
            job_description="Python FastAPI",
        )

    subscription_service.check_limit.assert_called_once_with(
        user=user,
        feature=AIFeature.RESUME_GENERATION,
    )

    ai_service.generate_resume.assert_not_called()


def test_generate_resume_executes_ai_when_subscription_limit_allows_request(
    resume_ai_service,
    repository,
    ai_service,
    ai_usage_service,
    resume_version_service,
    subscription_service,
):
    user = MagicMock()
    user.id = uuid4()

    resume = MagicMock()
    resume.id = uuid4()
    resume.user_id = user.id
    resume.title = "Software Engineer Resume"
    resume.summary = "Experienced backend engineer."
    resume.skills = []
    resume.experiences = []
    resume.educations = []
    resume.projects = []
    resume.certifications = []

    repository.get_for_generation.return_value = resume
    repository.update.return_value = resume

    metadata = AIExecutionMetadata(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        prompt_tokens=100,
        completion_tokens=200,
        total_tokens=300,
        latency_ms=500,
        estimated_cost=0.001,
    )

    ai_service.generate_resume.return_value = AIExecutionResult(
        content="Generated Resume",
        metadata=metadata,
    )

    resume_ai_service.generate_resume(
        user=user,
        resume_id=resume.id,
        target_job_title="Backend Engineer",
        job_description="Python FastAPI",
    )

    subscription_service.check_limit.assert_called_once_with(
        user=user,
        feature=AIFeature.RESUME_GENERATION,
    )

    ai_service.generate_resume.assert_called_once()

    ai_usage_service.record_success.assert_called_once_with(
        user_id=user.id,
        resume_id=resume.id,
        feature=AIFeature.RESUME_GENERATION,
        metadata=metadata,
    )

    resume_version_service.create_version_from_resume.assert_called_once()
