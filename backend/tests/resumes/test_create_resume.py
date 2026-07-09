from tests.utils import auth_headers, authenticated_user


def test_create_resume(client, db_session):
    _, token = authenticated_user(client, db_session)

    response = client.post(
        "/api/resumes",
        json={
            "title": "Software Engineer Resume",
            "summary": "Experienced backend developer.",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Software Engineer Resume"
    assert data["summary"] == "Experienced backend developer."
    assert data["is_default"] is False


def test_create_resume_requires_authentication(client):
    response = client.post(
        "/api/resumes",
        json={
            "title": "Resume",
            "summary": "Summary",
        },
    )

    assert response.status_code == 401
