from tests.factories.resume_factory import create_resume
from tests.factories.resume_version_factory import create_resume_version
from tests.factories.user_factory import create_user


def test_user_cannot_list_another_users_resume_versions(
    authenticated_client,
    db_session,
):
    client, current_user = authenticated_client

    other_user = create_user(db_session)

    other_resume = create_resume(
        db_session,
        user_id=other_user.id,
    )

    create_resume_version(
        db_session,
        resume_id=other_resume.id,
        version_number=1,
    )

    response = client.get(
        f"/api/resumes/{other_resume.id}/versions",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found."


def test_user_cannot_get_another_users_latest_version(
    authenticated_client,
    db_session,
):
    client, _ = authenticated_client

    other_user = create_user(db_session)

    other_resume = create_resume(
        db_session,
        user_id=other_user.id,
    )

    create_resume_version(
        db_session,
        resume_id=other_resume.id,
        version_number=1,
    )

    response = client.get(
        f"/api/resumes/{other_resume.id}/versions/latest",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found."


def test_user_cannot_get_another_users_resume_version(
    authenticated_client,
    db_session,
):
    client, _ = authenticated_client

    other_user = create_user(db_session)

    other_resume = create_resume(
        db_session,
        user_id=other_user.id,
    )

    version = create_resume_version(
        db_session,
        resume_id=other_resume.id,
        version_number=1,
    )

    response = client.get(
        f"/api/resumes/{other_resume.id}/versions/{version.id}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found."


def test_version_cannot_be_accessed_through_wrong_resume(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume_a = create_resume(
        db_session,
        user_id=user.id,
        title="Resume A",
    )

    resume_b = create_resume(
        db_session,
        user_id=user.id,
        title="Resume B",
    )

    version_a = create_resume_version(
        db_session,
        resume_id=resume_a.id,
        version_number=1,
    )

    response = client.get(
        f"/api/resumes/{resume_b.id}/versions/{version_a.id}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == ("Resume version not found.")
