from tests.factories.resume_factory import create_resume


def test_create_resume_version_endpoint_is_not_public(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    response = client.post(
        f"/api/resumes/{resume.id}/versions",
        json={
            "snapshot": {
                "title": "Unauthorized version",
            },
            "source": "user",
        },
    )

    assert response.status_code == 405
