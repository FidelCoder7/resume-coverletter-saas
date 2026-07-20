from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.ai.contracts import (
    AIExecutionMetadata,
    AIExecutionResult,
)
from app.ai.service import AIService
from app.ai_usage.service import AIUsageService
from app.ats.ai_service import ATSAIService
from app.common.constants import AIFeature


@pytest.fixture
def ai_service():
    return MagicMock(spec=AIService)


@pytest.fixture
def ai_usage_service():
    return MagicMock(spec=AIUsageService)


@pytest.fixture
def ats_ai_service(
    ai_service,
    ai_usage_service,
):
    return ATSAIService(
        ai_service=ai_service,
        ai_usage_service=ai_usage_service,
    )


def test_optimize_success(
    monkeypatch,
    ats_ai_service,
    ai_service,
    ai_usage_service,
):
    user_id = uuid4()
    resume_id = uuid4()

    metadata = AIExecutionMetadata(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        prompt_tokens=100,
        completion_tokens=150,
        total_tokens=250,
        latency_ms=1200,
        estimated_cost=0.00015,
    )

    ai_service.generate_ats_optimization.return_value = AIExecutionResult(
        content="Optimized Resume",
        metadata=metadata,
    )

    score_mock = MagicMock(
        return_value=(
            88,
            ["python", "fastapi"],
            ["docker"],
        )
    )

    monkeypatch.setattr(
        "app.ats.ai_service.ATSScoringService.score",
        score_mock,
    )

    result = ats_ai_service.optimize(
        user_id=user_id,
        resume_id=resume_id,
        resume_content="Original Resume",
        job_description="Python FastAPI Docker",
        target_job_title="Backend Engineer",
    )

    ai_service.generate_ats_optimization.assert_called_once()

    score_mock.assert_called_once()

    ai_usage_service.record_success.assert_called_once_with(
        user_id=user_id,
        resume_id=resume_id,
        feature=AIFeature.ATS_OPTIMIZATION,
        metadata=metadata,
    )

    assert result.optimized_resume == "Optimized Resume"

    assert result.ats_score == 88

    assert result.matched_keywords == [
        "python",
        "fastapi",
    ]

    assert result.missing_keywords == [
        "docker",
    ]

    assert result.recommendations == []


def test_optimize_propagates_generation_error(
    ats_ai_service,
    ai_service,
    ai_usage_service,
):
    ai_service.generate_ats_optimization.side_effect = Exception(
        "OpenAI failure",
    )

    with pytest.raises(
        Exception,
        match="OpenAI failure",
    ):
        ats_ai_service.optimize(
            user_id=uuid4(),
            resume_id=uuid4(),
            resume_content="Resume",
            job_description="Job",
            target_job_title=None,
        )

    ai_usage_service.record_success.assert_not_called()


def test_optimize_returns_score_values(
    monkeypatch,
    ats_ai_service,
    ai_service,
):
    metadata = AIExecutionMetadata(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30,
        latency_ms=100,
        estimated_cost=0.00001,
    )

    ai_service.generate_ats_optimization.return_value = AIExecutionResult(
        content="Optimized Resume",
        metadata=metadata,
    )

    monkeypatch.setattr(
        "app.ats.ai_service.ATSScoringService.score",
        MagicMock(
            return_value=(
                95,
                [
                    "python",
                    "sqlalchemy",
                ],
                [
                    "aws",
                    "docker",
                ],
            )
        ),
    )

    result = ats_ai_service.optimize(
        user_id=uuid4(),
        resume_id=uuid4(),
        resume_content="Resume",
        job_description="Job",
        target_job_title=None,
    )

    assert result.ats_score == 95

    assert result.matched_keywords == [
        "python",
        "sqlalchemy",
    ]

    assert result.missing_keywords == [
        "aws",
        "docker",
    ]


def test_optimize_passes_metadata_to_usage_service(
    monkeypatch,
    ats_ai_service,
    ai_service,
    ai_usage_service,
):
    user_id = uuid4()
    resume_id = uuid4()

    metadata = AIExecutionMetadata(
        provider="openai",
        model="gpt-5",
        prompt_version="v2",
        prompt_tokens=111,
        completion_tokens=222,
        total_tokens=333,
        latency_ms=999,
        estimated_cost=0.001,
    )

    ai_service.generate_ats_optimization.return_value = AIExecutionResult(
        content="Optimized Resume",
        metadata=metadata,
    )

    monkeypatch.setattr(
        "app.ats.ai_service.ATSScoringService.score",
        MagicMock(
            return_value=(
                100,
                [],
                [],
            )
        ),
    )

    ats_ai_service.optimize(
        user_id=user_id,
        resume_id=resume_id,
        resume_content="Resume",
        job_description="Job",
        target_job_title=None,
    )

    ai_usage_service.record_success.assert_called_once_with(
        user_id=user_id,
        resume_id=resume_id,
        feature=AIFeature.ATS_OPTIMIZATION,
        metadata=metadata,
    )
