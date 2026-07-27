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
from app.cover_letters.ai_service import CoverLetterAIService
from app.cover_letters.models import CoverLetter
from app.cover_letters.repository import CoverLetterRepository
from app.resumes.repository import ResumeRepository
from app.subscriptions.exceptions import SubscriptionLimitExceeded
from app.subscriptions.service import SubscriptionService


@pytest.fixture
def repository():
    return MagicMock(spec=CoverLetterRepository)


@pytest.fixture
def resume_repository():
    return MagicMock(spec=ResumeRepository)


@pytest.fixture
def ai_service():
    return MagicMock(spec=AIService)


@pytest.fixture
def ai_usage_service():
    return MagicMock(spec=AIUsageService)


@pytest.fixture
def subscription_service():
    return MagicMock(spec=SubscriptionService)


@pytest.fixture
def cover_letter_ai_service(
    repository,
    resume_repository,
    ai_service,
    ai_usage_service,
    subscription_service,
):
    return CoverLetterAIService(
        repository=repository,
        resume_repository=resume_repository,
        ai_service=ai_service,
        ai_usage_service=ai_usage_service,
        subscription_service=subscription_service,
    )


def test_generate_cover_letter_checks_generation_limit_before_ai_execution(
    cover_letter_ai_service,
    resume_repository,
    ai_service,
    subscription_service,
):
    user = MagicMock()
    user.id = uuid4()

    resume = MagicMock()
    resume.id = uuid4()
    resume.user_id = user.id

    resume_repository.get_for_generation.return_value = resume

    subscription_service.check_limit.side_effect = SubscriptionLimitExceeded(
        subscription_plan="free",
        feature=AIFeature.COVER_LETTER_GENERATION.value,
        limit=5,
        usage=5,
        period="monthly",
    )

    with pytest.raises(
        SubscriptionLimitExceeded,
    ):
        cover_letter_ai_service.generate_cover_letter(
            user=user,
            resume_id=resume.id,
            title="Application",
            company_name="Example Corp",
            job_title="Backend Engineer",
            job_description="Python FastAPI",
        )

    subscription_service.check_limit.assert_called_once_with(
        user=user,
        feature=AIFeature.COVER_LETTER_GENERATION,
    )

    ai_service.generate_cover_letter.assert_not_called()


def test_regenerate_cover_letter_checks_regeneration_limit_before_ai_execution(
    cover_letter_ai_service,
    repository,
    resume_repository,
    ai_service,
    subscription_service,
):
    user = MagicMock()
    user.id = uuid4()

    resume = MagicMock()
    resume.id = uuid4()
    resume.user_id = user.id

    cover_letter = MagicMock(spec=CoverLetter)
    cover_letter.id = uuid4()
    cover_letter.resume_id = resume.id
    cover_letter.company_name = "Example Corp"
    cover_letter.job_title = "Backend Engineer"

    repository.get_by_id.return_value = cover_letter
    resume_repository.get_for_generation.return_value = resume

    subscription_service.check_limit.side_effect = SubscriptionLimitExceeded(
        subscription_plan="free",
        feature=AIFeature.COVER_LETTER_REGENERATION.value,
        limit=5,
        usage=5,
        period="monthly",
    )

    with pytest.raises(
        SubscriptionLimitExceeded,
    ):
        cover_letter_ai_service.regenerate_cover_letter(
            user=user,
            cover_letter_id=cover_letter.id,
            job_description="Python FastAPI",
        )

    subscription_service.check_limit.assert_called_once_with(
        user=user,
        feature=AIFeature.COVER_LETTER_REGENERATION,
    )

    ai_service.generate_cover_letter.assert_not_called()


def test_generate_cover_letter_executes_ai_when_limit_allows_request(
    cover_letter_ai_service,
    repository,
    resume_repository,
    ai_service,
    ai_usage_service,
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

    resume_repository.get_for_generation.return_value = resume

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

    ai_service.generate_cover_letter.return_value = AIExecutionResult(
        content="Generated Cover Letter",
        metadata=metadata,
    )

    cover_letter = MagicMock()
    cover_letter.id = uuid4()

    repository.create.return_value = cover_letter

    cover_letter_ai_service.generate_cover_letter(
        user=user,
        resume_id=resume.id,
        title="Application",
        company_name="Example Corp",
        job_title="Backend Engineer",
        job_description="Python FastAPI",
    )

    subscription_service.check_limit.assert_called_once_with(
        user=user,
        feature=AIFeature.COVER_LETTER_GENERATION,
    )

    ai_service.generate_cover_letter.assert_called_once()

    ai_usage_service.record_success.assert_called_once_with(
        user_id=user.id,
        resume_id=resume.id,
        cover_letter_id=cover_letter.id,
        feature=AIFeature.COVER_LETTER_GENERATION,
        metadata=metadata,
    )
