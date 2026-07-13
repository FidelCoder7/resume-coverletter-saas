import pytest

from app.ai.providers import AIProvider
from app.ai.schemas import (
    CoverLetterGenerationRequest,
    CoverLetterGenerationResponse,
)
from app.ai.service import AIService
from app.cover_letters.exceptions import (
    CoverLetterAccessDenied,
    CoverLetterNotFound,
)
from app.cover_letters.repository import CoverLetterRepository
from app.cover_letters.service import CoverLetterService
from app.resumes.repository import ResumeRepository
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import create_user


class FakeAIProvider(AIProvider):
    def generate_cover_letter(
        self,
        request: CoverLetterGenerationRequest,
    ) -> CoverLetterGenerationResponse:
        return CoverLetterGenerationResponse(
            content="Regenerated cover letter.",
        )


DEFAULT_CONTENT = (
    "I am excited to apply for this opportunity because my "
    "experience building production-ready backend systems "
    "aligns well with your requirements."
)


def build_service(db_session):
    return CoverLetterService(
        repository=CoverLetterRepository(db_session),
        resume_repository=ResumeRepository(db_session),
        ai_service=AIService(
            provider=FakeAIProvider(),
        ),
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
        job_description=("Looking for an experienced FastAPI backend engineer."),
    )

    assert regenerated.id == cover_letter.id

    assert regenerated.content == ("Regenerated cover letter.")


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
        job_description=("Backend engineer position."),
    )

    assert regenerated.title == cover_letter.title
    assert regenerated.company_name == cover_letter.company_name
    assert regenerated.job_title == cover_letter.job_title
    assert regenerated.resume_id == cover_letter.resume_id


def test_regenerate_unknown_cover_letter(
    db_session,
):
    from uuid import uuid4

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
        job_description=("Backend engineer"),
    )

    assert regenerated.content != original

    assert regenerated.content == ("Regenerated cover letter.")


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

    assert loaded.content == ("Regenerated cover letter.")
