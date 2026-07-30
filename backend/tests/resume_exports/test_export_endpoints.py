from io import BytesIO
from zipfile import ZipFile

from docx import Document

from tests.factories.resume_factory import create_resume
from tests.factories.user_factory import create_user


def test_export_resume_as_pdf(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
        title="Backend Developer Resume",
        summary="Python Backend Developer",
    )

    response = client.get(
        f"/api/resumes/{resume.id}/export/pdf",
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

    content_disposition = response.headers["content-disposition"]

    assert (
        'attachment; filename="Backend_Developer_Resume.pdf"'
        == content_disposition
    )

    assert response.content
    assert response.content.startswith(b"%PDF")


def test_export_resume_as_docx(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
        title="Backend Developer Resume",
        summary="Python Backend Developer",
    )

    response = client.get(
        f"/api/resumes/{resume.id}/export/docx",
    )

    assert response.status_code == 200
    assert (
        response.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    content_disposition = response.headers["content-disposition"]

    assert (
        'attachment; filename="Backend_Developer_Resume.docx"'
        == content_disposition
    )

    assert response.content

    with ZipFile(
        BytesIO(response.content),
    ) as archive:
        names = archive.namelist()

    assert "[Content_Types].xml" in names
    assert "word/document.xml" in names


def test_export_resume_as_pdf_returns_rendered_resume_content(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
        title="Software Engineer Resume",
        summary="Experienced Python developer.",
    )

    response = client.get(
        f"/api/resumes/{resume.id}/export/pdf",
    )

    assert response.status_code == 200
    assert response.content
    assert response.content.startswith(b"%PDF")


def test_export_resume_as_docx_contains_resume_content(
    authenticated_client,
    db_session,
):
    client, user = authenticated_client

    resume = create_resume(
        db_session,
        user_id=user.id,
        title="Software Engineer Resume",
        summary="Experienced Python developer.",
    )

    response = client.get(
        f"/api/resumes/{resume.id}/export/docx",
    )

    assert response.status_code == 200

    document = Document(
        BytesIO(response.content),
    )

    document_text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )

    assert resume.title in document_text
    assert resume.summary in document_text


def test_export_resume_requires_authentication(
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

    pdf_response = client.get(
        f"/api/resumes/{resume.id}/export/pdf",
    )

    docx_response = client.get(
        f"/api/resumes/{resume.id}/export/docx",
    )

    assert pdf_response.status_code == 401
    assert docx_response.status_code == 401


def test_user_cannot_export_another_users_resume(
    authenticated_client,
    db_session,
):
    client, authenticated_user = authenticated_client

    other_user = create_user(
        db_session,
        verified=True,
    )

    resume = create_resume(
        db_session,
        user_id=other_user.id,
    )

    assert resume.user_id != authenticated_user.id

    pdf_response = client.get(
        f"/api/resumes/{resume.id}/export/pdf",
    )

    docx_response = client.get(
        f"/api/resumes/{resume.id}/export/docx",
    )

    assert pdf_response.status_code == 404
    assert docx_response.status_code == 404


def test_export_nonexistent_resume_returns_not_found(
    authenticated_client,
):
    client, _ = authenticated_client

    nonexistent_resume_id = (
        "00000000-0000-0000-0000-000000000000"
    )

    pdf_response = client.get(
        f"/api/resumes/{nonexistent_resume_id}/export/pdf",
    )

    docx_response = client.get(
        f"/api/resumes/{nonexistent_resume_id}/export/docx",
    )

    assert pdf_response.status_code == 404
    assert docx_response.status_code == 404