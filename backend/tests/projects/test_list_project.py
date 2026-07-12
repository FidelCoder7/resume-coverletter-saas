from tests.factories.project_factory import create_project
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_list_projects(client, db_session):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    create_project(
        db_session,
        resume_id=resume.id,
        name="AI Resume Builder",
        display_order=0,
    )

    create_project(
        db_session,
        resume_id=resume.id,
        name="Portfolio Website",
        display_order=1,
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        f"/api/projects/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["projects"]) == 2
    assert data["projects"][0]["name"] == "AI Resume Builder"
    assert data["projects"][1]["name"] == "Portfolio Website"


def test_list_returns_only_resume_projects(
    client,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    resume_one = create_resume(
        db_session,
        user_id=user.id,
    )

    resume_two = create_resume(
        db_session,
        user_id=user.id,
        title="Second Resume",
    )

    create_project(
        db_session,
        resume_id=resume_one.id,
        name="AI Resume Builder",
    )

    create_project(
        db_session,
        resume_id=resume_two.id,
        name="Portfolio Website",
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        f"/api/projects/resume/{resume_one.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["projects"]) == 1
    assert data["projects"][0]["name"] == "AI Resume Builder"


def test_cannot_list_another_users_resume_projects(
    client,
    db_session,
):
    owner = create_user(
        db_session,
        verified=True,
    )

    other_user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=owner.id,
    )

    create_project(
        db_session,
        resume_id=resume.id,
    )

    login = client.post(
        "/auth/login",
        data={
            "username": other_user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        f"/api/projects/resume/{resume.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403
