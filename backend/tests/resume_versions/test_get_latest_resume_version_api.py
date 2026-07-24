from tests.factories.resume_factory import create_resume
from tests.factories.resume_version_factory import create_resume_version


def test_get_latest_resume_version(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

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
        snapshot={
            "title": "Version 2",
            "skills": ["Python", "FastAPI"],
        },
    )

    response = client.get(
        f"/api/resumes/{resume.id}/versions/latest",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["version_number"] == 2
    assert data["snapshot"] == {
        "title": "Version 2",
        "skills": ["Python", "FastAPI"],
    }


def test_get_latest_resume_version_returns_404_when_no_versions_exist(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    response = client.get(
        f"/api/resumes/{resume.id}/versions/latest",
    )

    assert response.status_code == 404

    assert response.json()["detail"] == ("No versions found for this resume.")
