from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.ai.schemas import ATSOptimizationResult
from app.ats.schemas import ATSOptimizationResponse
from app.ats.service import ATSService
from app.common.constants import ResumeVersionSource
from app.resumes.exceptions import (
    ResumeAccessDenied,
    ResumeNotFound,
)


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def ai_service():
    return MagicMock()


@pytest.fixture
def resume_version_service():
    return MagicMock()


@pytest.fixture
def service(
    repository,
    ai_service,
    resume_version_service,
):
    return ATSService(
        repository=repository,
        ai_service=ai_service,
        resume_version_service=resume_version_service,
    )


def build_resume(
    user_id,
):
    resume = MagicMock()

    resume.id = uuid4()
    resume.user_id = user_id

    return resume


def build_optimization_result():
    return ATSOptimizationResult(
        optimized_resume="Optimized resume",
        ats_score=91,
        matched_keywords=["python"],
        missing_keywords=["aws"],
        recommendations=["Add AWS"],
    )


def configure_successful_optimization(
    repository,
    ai_service,
    resume,
    monkeypatch,
):
    repository.get_for_generation.return_value = resume
    repository.update.return_value = resume

    monkeypatch.setattr(
        "app.ats.service.ResumeFormatter.format",
        lambda _: "formatted resume",
    )

    ai_service.optimize.return_value = build_optimization_result()


def test_optimize_resume_success(
    service,
    repository,
    ai_service,
    resume_version_service,
    monkeypatch,
):
    user_id = uuid4()
    resume = build_resume(user_id)

    configure_successful_optimization(
        repository,
        ai_service,
        resume,
        monkeypatch,
    )

    result = service.optimize_resume(
        user_id=user_id,
        resume_id=resume.id,
        job_description="Python AWS",
        target_job_title="Backend Engineer",
    )

    assert isinstance(
        result,
        ATSOptimizationResponse,
    )

    assert result.resume_id == resume.id
    assert result.optimized_resume == "Optimized resume"
    assert result.ats_score == 91

    repository.update.assert_called_once_with(
        resume,
    )

    resume_version_service.create_version_from_resume.assert_called_once_with(
        resume=resume,
        source=ResumeVersionSource.ATS,
        change_summary="Resume optimized for ATS for Backend Engineer.",
    )


def test_resume_not_found(
    service,
    repository,
):
    repository.get_for_generation.return_value = None

    with pytest.raises(
        ResumeNotFound,
    ):
        service.optimize_resume(
            user_id=uuid4(),
            resume_id=uuid4(),
            job_description="JD",
            target_job_title=None,
        )


def test_access_denied(
    service,
    repository,
):
    resume = build_resume(
        uuid4(),
    )

    repository.get_for_generation.return_value = resume

    with pytest.raises(
        ResumeAccessDenied,
    ):
        service.optimize_resume(
            user_id=uuid4(),
            resume_id=resume.id,
            job_description="JD",
            target_job_title=None,
        )


def test_formatter_called(
    service,
    repository,
    ai_service,
    monkeypatch,
):
    user_id = uuid4()

    resume = build_resume(
        user_id,
    )

    repository.get_for_generation.return_value = resume
    repository.update.return_value = resume

    formatter = MagicMock(
        return_value="formatted",
    )

    monkeypatch.setattr(
        "app.ats.service.ResumeFormatter.format",
        formatter,
    )

    ai_service.optimize.return_value = build_optimization_result()

    service.optimize_resume(
        user_id=user_id,
        resume_id=resume.id,
        job_description="JD",
        target_job_title=None,
    )

    formatter.assert_called_once_with(
        resume,
    )


def test_ai_service_receives_formatted_resume(
    service,
    repository,
    ai_service,
    monkeypatch,
):
    user_id = uuid4()

    resume = build_resume(
        user_id,
    )

    repository.get_for_generation.return_value = resume
    repository.update.return_value = resume

    monkeypatch.setattr(
        "app.ats.service.ResumeFormatter.format",
        lambda _: "FORMATTED",
    )

    ai_service.optimize.return_value = build_optimization_result()

    service.optimize_resume(
        user_id=user_id,
        resume_id=resume.id,
        job_description="Python",
        target_job_title="Backend",
    )

    ai_service.optimize.assert_called_once_with(
        user_id=user_id,
        resume_id=resume.id,
        resume_content="FORMATTED",
        job_description="Python",
        target_job_title="Backend",
    )


def test_returns_response_model(
    service,
    repository,
    ai_service,
    monkeypatch,
):
    user_id = uuid4()

    resume = build_resume(
        user_id,
    )

    repository.get_for_generation.return_value = resume
    repository.update.return_value = resume

    monkeypatch.setattr(
        "app.ats.service.ResumeFormatter.format",
        lambda _: "",
    )

    ai_service.optimize.return_value = build_optimization_result()

    response = service.optimize_resume(
        user_id=user_id,
        resume_id=resume.id,
        job_description="JD",
        target_job_title=None,
    )

    assert response.resume_id == resume.id
    assert response.optimized_resume == "Optimized resume"
    assert response.ats_score == 91
    assert response.matched_keywords == [
        "python",
    ]
    assert response.missing_keywords == [
        "aws",
    ]


def test_ats_optimization_creates_ats_resume_version(
    service,
    repository,
    ai_service,
    resume_version_service,
    monkeypatch,
):
    user_id = uuid4()

    resume = build_resume(
        user_id,
    )

    configure_successful_optimization(
        repository,
        ai_service,
        resume,
        monkeypatch,
    )

    service.optimize_resume(
        user_id=user_id,
        resume_id=resume.id,
        job_description="Python AWS",
        target_job_title="Backend Engineer",
    )

    resume_version_service.create_version_from_resume.assert_called_once_with(
        resume=resume,
        source=ResumeVersionSource.ATS,
        change_summary="Resume optimized for ATS for Backend Engineer.",
    )


def test_ats_optimization_creates_ats_version_without_target_job_title(
    service,
    repository,
    ai_service,
    resume_version_service,
    monkeypatch,
):
    user_id = uuid4()

    resume = build_resume(
        user_id,
    )

    configure_successful_optimization(
        repository,
        ai_service,
        resume,
        monkeypatch,
    )

    service.optimize_resume(
        user_id=user_id,
        resume_id=resume.id,
        job_description="Python AWS",
        target_job_title=None,
    )

    resume_version_service.create_version_from_resume.assert_called_once_with(
        resume=resume,
        source=ResumeVersionSource.ATS,
        change_summary="Resume optimized for ATS.",
    )
