from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.resume_exports.exceptions import (
    ResumeExportNotFound,
    UnsupportedResumeExportFormat,
)
from app.resume_exports.renderers.models import RenderedResume
from app.resume_exports.schemas import ResumeExportFormat
from app.resume_exports.service import ResumeExportService
from tests.factories.resume_factory import make_resume


@pytest.fixture
def repository():
    return Mock()


@pytest.fixture
def pdf_renderer():
    return Mock()


@pytest.fixture
def docx_renderer():
    return Mock()


@pytest.fixture
def service(
    repository,
    pdf_renderer,
    docx_renderer,
):
    return ResumeExportService(
        repository=repository,
        pdf_renderer=pdf_renderer,
        docx_renderer=docx_renderer,
    )


def test_export_resume_uses_pdf_renderer(
    service,
    repository,
    pdf_renderer,
):
    user_id = uuid4()

    resume = make_resume(
        user_id=user_id,
    )

    repository.get_for_export.return_value = resume

    rendered = RenderedResume(
        content=b"pdf",
        filename="resume.pdf",
        media_type="application/pdf",
    )

    pdf_renderer.render.return_value = rendered

    result = service.export_resume(
        user_id=user_id,
        resume_id=resume.id,
        export_format=ResumeExportFormat.PDF,
    )

    assert result is rendered

    repository.get_for_export.assert_called_once_with(
        resume.id,
    )

    pdf_renderer.render.assert_called_once_with(
        resume,
    )


def test_export_resume_uses_docx_renderer(
    service,
    repository,
    docx_renderer,
):
    user_id = uuid4()

    resume = make_resume(
        user_id=user_id,
    )

    repository.get_for_export.return_value = resume

    rendered = RenderedResume(
        content=b"docx",
        filename="resume.docx",
        media_type=(
            "application/"
            "vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
    )

    docx_renderer.render.return_value = rendered

    result = service.export_resume(
        user_id=user_id,
        resume_id=resume.id,
        export_format=ResumeExportFormat.DOCX,
    )

    assert result is rendered

    repository.get_for_export.assert_called_once_with(
        resume.id,
    )

    docx_renderer.render.assert_called_once_with(
        resume,
    )


def test_export_resume_raises_when_resume_not_found(
    service,
    repository,
):
    repository.get_for_export.return_value = None

    with pytest.raises(
        ResumeExportNotFound,
        match="Resume not found.",
    ):
        service.export_resume(
            user_id=uuid4(),
            resume_id=uuid4(),
            export_format=ResumeExportFormat.PDF,
        )


def test_export_resume_raises_when_resume_belongs_to_another_user(
    service,
    repository,
):
    resume = make_resume(
        user_id=uuid4(),
    )

    repository.get_for_export.return_value = resume

    with pytest.raises(
        ResumeExportNotFound,
        match="Resume not found.",
    ):
        service.export_resume(
            user_id=uuid4(),
            resume_id=resume.id,
            export_format=ResumeExportFormat.PDF,
        )


def test_get_renderer_returns_pdf_renderer(
    service,
    pdf_renderer,
):
    renderer = service._get_renderer(
        ResumeExportFormat.PDF,
    )

    assert renderer is pdf_renderer


def test_get_renderer_returns_docx_renderer(
    service,
    docx_renderer,
):
    renderer = service._get_renderer(
        ResumeExportFormat.DOCX,
    )

    assert renderer is docx_renderer


def test_get_renderer_raises_for_unknown_format(
    service,
):
    with pytest.raises(
        UnsupportedResumeExportFormat,
    ):
        service._get_renderer(
            "xlsx",
        )