from tests.utils import auth_headers, authenticated_user


def test_delete_resume(client, db_session):
    _, token = authenticated_user(client, db_session)

    created = client.post(
        "/api/resumes",
        json={
            "title": "Resume",
            "summary": "Summary",
        },
        headers=auth_headers(token),
    )

    resume_id = created.json()["id"]

    response = client.delete(
        f"/api/resumes/{resume_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 204


def test_cannot_delete_another_users_resume(client, db_session):
    _, owner_token = authenticated_user(client, db_session)

    created = client.post(
        "/api/resumes",
        json={
            "title": "Resume",
            "summary": "Summary",
        },
        headers=auth_headers(owner_token),
    )

    resume_id = created.json()["id"]

    _, attacker_token = authenticated_user(client, db_session)

    response = client.delete(
        f"/api/resumes/{resume_id}",
        headers=auth_headers(attacker_token),
    )

    assert response.status_code == 403
