from app.resumes.models import Resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)


def test_create_project(client, db_session):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Backend Resume",
        summary="Python Backend Developer",
    )

    db_session.add(resume)
    db_session.commit()
    db_session.refresh(resume)

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        f"/api/projects/resume/{resume.id}",
        json={
            "name": "AI Resume Builder",
            "description": (
                "A full-stack SaaS application for creating AI-powered resumes."
            ),
            "technologies": "FastAPI, PostgreSQL, Docker",
            "project_url": "https://example.com",
            "repository_url": ("https://github.com/example/ai-resume-builder"),
            "start_date": "2025-01-01",
            "end_date": None,
            "is_ongoing": True,
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["resume_id"] == str(resume.id)
    assert data["name"] == "AI Resume Builder"
    assert data["description"] == (
        "A full-stack SaaS application for creating AI-powered resumes."
    )
    assert data["technologies"] == "FastAPI, PostgreSQL, Docker"
    assert data["project_url"] == "https://example.com/"
    assert data["repository_url"] == "https://github.com/example/ai-resume-builder"
    assert data["start_date"] == "2025-01-01"
    assert data["end_date"] is None
    assert data["is_ongoing"] is True
    assert data["display_order"] == 0


def test_create_project_requires_authentication(
    client,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Resume",
    )

    db_session.add(resume)
    db_session.commit()
    db_session.refresh(resume)

    response = client.post(
        f"/api/projects/resume/{resume.id}",
        json={
            "name": "AI Resume Builder",
            "description": "Project description",
            "technologies": "FastAPI, PostgreSQL",
            "project_url": "https://example.com",
            "repository_url": ("https://github.com/example/project"),
            "start_date": "2025-01-01",
            "end_date": None,
            "is_ongoing": True,
            "display_order": 0,
        },
    )

    assert response.status_code == 401


def test_create_project_rejects_invalid_dates(
    client,
    db_session,
):
    user = create_user(
        db_session,
        email="john@example.com",
        password=DEFAULT_PASSWORD,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Backend Resume",
    )

    db_session.add(resume)
    db_session.commit()
    db_session.refresh(resume)

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        f"/api/projects/resume/{resume.id}",
        json={
            "name": "AI Resume Builder",
            "description": "Project description",
            "technologies": "FastAPI",
            "project_url": "https://example.com",
            "repository_url": ("https://github.com/example/project"),
            "start_date": "2025-01-01",
            "end_date": "2024-12-31",
            "is_ongoing": False,
            "display_order": 0,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 400


def test_create_ongoing_project_cannot_have_end_date(
    client,
    db_session,
):
    user = create_user(
        db_session,
        verified=True,
    )

    resume = Resume(
        user_id=user.id,
        title="Resume",
    )

    db_session.add(resume)
    db_session.commit()
    db_session.refresh(resume)

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        f"/api/projects/resume/{resume.id}",
        json={
            "name": "Portfolio",
            "description": "Project description",
            "technologies": "FastAPI",
            "project_url": "https://example.com",
            "repository_url": ("https://github.com/example/project"),
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
