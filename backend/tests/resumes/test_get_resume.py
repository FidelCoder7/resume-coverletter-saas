from tests.utils import auth_headers, authenticated_user


def test_get_resume(client, db_session):
    _, token = authenticated_user(client, db_session)

    created = client.post(
        "/api/resumes",
        json={
            "title": "Backend Resume",
            "summary": "Python",
        },
        headers=auth_headers(token),
    )

    resume_id = created.json()["id"]

    response = client.get(
        f"/api/resumes/{resume_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    assert response.json()["id"] == resume_id


def test_cannot_get_another_users_resume(client, db_session):
    _, owner_token = authenticated_user(client, db_session)

    created = client.post(
        "/api/resumes",
        json={
            "title": "Private Resume",
            "summary": "Owner only",
        },
        headers=auth_headers(owner_token),
    )

    resume_id = created.json()["id"]

    _, attacker_token = authenticated_user(client, db_session)

    response = client.get(
        f"/api/resumes/{resume_id}",
        headers=auth_headers(attacker_token),
    )

    assert response.status_code == 403


def test_get_unknown_resume_returns_404(client, db_session):
    _, token = authenticated_user(client, db_session)

    response = client.get(
        "/api/resumes/00000000-0000-0000-0000-000000000000",
        headers=auth_headers(token),
    )

    assert response.status_code == 404
