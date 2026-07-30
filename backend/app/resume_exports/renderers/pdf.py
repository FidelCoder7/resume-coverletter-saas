from io import BytesIO

from weasyprint import HTML

from app.resume_exports.renderers.base import ResumeExportRenderer
from app.resume_exports.renderers.models import RenderedResume
from app.resume_exports.templates.pdf import render_resume_html
from app.resumes.models import Resume


class PdfResumeRenderer(ResumeExportRenderer):
    """
    Render a complete resume as a PDF document.

    The renderer receives a fully loaded Resume entity and converts
    it into HTML before generating the final PDF document.
    """

    @property
    def media_type(self) -> str:
        return "application/pdf"

    @property
    def file_extension(self) -> str:
        return "pdf"

    def render(
        self,
        resume: Resume,
    ) -> RenderedResume:
        html_content = render_resume_html(
            resume,
        )

        pdf_buffer = BytesIO()

        HTML(
            string=html_content,
        ).write_pdf(
            pdf_buffer,
        )

        return RenderedResume(
            content=pdf_buffer.getvalue(),
            filename=self._build_filename(resume),
            media_type=self.media_type,
        )

    def _build_filename(
        self,
        resume: Resume,
    ) -> str:
        filename = resume.title.strip()

        if not filename:
            filename = "resume"

        sanitized = "".join(
            character
            if character.isalnum() or character in {" ", "-", "_"}
            else "_"
            for character in filename
        )

        sanitized = "_".join(
            sanitized.split(),
        )

        return f"{sanitized}.pdf"