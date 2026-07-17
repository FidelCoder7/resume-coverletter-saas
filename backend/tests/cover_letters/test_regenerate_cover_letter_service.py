from uuid import uuid4

import pytest

from app.ai.service import AIService
from app.ai_usage.models import AIUsage
from app.ai_usage.repository import AIUsageRepository
from app.cover_letters.exceptions import (
    CoverLetterAccessDenied,
    CoverLetterNotFound,
)
from app.cover_letters.repository import CoverLetterRepository
from app.cover_letters.service import CoverLetterService
from app.resumes.repository import ResumeRepository
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import create_user
from tests.fakes.fake_ai_provider import GENERATED_COVER_LETTER, FakeAIProvider

DEFAULT_CONTENT = "Original cover letter."



def build_service(
    db_session,
) -> CoverLetterService:
    repository = CoverLetterRepository(
        db_session,
    )

    resume_repository = ResumeRepository(
        db_session,
    )

    ai_usage_repository = AIUsageRepository(
        db_session,
    )

    ai_service = AIService(
        provider=FakeAIProvider(),
    )

    return CoverLetterService(
        repository=repository,
        resume_repository=resume_repository,
        ai_service=ai_service,
        ai_usage_repository=ai_usage_repository,
    )


def create_cover_letter(
    service,
    *,
    user,
    resume,
):
    return service.create_cover_letter(
        user_id=user.id,
        resume_id=resume.id,
        title="Backend Engineer",
        company_name="OpenAI",
        job_title="Backend Engineer",
        content=DEFAULT_CONTENT,
    )


def test_regenerate_cover_letter_success(
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

    service = build_service(
        db_session,
    )

    cover_letter = create_cover_letter(
        service,
        user=user,
        resume=resume,
    )

    regenerated = service.regenerate_cover_letter(
        user_id=user.id,
        cover_letter_id=cover_letter.id,
        job_description="Looking for an experienced FastAPI backend engineer.",
    )

    assert regenerated.id == cover_letter.id
    assert (
        regenerated.content == GENERATED_COVER_LETTER
    )


def test_regenerate_preserves_metadata(
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

    service = build_service(
        db_session,
    )

    cover_letter = create_cover_letter(
        service,
        user=user,
        resume=resume,
    )

    regenerated = service.regenerate_cover_letter(
        user_id=user.id,
        cover_letter_id=cover_letter.id,
        job_description="Backend engineer position.",
    )

    assert regenerated.id == cover_letter.id
    assert regenerated.resume_id == cover_letter.resume_id
    assert regenerated.title == cover_letter.title
    assert regenerated.company_name == cover_letter.company_name
    assert regenerated.job_title == cover_letter.job_title


def test_regenerate_unknown_cover_letter(
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    service = build_service(
        db_session,
    )

    with pytest.raises(CoverLetterNotFound):
        service.regenerate_cover_letter(
            user_id=user.id,
            cover_letter_id=uuid4(),
            job_description="Updated job description",
        )


def test_regenerate_other_users_cover_letter(
    db_session,
):
    owner = create_user(
        db_session,
        verified=True,
    )

    attacker = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=owner.id,
    )

    service = build_service(
        db_session,
    )

    cover_letter = create_cover_letter(
        service,
        user=owner,
        resume=resume,
    )

    with pytest.raises(CoverLetterAccessDenied):
        service.regenerate_cover_letter(
            user_id=attacker.id,
            cover_letter_id=cover_letter.id,
            job_description="Updated job description",
        )


def test_regenerate_overwrites_existing_content(
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

    service = build_service(
        db_session,
    )

    cover_letter = create_cover_letter(
        service,
        user=user,
        resume=resume,
    )

    original = cover_letter.content

    regenerated = service.regenerate_cover_letter(
        user_id=user.id,
        cover_letter_id=cover_letter.id,
        job_description="Backend engineer",
    )

    assert regenerated.content != original
    assert (
        regenerated.content == GENERATED_COVER_LETTER
    )


def test_regenerate_updates_database(
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

    service = build_service(
        db_session,
    )

    cover_letter = create_cover_letter(
        service,
        user=user,
        resume=resume,
    )

    service.regenerate_cover_letter(
        user_id=user.id,
        cover_letter_id=cover_letter.id,
        job_description="Backend engineer",
    )

    loaded = service.get_cover_letter(
        user_id=user.id,
        cover_letter_id=cover_letter.id,
    )

    assert loaded.content == GENERATED_COVER_LETTER


def test_regenerate_cover_letter_records_ai_usage(
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

    service = build_service(
        db_session,
    )

    cover_letter = service.generate_cover_letter(
        user_id=user.id,
        resume_id=resume.id,
        title="Backend Engineer",
        company_name="OpenAI",
        job_title="Backend Engineer",
        job_description="Initial job description.",
    )

    service.regenerate_cover_letter(
        user_id=user.id,
        cover_letter_id=cover_letter.id,
        job_description="Updated job description.",
    )

    usages = db_session.query(AIUsage).order_by(AIUsage.created_at).all()

    assert len(usages) == 2

    latest = usages[-1]

    assert latest.user_id == user.id
    assert latest.resume_id == resume.id
    assert latest.cover_letter_id == cover_letter.id

    assert latest.provider == "fake"
    assert latest.model == "fake-model"

    assert latest.prompt_tokens == 120
    assert latest.completion_tokens == 240
    assert latest.total_tokens == 360

    assert latest.status.value == "success"
