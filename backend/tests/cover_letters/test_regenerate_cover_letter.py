from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)
from tests.utils import auth_headers, authenticated_user

DEFAULT_CONTENT = (
    "I am excited to apply for this opportunity. "
    "My background in FastAPI, SQLAlchemy, PostgreSQL, "
    "testing, clean architecture, and REST API development "
    "makes me an excellent fit for this position."
)


def create_cover_letter(
    client,
    token,
    resume,
):
    response = client.post(
        f"/api/cover-letters/resume/{resume.id}",
        json={
            "title": "Backend Engineer",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "content": DEFAULT_CONTENT,
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 201

    return response.json()


def test_regenerate_cover_letter_success(
    client,
    db_session,
):
    user, token = authenticated_user(client, db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    cover_letter = create_cover_letter(
        client,
        token,
        resume,
    )

    response = client.post(
        f"/api/cover-letters/{cover_letter['id']}/regenerate",
        json={
            "job_description": (
                "Looking for a backend engineer with FastAPI "
                "experience and strong testing skills."
            ),
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == cover_letter["id"]
    assert data["resume_id"] == str(resume.id)
    assert data["title"] == "Backend Engineer"
    assert data["company_name"] == "OpenAI"
    assert data["job_title"] == "Backend Engineer"

    assert data["content"] == "This is a generated cover letter for testing purposes."


def test_regenerate_requires_authentication(
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

    cover_letter = create_cover_letter(
        client,
        token,
        resume,
    )

    response = client.post(
        f"/api/cover-letters/{cover_letter['id']}/regenerate",
        json={
            "job_description": ("Backend engineer with Python experience."),
        },
    )

    assert response.status_code == 401


def test_regenerate_unknown_cover_letter_returns_404(
    client,
    db_session,
):
    from uuid import uuid4

    user, token = authenticated_user(client, db_session)

    response = client.post(
        f"/api/cover-letters/{uuid4()}/regenerate",
        json={
            "job_description": ("Looking for an experienced backend engineer."),
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Cover letter not found.",
    }


def test_regenerate_other_users_cover_letter_returns_403(
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
            "username": owner.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    owner_token = login.json()["access_token"]

    cover_letter = create_cover_letter(
        client,
        owner_token,
        resume,
    )

    login = client.post(
        "/auth/login",
        data={
            "username": attacker.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    attacker_token = login.json()["access_token"]

    response = client.post(
        f"/api/cover-letters/{cover_letter['id']}/regenerate",
        json={
            "job_description": ("Backend engineer with Python experience."),
        },
        headers=auth_headers(attacker_token),
    )

    assert response.status_code == 403

    assert response.json() == {
        "detail": "You do not have permission to access this resume.",
    }


def test_regenerate_rejects_short_job_description(
    client,
    db_session,
):
    user, token = authenticated_user(client, db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    cover_letter = create_cover_letter(
        client,
        token,
        resume,
    )

    response = client.post(
        f"/api/cover-letters/{cover_letter['id']}/regenerate",
        json={
            "job_description": "Too short",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 422


def test_regenerate_updates_existing_cover_letter(
    client,
    db_session,
):
    user, token = authenticated_user(client, db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    cover_letter = create_cover_letter(
        client,
        token,
        resume,
    )

    response = client.post(
        f"/api/cover-letters/{cover_letter['id']}/regenerate",
        json={
            "job_description": ("Looking for a senior backend engineer."),
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    response = client.get(
        f"/api/cover-letters/{cover_letter['id']}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    assert (
        response.json()["content"]
        == "This is a generated cover letter for testing purposes."
    )


def test_regenerate_preserves_cover_letter_metadata(
    client,
    db_session,
):
    user, token = authenticated_user(client, db_session)

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    cover_letter = create_cover_letter(
        client,
        token,
        resume,
    )

    client.post(
        f"/api/cover-letters/{cover_letter['id']}/regenerate",
        json={
            "job_description": ("Looking for an experienced backend engineer."),
        },
        headers=auth_headers(token),
    )

    response = client.get(
        f"/api/cover-letters/{cover_letter['id']}",
        headers=auth_headers(token),
    )

    data = response.json()

    assert data["title"] == "Backend Engineer"
    assert data["company_name"] == "OpenAI"
    assert data["job_title"] == "Backend Engineer"
