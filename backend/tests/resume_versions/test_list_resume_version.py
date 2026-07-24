from app.common.constants import ResumeVersionSource
from app.resume_versions.repository import ResumeVersionRepository
from app.resume_versions.service import ResumeVersionService
from tests.factories.resume_factory import create_resume
from tests.factories.resume_version_factory import create_resume_version
from tests.factories.user_factory import create_user


def test_get_version_history_returns_versions_in_descending_order(
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
        source=ResumeVersionSource.USER.value,
    )

    create_resume_version(
        db_session,
        resume_id=resume.id,
        version_number=2,
        snapshot={"title": "Version 2"},
        source=ResumeVersionSource.USER.value,
    )

    create_resume_version(
        db_session,
        resume_id=resume.id,
        version_number=3,
        snapshot={"title": "Version 3"},
        source=ResumeVersionSource.AI.value,
    )

    repository = ResumeVersionRepository(db_session)
    service = ResumeVersionService(repository)

    history = service.get_version_history(
        resume_id=resume.id,
    )

    assert len(history) == 3
    assert [version.version_number for version in history] == [
        3,
        2,
        1,
    ]


def test_get_version_history_returns_empty_list_for_resume_without_versions(
    db_session,
):
    user = create_user(db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    repository = ResumeVersionRepository(db_session)
    service = ResumeVersionService(repository)

    history = service.get_version_history(
        resume_id=resume.id,
    )

    assert history == []


def test_get_version_history_only_returns_versions_for_requested_resume(
    db_session,
):
    user = create_user(db_session)

    first_resume = create_resume(
        db_session,
        user_id=user.id,
        title="First Resume",
    )

    second_resume = create_resume(
        db_session,
        user_id=user.id,
        title="Second Resume",
    )

    create_resume_version(
        db_session,
        resume_id=first_resume.id,
        version_number=1,
        snapshot={"title": "First Resume Version 1"},
    )

    create_resume_version(
        db_session,
        resume_id=second_resume.id,
        version_number=1,
        snapshot={"title": "Second Resume Version 1"},
    )

    repository = ResumeVersionRepository(db_session)
    service = ResumeVersionService(repository)

    history = service.get_version_history(
        resume_id=first_resume.id,
    )

    assert len(history) == 1
    assert history[0].resume_id == first_resume.id
    assert history[0].snapshot == {
        "title": "First Resume Version 1",
    }
