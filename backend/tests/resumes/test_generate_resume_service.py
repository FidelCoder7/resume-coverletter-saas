from datetime import datetime
from uuid import uuid4

import pytest

from app.ai.service import AIService
from app.ai_usage.repository import AIUsageRepository
from app.ai_usage.service import AIUsageService
from app.common.constants import ResumeVersionSource
from app.resume_versions.repository import ResumeVersionRepository
from app.resume_versions.service import ResumeVersionService
from app.resumes.ai_service import ResumeAIService
from app.resumes.exceptions import (
    ResumeAccessDenied,
    ResumeNotFound,
)
from app.resumes.repository import ResumeRepository
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import create_user
from tests.fakes.fake_ai_provider import FakeAIProvider


@pytest.fixture()
def service(db_session):
    repository = ResumeRepository(db_session)

    ai_usage_service = AIUsageService(
        AIUsageRepository(db_session),
    )

    ai_service = AIService(
        provider=FakeAIProvider(),
    )

    resume_version_service = ResumeVersionService(
        ResumeVersionRepository(db_session),
    )

    return ResumeAIService(
        repository=repository,
        ai_service=ai_service,
        ai_usage_service=ai_usage_service,
        resume_version_service=resume_version_service,
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

    usage_service = AIUsageService(
        AIUsageRepository(db_session),
    )

    history = usage_service.list_resume_history(
        resume_id=resume.id,
    )

    assert len(history) == 1

    usage = history[0]

    assert usage.user_id == user.id
    assert usage.resume_id == resume.id
    assert usage.cover_letter_id is None

    assert usage.provider == "fake"
    assert usage.model == "fake-model"

    assert usage.prompt_tokens == 120
    assert usage.completion_tokens == 240
    assert usage.total_tokens == 360

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


def test_generate_resume_creates_ai_version(
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

    repository = ResumeVersionRepository(
        db_session,
    )

    version = repository.get_latest(
        resume_id=updated.id,
    )

    assert version is not None
    assert version.version_number == 1
    assert version.source == ResumeVersionSource.AI

    assert version.snapshot["generated_content"] == (updated.generated_content)

    assert version.snapshot["generated_at"] == (updated.generated_at.isoformat())


def test_regenerate_resume_creates_new_ai_version(
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

    first = service.generate_resume(
        user_id=user.id,
        resume_id=resume.id,
        target_job_title="Backend Engineer",
        job_description="FastAPI backend role.",
    )

    second = service.generate_resume(
        user_id=user.id,
        resume_id=resume.id,
        target_job_title="Senior Backend Engineer",
        job_description="Senior FastAPI backend role.",
    )

    repository = ResumeVersionRepository(
        db_session,
    )

    versions = repository.list_by_resume(
        resume_id=resume.id,
    )

    assert len(versions) == 2

    assert versions[0].version_number == 2
    assert versions[0].source == ResumeVersionSource.AI
    assert versions[0].snapshot["generated_content"] == second.generated_content

    assert versions[1].version_number == 1
    assert versions[1].source == ResumeVersionSource.AI
    assert versions[1].snapshot["generated_content"] == first.generated_content
