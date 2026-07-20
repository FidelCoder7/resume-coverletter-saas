from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.ai.contracts import (
    AIExecutionMetadata,
    AIExecutionResult,
)
from app.ai.exceptions import AIProviderError
from app.ats.ai_service import ATSAIService
from app.common.constants import (
    AIFeature,
)


def build_metadata() -> AIExecutionMetadata:
    return AIExecutionMetadata(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        prompt_tokens=120,
        completion_tokens=180,
        total_tokens=300,
        latency_ms=650,
        estimated_cost=0.00018,
    )


def test_successful_ats_optimization_records_ai_usage():
    ai_service = MagicMock()

    ai_service.generate_ats_optimization.return_value = AIExecutionResult(
        content="Optimized ATS resume",
        metadata=build_metadata(),
    )

    usage_service = MagicMock()

    service = ATSAIService(
        ai_service=ai_service,
        ai_usage_service=usage_service,
    )

    user_id = uuid4()
    resume_id = uuid4()

    service.optimize(
        user_id=user_id,
        resume_id=resume_id,
        resume_content="Original resume",
        job_description="Python FastAPI Docker",
        target_job_title="Backend Engineer",
    )

    usage_service.record_success.assert_called_once()

    kwargs = usage_service.record_success.call_args.kwargs

    assert kwargs["user_id"] == user_id
    assert kwargs["resume_id"] == resume_id

    assert kwargs["feature"] == AIFeature.ATS_OPTIMIZATION

    metadata = kwargs["metadata"]

    assert metadata.provider == "openai"
    assert metadata.model == "gpt-5"
    assert metadata.prompt_tokens == 120
    assert metadata.completion_tokens == 180
    assert metadata.total_tokens == 300
    assert metadata.latency_ms == 650



def test_failed_ats_optimization_does_not_record_success():
    ai_service = MagicMock()

    ai_service.generate_ats_optimization.side_effect = AIProviderError(
        "provider failed"
    )

    usage_service = MagicMock()

    service = ATSAIService(
        ai_service=ai_service,
        ai_usage_service=usage_service,
    )

    with pytest.raises(AIProviderError):
        service.optimize(
            user_id=uuid4(),
            resume_id=uuid4(),
            resume_content="resume",
            job_description="Python",
            target_job_title=None,
        )

    usage_service.record_success.assert_not_called()
