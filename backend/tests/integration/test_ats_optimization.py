from unittest.mock import MagicMock

from app.ai.contracts import (
    AIExecutionMetadata,
    AIExecutionResult,
)
from app.ai.service import AIService
from app.ai_usage.repository import AIUsageRepository
from app.ai_usage.service import AIUsageService
from app.ats.ai_service import ATSAIService
from app.ats.service import ATSService
from app.common.constants import (
    AIFeature,
    AIRequestStatus,
)
from app.resumes.repository import ResumeRepository
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import create_user


def test_ats_optimization_creates_ai_usage_record(
    db_session,
):
    user = create_user(db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
        title="Backend Resume",
        summary="Python FastAPI SQLAlchemy",
    )

    metadata = AIExecutionMetadata(
        provider="openai",
        model="gpt-5",
        prompt_version="v1",
        prompt_tokens=120,
        completion_tokens=180,
        total_tokens=300,
        latency_ms=1500,
        estimated_cost=0.00018,
    )

    ai_service = MagicMock(spec=AIService)

    ai_service.generate_ats_optimization.return_value = AIExecutionResult(
        content="Optimized Python FastAPI SQLAlchemy Docker Kubernetes Resume",
        metadata=metadata,
    )

    ats_service = ATSService(
        repository=ResumeRepository(db_session),
        ai_service=ATSAIService(
            ai_service=ai_service,
            ai_usage_service=AIUsageService(
                AIUsageRepository(db_session),
            ),
        ),
    )

    response = ats_service.optimize_resume(
        user_id=user.id,
        resume_id=resume.id,
        job_description="Python FastAPI Docker Kubernetes PostgreSQL",
        target_job_title="Backend Engineer",
    )

    usage = AIUsageRepository(db_session).list_by_resume(
        resume.id,
    )

    assert len(usage) == 1

    record = usage[0]

    assert record.user_id == user.id
    assert record.resume_id == resume.id
    assert record.feature == AIFeature.ATS_OPTIMIZATION
    assert record.status == AIRequestStatus.SUCCESS
    assert record.provider == "openai"
    assert record.model == "gpt-5"

    assert response.resume_id == resume.id
    assert response.optimized_resume.startswith("Optimized")
