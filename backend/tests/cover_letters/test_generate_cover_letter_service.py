from uuid import uuid4

import pytest

from app.ai.service import AIService
from app.ai_usage.models import AIUsage
from app.ai_usage.repository import AIUsageRepository
from app.ai_usage.service import AIUsageService
from app.cover_letters.ai_service import CoverLetterAIService
from app.cover_letters.exceptions import (
    CoverLetterAccessDenied,
    CoverLetterNotFound,
    DuplicateCoverLetter,
)
from app.cover_letters.repository import CoverLetterRepository
from app.resumes.repository import ResumeRepository
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import create_user
from tests.fakes.fake_ai_provider import GENERATED_COVER_LETTER, FakeAIProvider


@pytest.fixture()
def service(db_session):
    repository = CoverLetterRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    ai_usage_service = AIUsageService(
        AIUsageRepository(db_session),
    )

    ai_service = AIService(
        provider=FakeAIProvider(),
    )

    return CoverLetterAIService(
        repository=repository,
        resume_repository=resume_repository,
        ai_service=ai_service,
        ai_usage_service=ai_usage_service,
    )


def test_generate_cover_letter(service, db_session):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    cover_letter = service.generate_cover_letter(
        user_id=user.id,
        resume_id=resume.id,
        title="Backend Engineer",
        company_name="OpenAI",
        job_title="Backend Engineer",
        job_description=("We are looking for an experienced FastAPI backend engineer."),
    )

    assert cover_letter.resume_id == resume.id
    assert cover_letter.title == "Backend Engineer"
    assert cover_letter.company_name == "OpenAI"
    assert cover_letter.job_title == "Backend Engineer"
    assert cover_letter.content == GENERATED_COVER_LETTER


def test_generate_cover_letter_unknown_resume(service, db_session):
    user = create_user(
        db_session,
        verified=True,
    )

    with pytest.raises(CoverLetterNotFound):
        service.generate_cover_letter(
            user_id=user.id,
            resume_id=uuid4(),
            title="Backend Engineer",
            company_name="OpenAI",
            job_title="Backend Engineer",
            job_description="Backend role.",
        )


def test_generate_cover_letter_forbidden(service, db_session):
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

    with pytest.raises(CoverLetterAccessDenied):
        service.generate_cover_letter(
            user_id=other_user.id,
            resume_id=resume.id,
            title="Backend Engineer",
            company_name="OpenAI",
            job_title="Backend Engineer",
            job_description="Backend role.",
        )


def test_generate_cover_letter_duplicate_title(service, db_session):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    service.generate_cover_letter(
        user_id=user.id,
        resume_id=resume.id,
        title="Backend Engineer",
        company_name="OpenAI",
        job_title="Backend Engineer",
        job_description="Backend role.",
    )

    with pytest.raises(DuplicateCoverLetter):
        service.generate_cover_letter(
            user_id=user.id,
            resume_id=resume.id,
            title="Backend Engineer",
            company_name="OpenAI",
            job_title="Backend Engineer",
            job_description="Backend role.",
        )


def test_generated_cover_letter_is_persisted(service, db_session):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    generated = service.generate_cover_letter(
        user_id=user.id,
        resume_id=resume.id,
        title="Backend Engineer",
        company_name="OpenAI",
        job_title="Backend Engineer",
        job_description="Backend role.",
    )

    repository = CoverLetterRepository(db_session)

    stored = repository.get_by_id(
        generated.id,
    )

    assert stored is not None
    assert stored.id == generated.id
    assert stored.content == generated.content


def test_generate_cover_letter_records_ai_usage(
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

    cover_letter = service.generate_cover_letter(
        user_id=user.id,
        resume_id=resume.id,
        title="Backend Engineer",
        company_name="OpenAI",
        job_title="Backend Engineer",
        job_description="Backend role.",
    )

    usage = db_session.query(AIUsage).one()

    assert usage.user_id == user.id
    assert usage.resume_id == resume.id
    assert usage.cover_letter_id == cover_letter.id

    assert usage.provider == "fake"
    assert usage.model == "fake-model"

    assert usage.prompt_tokens == 120
    assert usage.completion_tokens == 240
    assert usage.total_tokens == 360

    assert usage.status.value == "success"
