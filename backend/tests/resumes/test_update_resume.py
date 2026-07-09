from tests.utils import auth_headers, authenticated_user


def test_update_resume(client, db_session):
    _, token = authenticated_user(client, db_session)

    created = client.post(
        "/api/resumes",
        json={
            "title": "Old",
            "summary": "Old summary",
        },
        headers=auth_headers(token),
    )

    resume_id = created.json()["id"]

    response = client.put(
        f"/api/resumes/{resume_id}",
        json={
            "title": "New",
            "summary": "Updated summary",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New"
    assert data["summary"] == "Updated summary"


def test_cannot_update_another_users_resume(client, db_session):
    _, owner_token = authenticated_user(client, db_session)

    created = client.post(
        "/api/resumes",
        json={
            "title": "Owner Resume",
            "summary": "Summary",
        },
        headers=auth_headers(owner_token),
    )

    resume_id = created.json()["id"]

    _, attacker_token = authenticated_user(client, db_session)

    response = client.put(
        f"/api/resumes/{resume_id}",
        json={
            "title": "Hacked",
            "summary": "Nope",
        },
        headers=auth_headers(attacker_token),
    )

    assert response.status_code == 403
