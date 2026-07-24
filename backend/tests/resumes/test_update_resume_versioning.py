from app.common.constants import ResumeVersionSource
from app.resume_versions.repository import ResumeVersionRepository
from tests.factories.resume_factory import create_resume
from tests.utils import auth_headers, authenticated_user


def test_update_resume_creates_user_version(
    client,
    db_session,
):
    user, token = authenticated_user(
        client,
        db_session,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
        title="Old Resume",
        summary="Old summary",
    )

    response = client.put(
        f"/api/resumes/{resume.id}",
        json={
            "title": "Updated Resume",
            "summary": "Updated summary",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    repository = ResumeVersionRepository(
        db_session,
    )

    version = repository.get_latest(
        resume_id=resume.id,
    )

    assert version is not None
    assert version.version_number == 1
    assert version.source == ResumeVersionSource.USER

    assert version.snapshot["title"] == "Updated Resume"
    assert version.snapshot["summary"] == "Updated summary"


def test_multiple_resume_updates_increment_version_number(
    client,
    db_session,
):
    user, token = authenticated_user(
        client,
        db_session,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    headers = auth_headers(token)

    first_update = client.put(
        f"/api/resumes/{resume.id}",
        json={
            "title": "First Update",
            "summary": "First update",
        },
        headers=headers,
    )

    assert first_update.status_code == 200

    second_update = client.put(
        f"/api/resumes/{resume.id}",
        json={
            "title": "Second Update",
            "summary": "Second update",
        },
        headers=headers,
    )

    assert second_update.status_code == 200

    repository = ResumeVersionRepository(
        db_session,
    )

    versions = repository.list_by_resume(
        resume_id=resume.id,
    )

    assert len(versions) == 2

    assert versions[0].version_number == 2
    assert versions[0].source == ResumeVersionSource.USER
    assert versions[0].snapshot["title"] == "Second Update"

    assert versions[1].version_number == 1
    assert versions[1].source == ResumeVersionSource.USER
    assert versions[1].snapshot["title"] == "First Update"
