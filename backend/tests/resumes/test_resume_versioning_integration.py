from app.common.constants import ResumeVersionSource
from app.resume_versions.repository import ResumeVersionRepository
from tests.factories.resume_factory import create_resume
from tests.utils import auth_headers, authenticated_user


def test_resume_version_history_tracks_manual_and_ai_changes(
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
        title="Initial Resume",
        summary="Initial summary",
    )

    headers = auth_headers(token)

    update_response = client.put(
        f"/api/resumes/{resume.id}",
        json={
            "title": "Updated Resume",
            "summary": "Updated summary",
        },
        headers=headers,
    )

    assert update_response.status_code == 200

    generate_response = client.post(
        f"/api/resumes/{resume.id}/generate",
        json={
            "target_job_title": "Backend Engineer",
            "job_description": "Python FastAPI backend engineer.",
        },
        headers=headers,
    )

    assert generate_response.status_code == 200

    repository = ResumeVersionRepository(
        db_session,
    )

    versions = repository.list_by_resume(
        resume_id=resume.id,
    )

    assert len(versions) == 2

    latest = versions[0]
    previous = versions[1]

    assert latest.version_number == 2
    assert latest.source == ResumeVersionSource.AI

    assert previous.version_number == 1
    assert previous.source == ResumeVersionSource.USER

    assert previous.snapshot["title"] == "Updated Resume"
    assert previous.snapshot["summary"] == "Updated summary"

    assert latest.snapshot["generated_content"] is not None
