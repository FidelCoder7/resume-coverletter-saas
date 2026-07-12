from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import (
    DEFAULT_PASSWORD,
    create_user,
)

DEFAULT_CONTENT = (
    "I am excited to apply for this position because my experience "
    "building production-ready backend applications with Python and "
    "FastAPI aligns well with your requirements. I enjoy solving "
    "real-world problems, writing clean code, and collaborating with "
    "engineering teams to deliver reliable software."
)


def test_create_cover_letter(
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
        f"/api/cover-letters/resume/{resume.id}",
        json={
            "title": "Backend Engineer Cover Letter",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "content": DEFAULT_CONTENT,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["resume_id"] == str(resume.id)
    assert data["title"] == "Backend Engineer Cover Letter"
    assert data["company_name"] == "OpenAI"
    assert data["job_title"] == "Backend Engineer"
    assert data["content"] == DEFAULT_CONTENT


def test_create_cover_letter_requires_authentication(
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
        f"/api/cover-letters/resume/{resume.id}",
        json={
            "title": "Backend Engineer Cover Letter",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "content": DEFAULT_CONTENT,
        },
    )

    assert response.status_code == 401


def test_create_cover_letter_on_another_users_resume_is_forbidden(
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

    login = client.post(
        "/auth/login",
        data={
            "username": other_user.email,
            "password": DEFAULT_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        f"/api/cover-letters/resume/{resume.id}",
        json={
            "title": "Backend Engineer Cover Letter",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
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


def test_create_cover_letter_for_unknown_resume_returns_404(
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

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        f"/api/cover-letters/resume/{uuid4()}",
        json={
            "title": "Backend Engineer Cover Letter",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "content": DEFAULT_CONTENT,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    assert response.json() == {"detail": "Resume not found."}


def test_create_cover_letter_rejects_short_content(
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

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        f"/api/cover-letters/resume/{resume.id}",
        json={
            "title": "Backend Engineer Cover Letter",
            "company_name": "OpenAI",
            "job_title": "Backend Engineer",
            "content": "Too short",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 422


def test_cannot_create_duplicate_cover_letter_title_for_same_resume(
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

    assert login.status_code == 200

    token = login.json()["access_token"]

    payload = {
        "title": "Backend Engineer Cover Letter",
        "company_name": "OpenAI",
        "job_title": "Backend Engineer",
        "content": DEFAULT_CONTENT,
    }

    response = client.post(
        f"/api/cover-letters/resume/{resume.id}",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    response = client.post(
        f"/api/cover-letters/resume/{resume.id}",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": ("A cover letter with this title already exists on this resume.")
    }
