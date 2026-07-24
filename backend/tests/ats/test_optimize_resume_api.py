from unittest.mock import MagicMock

from app.ai.schemas import ATSOptimizationResult
from app.ats.dependencies import get_ats_ai_service
from app.common.constants import ResumeVersionSource
from app.main import app
from app.resume_versions.repository import ResumeVersionRepository
from app.resume_versions.service import ResumeVersionService
from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import create_user


def test_optimize_resume_creates_ats_version(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    ai_service = MagicMock()

    ai_service.optimize.return_value = ATSOptimizationResult(
        optimized_resume="ATS optimized resume",
        ats_score=92,
        matched_keywords=[
            "python",
            "fastapi",
        ],
        missing_keywords=[
            "docker",
        ],
        recommendations=[
            "Mention Docker experience.",
        ],
    )

    app.dependency_overrides[get_ats_ai_service] = lambda: ai_service

    try:
        response = client.post(
            f"/api/ats/optimize/{resume.id}",
            json={
                "job_description": "Python FastAPI Docker",
                "target_job_title": "Backend Engineer",
            },
        )

        assert response.status_code == 200

        versions_response = client.get(
            f"/api/resumes/{resume.id}/versions",
        )

        assert versions_response.status_code == 200

        versions = versions_response.json()

        assert len(versions) == 1
        assert versions[0]["version_number"] == 1
        assert versions[0]["source"] == (ResumeVersionSource.ATS.value)

        assert versions[0]["snapshot"]["generated_content"] == ("ATS optimized resume")

    finally:
        app.dependency_overrides.clear()


def test_ats_optimization_increments_existing_resume_version(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    version_service = ResumeVersionService(
        ResumeVersionRepository(db_session),
    )

    version_service.create_version(
        resume_id=resume.id,
        snapshot={
            "title": "Original Resume",
        },
        source=ResumeVersionSource.USER,
        change_summary="Initial resume version",
    )

    ai_service = MagicMock()

    ai_service.optimize.return_value = ATSOptimizationResult(
        optimized_resume="ATS optimized resume",
        ats_score=90,
        matched_keywords=[
            "python",
        ],
        missing_keywords=[],
        recommendations=[],
    )

    app.dependency_overrides[get_ats_ai_service] = lambda: ai_service

    try:
        response = client.post(
            f"/api/ats/optimize/{resume.id}",
            json={
                "job_description": "Python backend engineer",
                "target_job_title": None,
            },
        )

        assert response.status_code == 200

        versions_response = client.get(
            f"/api/resumes/{resume.id}/versions",
        )

        assert versions_response.status_code == 200

        versions = versions_response.json()

        assert len(versions) == 2

        assert [version["version_number"] for version in versions] == [
            2,
            1,
        ]

        assert versions[0]["source"] == (ResumeVersionSource.ATS.value)

        assert versions[0]["snapshot"]["generated_content"] == ("ATS optimized resume")

        assert versions[1]["source"] == (ResumeVersionSource.USER.value)

    finally:
        app.dependency_overrides.clear()


def test_ats_optimization_creates_version_without_target_job_title(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    ai_service = MagicMock()

    ai_service.optimize.return_value = ATSOptimizationResult(
        optimized_resume="ATS optimized resume",
        ats_score=88,
        matched_keywords=[
            "python",
        ],
        missing_keywords=[],
        recommendations=[],
    )

    app.dependency_overrides[get_ats_ai_service] = lambda: ai_service

    try:
        response = client.post(
            f"/api/ats/optimize/{resume.id}",
            json={
                "job_description": "Python developer",
            },
        )

        assert response.status_code == 200

        versions_response = client.get(
            f"/api/resumes/{resume.id}/versions",
        )

        assert versions_response.status_code == 200

        versions = versions_response.json()

        assert len(versions) == 1
        assert versions[0]["version_number"] == 1

        assert versions[0]["source"] == (ResumeVersionSource.ATS.value)

        assert versions[0]["change_summary"] == ("Resume optimized for ATS.")

    finally:
        app.dependency_overrides.clear()


def test_ats_optimization_updates_resume_generated_content(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
    )

    ai_service = MagicMock()

    ai_service.optimize.return_value = ATSOptimizationResult(
        optimized_resume="Updated ATS resume content",
        ats_score=95,
        matched_keywords=[
            "python",
            "fastapi",
        ],
        missing_keywords=[],
        recommendations=[],
    )

    app.dependency_overrides[get_ats_ai_service] = lambda: ai_service

    try:
        response = client.post(
            f"/api/ats/optimize/{resume.id}",
            json={
                "job_description": ("Python FastAPI backend developer"),
                "target_job_title": "Backend Developer",
            },
        )

        assert response.status_code == 200

    finally:
        app.dependency_overrides.clear()

    db_session.refresh(resume)

    assert resume.generated_content == ("Updated ATS resume content")

    assert resume.generated_at is not None


def test_ats_optimization_cannot_access_another_users_resume(
    authenticated_client,
    db_session,
):
    client, _ = authenticated_client

    other_user = create_user(
        db_session,
    )

    other_resume = create_resume(
        db_session,
        user_id=other_user.id,
    )

    ai_service = MagicMock()

    app.dependency_overrides[get_ats_ai_service] = lambda: ai_service

    try:
        response = client.post(
            f"/api/ats/optimize/{other_resume.id}",
            json={
                "job_description": "Python backend engineer",
            },
        )

        assert response.status_code == 403

        ai_service.optimize.assert_not_called()

    finally:
        app.dependency_overrides.clear()


def test_ats_optimization_returns_404_for_missing_resume(
    authenticated_client,
):
    client, _ = authenticated_client

    ai_service = MagicMock()

    app.dependency_overrides[get_ats_ai_service] = lambda: ai_service

    try:
        response = client.post(
            "/api/ats/optimize/" "00000000-0000-0000-0000-000000000000",
            json={
                "job_description": "Python backend engineer",
            },
        )

        assert response.status_code == 404

        ai_service.optimize.assert_not_called()

    finally:
        app.dependency_overrides.clear()
