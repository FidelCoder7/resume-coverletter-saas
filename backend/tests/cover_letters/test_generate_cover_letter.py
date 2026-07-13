from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)

GENERATED_CONTENT = "This is a generated cover letter for testing purposes."


def test_generate_cover_letter(
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
        summary="Experienced Python backend developer.",
    )

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.post(
        f"/api/cover-letters/resume/{resume.id}/generate",
        json={
            "title": "Backend Engineer",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "job_description": (
                "Looking for an experienced FastAPI backend developer "
                "with PostgreSQL and REST API experience."
            ),
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["resume_id"] == str(resume.id)
    assert data["title"] == "Backend Engineer"
    assert data["company_name"] == "OpenAI"
    assert data["job_title"] == "Backend Engineer"
    assert data["content"] == GENERATED_CONTENT


def test_generate_cover_letter_requires_authentication(
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

    response = client.post(
        f"/api/cover-letters/resume/{resume.id}/generate",
        json={
            "title": "Backend Engineer",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "job_description": ("Looking for an experienced backend developer."),
        },
    )

    assert response.status_code == 401


def test_generate_cover_letter_for_unknown_resume_returns_404(
    client,
    db_session,
):
    from uuid import uuid4

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

    token = login.json()["access_token"]

    response = client.post(
        f"/api/cover-letters/resume/{uuid4()}/generate",
        json={
            "title": "Backend Engineer",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "job_description": ("Looking for an experienced backend developer."),
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Resume not found.",
    }


def test_generate_cover_letter_on_other_users_resume_returns_403(
    client,
    db_session,
):
    owner = create_user(
        db_session,
        verified=True,
    )

    attacker = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=owner.id,
    )

    login = client.post(
        "/auth/login",
        data={
            "username": attacker.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.post(
        f"/api/cover-letters/resume/{resume.id}/generate",
        json={
            "title": "Backend Engineer",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "job_description": ("Looking for an experienced backend developer."),
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403

    assert response.json() == {
        "detail": "You do not have permission to access this resume.",
    }


def test_generate_cover_letter_rejects_short_job_description(
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

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    response = client.post(
        f"/api/cover-letters/resume/{resume.id}/generate",
        json={
            "title": "Backend Engineer",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "job_description": "Too short",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 422


def test_generate_cover_letter_rejects_duplicate_title(
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

    login = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    token = login.json()["access_token"]

    payload = {
        "title": "Backend Engineer",
        "company_name": "OpenAI",
        "job_title": "Backend Engineer",
        "job_description": ("Looking for an experienced FastAPI backend developer."),
    }

    response = client.post(
        f"/api/cover-letters/resume/{resume.id}/generate",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    response = client.post(
        f"/api/cover-letters/resume/{resume.id}/generate",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": ("A cover letter with this title already exists on this resume."),
    }
