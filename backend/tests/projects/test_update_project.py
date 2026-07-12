from uuid import uuid4

from tests.factories.project_factory import create_project
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_update_project(client, db_session):
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

    project = create_project(
        db_session,
        resume_id=resume.id,
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

    response = client.put(
        f"/api/projects/{project.id}",
        json={
            "name": "Resume SaaS",
            "description": "Updated project description.",
            "technologies": "FastAPI, PostgreSQL, Docker, Redis",
            "project_url": "https://example.com",
            "repository_url": "https://github.com/example/resume-saas",
            "start_date": "2025-01-01",
            "end_date": "2025-06-30",
            "is_ongoing": False,
            "display_order": 1,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Resume SaaS"
    assert data["description"] == "Updated project description."
    assert data["technologies"] == "FastAPI, PostgreSQL, Docker, Redis"
    assert data["project_url"] == "https://example.com/"
    assert data["repository_url"] == "https://github.com/example/resume-saas"
    assert data["start_date"] == "2025-01-01"
    assert data["end_date"] == "2025-06-30"
    assert data["is_ongoing"] is False
    assert data["display_order"] == 1


def test_cannot_update_another_users_project(
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

    project = create_project(
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

    response = client.put(
        f"/api/projects/{project.id}",
        json={
            "name": "Unauthorized Update",
            "description": "Should fail.",
            "technologies": "FastAPI",
            "project_url": "https://example.com",
            "repository_url": "https://github.com/example/project",
            "start_date": "2025-01-01",
            "end_date": None,
            "is_ongoing": True,
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_update_unknown_project_returns_404(
    client,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
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

    response = client.put(
        f"/api/projects/{uuid4()}",
        json={
            "name": "Resume SaaS",
            "description": "Project description",
            "technologies": "FastAPI",
            "project_url": "https://example.com",
            "repository_url": "https://github.com/example/project",
            "start_date": "2025-01-01",
            "end_date": None,
            "is_ongoing": True,
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404


def test_update_project_rejects_invalid_dates(
    client,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    project = create_project(
        db_session,
        resume_id=resume.id,
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

    response = client.put(
        f"/api/projects/{project.id}",
        json={
            "name": "Resume SaaS",
            "description": "Project description",
            "technologies": "FastAPI",
            "project_url": "https://example.com",
            "repository_url": "https://github.com/example/project",
            "start_date": "2025-06-01",
            "end_date": "2025-01-01",
            "is_ongoing": False,
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 400


def test_update_ongoing_project_cannot_have_end_date(
    client,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    project = create_project(
        db_session,
        resume_id=resume.id,
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

    response = client.put(
        f"/api/projects/{project.id}",
        json={
            "name": "Resume SaaS",
            "description": "Project description",
            "technologies": "FastAPI",
            "project_url": "https://example.com",
            "repository_url": "https://github.com/example/project",
            "start_date": "2025-01-01",
            "end_date": "2025-06-01",
            "is_ongoing": True,
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 400
