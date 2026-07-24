from app.resume_versions.repository import ResumeVersionRepository
from app.resume_versions.service import ResumeVersionService
from tests.factories.resume_factory import create_resume
from tests.factories.resume_version_factory import create_resume_version
from tests.factories.user_factory import create_user


def test_get_latest_version_returns_highest_version_number(
    db_session,
):
    user = create_user(db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    create_resume_version(
        db_session,
        resume_id=resume.id,
        version_number=1,
        snapshot={"title": "Version 1"},
    )

    create_resume_version(
        db_session,
        resume_id=resume.id,
        version_number=2,
        snapshot={"title": "Version 2"},
    )

    create_resume_version(
        db_session,
        resume_id=resume.id,
        version_number=3,
        snapshot={"title": "Version 3"},
    )

    repository = ResumeVersionRepository(db_session)
    service = ResumeVersionService(repository)

    latest = service.get_latest_version(
        resume_id=resume.id,
    )

    assert latest is not None
    assert latest.version_number == 3
    assert latest.snapshot == {
        "title": "Version 3",
    }


def test_get_latest_version_returns_none_when_no_versions_exist(
    db_session,
):
    user = create_user(db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    repository = ResumeVersionRepository(db_session)
    service = ResumeVersionService(repository)

    latest = service.get_latest_version(
        resume_id=resume.id,
    )

    assert latest is None
