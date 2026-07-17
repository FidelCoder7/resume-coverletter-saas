from datetime import datetime
from uuid import uuid4

import pytest

from app.ai.service import AIService
from app.ai_usage.models import AIUsage
from app.ai_usage.repository import AIUsageRepository
from app.resumes.exceptions import (
    ResumeAccessDenied,
    ResumeNotFound,
)
from app.resumes.repository import ResumeRepository
from app.resumes.service import ResumeAIService
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import create_user
from tests.fakes.fake_ai_provider import FakeAIProvider


@pytest.fixture()
def service(db_session):
    repository = ResumeRepository(db_session)
    ai_usage_repository = AIUsageRepository(db_session)

    ai_service = AIService(
        provider=FakeAIProvider(),
    )

    return ResumeAIService(
        repository=repository,
        ai_service=ai_service,
        ai_usage_repository=ai_usage_repository,
    )


def test_generate_resume(service, db_session):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    updated = service.generate_resume(
        user_id=user.id,
        resume_id=resume.id,
        target_job_title="Backend Engineer",
        job_description="FastAPI backend role.",
    )

    assert updated.generated_content is not None
    assert "FastAPI" in updated.generated_content
    assert updated.generated_at is not None


def test_generate_resume_unknown_resume(
    service,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    with pytest.raises(ResumeNotFound):
        service.generate_resume(
            user_id=user.id,
            resume_id=uuid4(),
            target_job_title="Backend Engineer",
            job_description="FastAPI backend role.",
        )


def test_generate_resume_forbidden(
    service,
    db_session,
):
    owner = create_user(
        db_session,
        verified=True,
    )

    other_user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=owner.id,
    )

    with pytest.raises(ResumeAccessDenied):
        service.generate_resume(
            user_id=other_user.id,
            resume_id=resume.id,
            target_job_title="Backend Engineer",
            job_description="FastAPI backend role.",
        )


def test_generated_resume_is_persisted(
    service,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    updated = service.generate_resume(
        user_id=user.id,
        resume_id=resume.id,
        target_job_title="Backend Engineer",
        job_description="FastAPI backend role.",
    )

    repository = ResumeRepository(db_session)

    stored = repository.get_by_id(
        updated.id,
    )

    assert stored is not None
    assert stored.generated_content == updated.generated_content
    assert stored.generated_at is not None


def test_generated_resume_sets_timestamp(
    service,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    updated = service.generate_resume(
        user_id=user.id,
        resume_id=resume.id,
        target_job_title="Backend Engineer",
        job_description="FastAPI backend role.",
    )

    assert isinstance(
        updated.generated_at,
        datetime,
    )


def test_generate_resume_records_ai_usage(
    service,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    service.generate_resume(
        user_id=user.id,
        resume_id=resume.id,
        target_job_title="Backend Engineer",
        job_description="FastAPI backend role.",
    )

    usage = db_session.query(AIUsage).one()

    assert usage.user_id == user.id
    assert usage.resume_id == resume.id
    assert usage.cover_letter_id is None

    assert usage.provider == "fake"
    assert usage.model == "fake-model"

    assert usage.prompt_tokens == 120
    assert usage.completion_tokens == 180
    assert usage.total_tokens == 300

    assert usage.status.value == "success"


def test_regenerate_resume_overwrites_previous_content(
    service,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
        generated_content="Old Resume",
    )

    updated = service.generate_resume(
        user_id=user.id,
        resume_id=resume.id,
        target_job_title="Senior Backend Engineer",
        job_description="Senior FastAPI role.",
    )

    assert updated.generated_content != "Old Resume"
