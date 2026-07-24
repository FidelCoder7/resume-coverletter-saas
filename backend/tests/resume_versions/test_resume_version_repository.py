import pytest

from app.common.constants import ResumeVersionSource
from app.resume_versions.exceptions import DuplicateResumeVersion
from app.resume_versions.repository import ResumeVersionRepository
from tests.factories.resume_factory import create_resume
from tests.factories.resume_version_factory import create_resume_version
from tests.factories.user_factory import create_user


def test_repository_get_next_version_number_returns_one_for_new_resume(
    db_session,
):
    user = create_user(db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    repository = ResumeVersionRepository(db_session)

    next_version = repository.get_next_version_number(
        resume_id=resume.id,
    )

    assert next_version == 1


def test_repository_get_next_version_number_returns_next_number(
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
    )

    create_resume_version(
        db_session,
        resume_id=resume.id,
        version_number=2,
    )

    repository = ResumeVersionRepository(db_session)

    next_version = repository.get_next_version_number(
        resume_id=resume.id,
    )

    assert next_version == 3


def test_repository_get_by_resume_and_number_returns_matching_version(
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
        version_number=2,
    )

    repository = ResumeVersionRepository(db_session)

    result = repository.get_by_resume_and_number(
        resume_id=resume.id,
        version_number=2,
    )

    assert result is not None
    assert result.id == version.id


def test_repository_get_by_resume_and_number_returns_none_when_not_found(
    db_session,
):
    user = create_user(db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    repository = ResumeVersionRepository(db_session)

    result = repository.get_by_resume_and_number(
        resume_id=resume.id,
        version_number=999,
    )

    assert result is None


def test_repository_rejects_duplicate_version_number(
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
    )

    repository = ResumeVersionRepository(db_session)

    with pytest.raises(DuplicateResumeVersion):
        repository.create(
            resume_id=resume.id,
            version_number=1,
            snapshot={
                "title": "Duplicate Version",
            },
            source=ResumeVersionSource.USER.value,
        )


def test_same_version_number_is_allowed_for_different_resumes(
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

    repository = ResumeVersionRepository(db_session)

    first_version = repository.create(
        resume_id=first_resume.id,
        version_number=1,
        snapshot={"title": "First Resume"},
        source=ResumeVersionSource.USER.value,
    )

    second_version = repository.create(
        resume_id=second_resume.id,
        version_number=1,
        snapshot={"title": "Second Resume"},
        source=ResumeVersionSource.USER.value,
    )

    assert first_version.version_number == 1
    assert second_version.version_number == 1
    assert first_version.resume_id != second_version.resume_id
