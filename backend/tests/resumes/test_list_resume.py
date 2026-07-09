from tests.utils import auth_headers, authenticated_user


def test_list_resumes(client, db_session):
    _, token = authenticated_user(client, db_session)

    client.post(
        "/api/resumes",
        json={
            "title": "Resume One",
            "summary": "Summary",
        },
        headers=auth_headers(token),
    )

    client.post(
        "/api/resumes",
        json={
            "title": "Resume Two",
            "summary": "Summary",
        },
        headers=auth_headers(token),
    )

    response = client.get(
        "/api/resumes",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["resumes"]) == 2


def test_list_returns_only_authenticated_users_resumes(
    client,
    db_session,
):
    _, token_one = authenticated_user(client, db_session)

    client.post(
        "/api/resumes",
        json={
            "title": "Resume A",
            "summary": "Owner A",
        },
        headers=auth_headers(token_one),
    )

    _, token_two = authenticated_user(client, db_session)

    client.post(
        "/api/resumes",
        json={
            "title": "Resume B",
            "summary": "Owner B",
        },
        headers=auth_headers(token_two),
    )

    response = client.get(
        "/api/resumes",
        headers=auth_headers(token_one),
    )

    assert response.status_code == 200

    resumes = response.json()["resumes"]

    assert len(resumes) == 1
    assert resumes[0]["title"] == "Resume A"
