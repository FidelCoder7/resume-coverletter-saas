from unittest.mock import MagicMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.ats.dependencies import get_ats_service
from app.auth.dependencies import get_current_user
from app.main import app
from app.users.models import User

client = TestClient(app)


def build_user() -> User:
    user = MagicMock(spec=User)
    user.id = uuid4()
    return user


def build_response(resume_id):
    return {
        "resume_id": resume_id,
        "optimized_resume": "Optimized resume",
        "ats_score": 92,
        "matched_keywords": [
            "python",
            "fastapi",
        ],
        "missing_keywords": [
            "docker",
        ],
        "recommendations": [
            "Mention Docker experience.",
        ],
    }


def test_optimize_resume_success():
    resume_id = uuid4()

    current_user = build_user()

    service = MagicMock()

    service.optimize_resume.return_value = build_response(
        resume_id,
    )

    app.dependency_overrides[get_current_user] = lambda: current_user

    app.dependency_overrides[get_ats_service] = lambda: service

    response = client.post(
        f"/api/ats/optimize/{resume_id}",
        json={
            "job_description": "Python FastAPI Docker",
            "target_job_title": "Backend Engineer",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["resume_id"] == str(resume_id)
    assert body["ats_score"] == 92
    assert body["optimized_resume"] == "Optimized resume"

    service.optimize_resume.assert_called_once_with(
        user_id=current_user.id,
        resume_id=resume_id,
        job_description="Python FastAPI Docker",
        target_job_title="Backend Engineer",
    )

    app.dependency_overrides.clear()


def test_optimize_resume_without_target_job_title():
    resume_id = uuid4()

    current_user = build_user()

    service = MagicMock()

    service.optimize_resume.return_value = build_response(
        resume_id,
    )

    app.dependency_overrides[get_current_user] = lambda: current_user

    app.dependency_overrides[get_ats_service] = lambda: service

    response = client.post(
        f"/api/ats/optimize/{resume_id}",
        json={
            "job_description": "Python FastAPI",
        },
    )

    assert response.status_code == 200

    service.optimize_resume.assert_called_once_with(
        user_id=current_user.id,
        resume_id=resume_id,
        job_description="Python FastAPI",
        target_job_title=None,
    )

    app.dependency_overrides.clear()


def test_optimize_resume_requires_job_description():
    resume_id = uuid4()

    current_user = build_user()

    service = MagicMock()

    app.dependency_overrides[get_current_user] = lambda: current_user

    app.dependency_overrides[get_ats_service] = lambda: service

    response = client.post(
        f"/api/ats/optimize/{resume_id}",
        json={},
    )

    assert response.status_code == 422

    service.optimize_resume.assert_not_called()

    app.dependency_overrides.clear()


def test_optimize_resume_requires_authentication():
    app.dependency_overrides.clear()

    response = client.post(
        f"/api/ats/optimize/{uuid4()}",
        json={
            "job_description": "Python",
        },
    )

    assert response.status_code in (
        401,
        403,
    )
