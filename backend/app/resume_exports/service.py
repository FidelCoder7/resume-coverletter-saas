from uuid import UUID

from app.resume_exports.exceptions import (
    ResumeExportNotFound,
    UnsupportedResumeExportFormat,
)
from app.resume_exports.renderers import ResumeExportRenderer
from app.resume_exports.renderers.models import RenderedResume
from app.resume_exports.schemas import ResumeExportFormat
from app.resumes.repository import ResumeRepository


class ResumeExportService:
    """
    Coordinates resume export workflows.

    The service owns export business logic while document rendering
    is delegated to format-specific renderer implementations.
    """

    def __init__(
        self,
        repository: ResumeRepository,
        pdf_renderer: ResumeExportRenderer,
        docx_renderer: ResumeExportRenderer,
    ) -> None:
        self.repository = repository
        self.pdf_renderer = pdf_renderer
        self.docx_renderer = docx_renderer

    def export_resume(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        export_format: ResumeExportFormat,
    ) -> RenderedResume:
        """
        Export a user's resume in the requested format.

        The service:
        1. Loads the complete resume export representation.
        2. Verifies resume ownership.
        3. Selects the appropriate concrete renderer.
        4. Delegates document generation to that renderer.
        5. Returns the complete rendered document result.
        """

        resume = self.repository.get_for_export(
            resume_id,
        )

        if resume is None or resume.user_id != user_id:
            raise ResumeExportNotFound(
                "Resume not found.",
            )

        renderer = self._get_renderer(
            export_format,
        )

        return renderer.render(
            resume,
        )

    def _get_renderer(
        self,
        export_format: ResumeExportFormat,
    ) -> ResumeExportRenderer:
        """
        Resolve the concrete renderer for the requested export format.
        """

        if export_format == ResumeExportFormat.PDF:
            return self.pdf_renderer

        if export_format == ResumeExportFormat.DOCX:
            return self.docx_renderer

        raise UnsupportedResumeExportFormat(
            f"Unsupported resume export format: {export_format}",
        )
