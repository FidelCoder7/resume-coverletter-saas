from tests.factories.resume_factory import create_resume
from tests.utils import (
    auth_headers,
    authenticated_user,
)


def test_generate_resume(
    client,
    db_session,
):
    user, token = authenticated_user(
        client,
        db_session,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    response = client.post(
        f"/api/resumes/{resume.id}/generate",
        json={
            "target_job_title": "Backend Engineer",
            "job_description": ("Looking for a Python FastAPI backend engineer."),
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(resume.id)
    assert data["generated_content"] is not None
    assert data["generated_at"] is not None


def test_generate_resume_not_found(
    client,
    db_session,
):
    _, token = authenticated_user(
        client,
        db_session,
    )

    response = client.post(
        "/api/resumes/00000000-0000-0000-0000-000000000000/generate",
        json={
            "target_job_title": "Backend Engineer",
            "job_description": "Backend role.",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 404


def test_generate_resume_forbidden(
    client,
    db_session,
):
    owner, _ = authenticated_user(
        client,
        db_session,
    )

    other, token = authenticated_user(
        client,
        db_session,
    )

    resume = create_resume(
        db_session,
        user_id=owner.id,
    )

    response = client.post(
        f"/api/resumes/{resume.id}/generate",
        json={
            "target_job_title": "Backend Engineer",
            "job_description": "Backend role.",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 403


def test_generate_resume_persists_generated_content(
    client,
    db_session,
):
    user, token = authenticated_user(
        client,
        db_session,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    response = client.post(
        f"/api/resumes/{resume.id}/generate",
        json={
            "target_job_title": "Backend Engineer",
            "job_description": "FastAPI backend role.",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    db_session.refresh(resume)

    assert resume.generated_content is not None
    assert resume.generated_at is not None


def test_generate_resume_records_ai_usage(
    client,
    db_session,
):
    from app.ai_usage.models import AIUsage

    user, token = authenticated_user(
        client,
        db_session,
    )

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    response = client.post(
        f"/api/resumes/{resume.id}/generate",
        json={
            "target_job_title": "Backend Engineer",
            "job_description": "Backend role.",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    usage = db_session.query(AIUsage).one()

    assert usage.user_id == user.id
    assert usage.resume_id == resume.id
    assert usage.feature.value == "resume_generation"
    assert usage.status.value == "success"
