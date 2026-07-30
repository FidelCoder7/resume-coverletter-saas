from io import BytesIO

import pytest
from pypdf import PdfReader

from app.resume_exports.renderers import PdfResumeRenderer
from tests.factories.resume_factory import make_resume


@pytest.fixture
def resume():
    resume = make_resume(
    user_id="00000000-0000-0000-0000-000000000001",
    title="Backend Resume",
    summary="Python Backend Developer",
    )


    resume.experiences = []
    resume.educations = []
    resume.skills = []
    resume.projects = []
    resume.certifications = []

    return resume


def test_pdf_renderer_metadata():
    renderer = PdfResumeRenderer()


    assert renderer.media_type == "application/pdf"
    assert renderer.file_extension == "pdf"


def test_pdf_renderer_produces_valid_pdf(
    resume,
):
    renderer = PdfResumeRenderer()

    result = renderer.render(
        resume,
    )

    assert result.content
    assert result.filename.endswith(".pdf")
    assert result.media_type == renderer.media_type

    reader = PdfReader(
        BytesIO(result.content),
    )

    assert len(reader.pages) >= 1


def test_pdf_renderer_contains_resume_content(
    resume,
):
    renderer = PdfResumeRenderer()


    result = renderer.render(
        resume,
    )

    reader = PdfReader(
        BytesIO(result.content),
    )

    document_text = "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )

    assert resume.title in document_text

    if resume.summary:
        assert resume.summary in document_text

    for experience in resume.experiences:
        assert experience.company in document_text
        assert experience.job_title in document_text

    for education in resume.educations:
        assert education.institution in document_text

    for skill in resume.skills:
        assert skill.name in document_text

    for project in resume.projects:
        assert project.name in document_text

    for certification in resume.certifications:
        assert certification.name in document_text


def test_pdf_renderer_uses_fallback_filename_for_empty_title(
    resume,
):
    resume.title = ""


    renderer = PdfResumeRenderer()

    result = renderer.render(
        resume,
    )

    assert result.filename == "resume.pdf"
