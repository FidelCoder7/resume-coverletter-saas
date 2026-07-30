from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.resume_exports.renderers.docx import DocxResumeRenderer
from app.resume_exports.renderers.pdf import PdfResumeRenderer
from app.resume_exports.service import ResumeExportService
from app.resumes.repository import ResumeRepository


def get_resume_export_service(
    db: Session = Depends(get_db),
) -> ResumeExportService:
    """
    Return the resume export service with all supported
    document renderers configured.
    """

    repository = ResumeRepository(db)

    pdf_renderer = PdfResumeRenderer()
    docx_renderer = DocxResumeRenderer()

    return ResumeExportService(
        repository=repository,
        pdf_renderer=pdf_renderer,
        docx_renderer=docx_renderer,
    )