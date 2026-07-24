from app.common.constants import ResumeVersionSource
from app.resume_versions.repository import ResumeVersionRepository
from app.resume_versions.service import ResumeVersionService
from tests.factories.resume_factory import create_resume
from tests.factories.resume_version_factory import create_resume_version
from tests.factories.user_factory import create_user


def test_get_resume_version_returns_requested_version(
    db_session,
):
    user = create_user(db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    version = create_resume_version(
        db_session,
        resume_id=resume.id,
        version_number=1,
        snapshot={
            "title": "Backend Resume",
        },
        source=ResumeVersionSource.USER.value,
    )

    repository = ResumeVersionRepository(db_session)
    service = ResumeVersionService(repository)

    result = service.get_version(
        version_id=version.id,
    )

    assert result is not None
    assert result.id == version.id
    assert result.resume_id == resume.id
    assert result.version_number == 1
    assert result.snapshot == {
        "title": "Backend Resume",
    }


def test_get_resume_version_returns_none_for_unknown_version(
    db_session,
):
    from uuid import uuid4

    repository = ResumeVersionRepository(db_session)
    service = ResumeVersionService(repository)

    result = service.get_version(
        version_id=uuid4(),
    )

    assert result is None
