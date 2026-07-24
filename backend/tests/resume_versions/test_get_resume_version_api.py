from uuid import uuid4

from tests.factories.resume_factory import create_resume
from tests.factories.resume_version_factory import create_resume_version


def test_get_resume_version(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    version = create_resume_version(
        db_session,
        resume_id=resume.id,
        version_number=1,
        snapshot={
            "title": "Backend Engineer",
            "summary": "Python developer",
            "skills": [
                "Python",
                "FastAPI",
            ],
        },
        source="user",
        change_summary="Initial resume snapshot",
    )

    response = client.get(
        f"/api/resumes/{resume.id}/versions/{version.id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(version.id)
    assert data["resume_id"] == str(resume.id)
    assert data["version_number"] == 1
    assert data["source"] == "user"
    assert data["change_summary"] == "Initial resume snapshot"

    assert data["snapshot"] == {
        "title": "Backend Engineer",
        "summary": "Python developer",
        "skills": [
            "Python",
            "FastAPI",
        ],
    }

    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_get_missing_resume_version_returns_404(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    response = client.get(
        f"/api/resumes/{resume.id}/versions/{uuid4()}",
    )

    assert response.status_code == 404

    assert response.json()["detail"] == ("Resume version not found.")


def test_list_versions_for_missing_resume_returns_404(
    authenticated_client,
):
    client, _ = authenticated_client

    response = client.get(
        f"/api/resumes/{uuid4()}/versions",
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "Resume not found."
