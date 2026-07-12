from uuid import uuid4

from tests.factories.cover_letter_factory import (
    DEFAULT_CONTENT,
    create_cover_letter,
)
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)

UPDATED_CONTENT = (
    "I am excited to contribute my backend engineering experience to your "
    "team. My background includes designing REST APIs, working with FastAPI, "
    "SQLAlchemy, PostgreSQL, automated testing, and deploying production-ready "
    "applications while maintaining clean architecture principles."
)


def test_update_cover_letter(
    client,
    db_session,
):
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

    cover_letter = create_cover_letter(
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
        f"/api/cover-letters/{cover_letter.id}",
        json={
            "title": "Senior Backend Engineer",
            "company_name": "Anthropic",
            "job_title": "Senior Backend Engineer",
            "content": UPDATED_CONTENT,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Senior Backend Engineer"
    assert data["company_name"] == "Anthropic"
    assert data["job_title"] == "Senior Backend Engineer"
    assert data["content"] == UPDATED_CONTENT

    db_session.refresh(cover_letter)

    assert cover_letter.title == "Senior Backend Engineer"
    assert cover_letter.company_name == "Anthropic"
    assert cover_letter.job_title == "Senior Backend Engineer"
    assert cover_letter.content == UPDATED_CONTENT


def test_cannot_update_another_users_cover_letter(
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

    cover_letter = create_cover_letter(
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
        f"/api/cover-letters/{cover_letter.id}",
        json={
            "title": "Unauthorized Update",
            "company_name": "Company",
            "job_title": "Developer",
            "content": DEFAULT_CONTENT,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403

    assert response.json() == {
        "detail": "You do not have permission to modify this resume."
    }


def test_update_unknown_cover_letter_returns_404(
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
        f"/api/cover-letters/{uuid4()}",
        json={
            "title": "Backend Engineer",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "content": DEFAULT_CONTENT,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    assert response.json() == {"detail": "Cover letter not found."}


def test_update_cover_letter_rejects_short_content(
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

    cover_letter = create_cover_letter(
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
        f"/api/cover-letters/{cover_letter.id}",
        json={
            "title": "Backend Engineer",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "content": "Too short",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 422


def test_cannot_update_cover_letter_to_duplicate_title(
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

    first_cover_letter = create_cover_letter(
        db_session,
        resume_id=resume.id,
        title="Backend Engineer Cover Letter",
        company_name="OpenAI",
        job_title="Backend Engineer",
    )

    second_cover_letter = create_cover_letter(
        db_session,
        resume_id=resume.id,
        title="Software Engineer Cover Letter",
        company_name="Google",
        job_title="Software Engineer",
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
        f"/api/cover-letters/{second_cover_letter.id}",
        json={
            "title": first_cover_letter.title,
            "company_name": "Microsoft",
            "job_title": "Backend Developer",
            "content": DEFAULT_CONTENT,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": ("A cover letter with this title already exists on this resume.")
    }
