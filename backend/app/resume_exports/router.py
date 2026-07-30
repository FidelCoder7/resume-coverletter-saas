from uuid import UUID

from fastapi import APIRouter, Depends, Response

from app.auth.dependencies import get_current_user
from app.resume_exports.dependencies import get_resume_export_service
from app.resume_exports.schemas import ResumeExportFormat
from app.resume_exports.service import ResumeExportService
from app.users.models import User

router = APIRouter(
    prefix="/resumes",
    tags=["Resume Exports"],
)


@router.get(
    "/{resume_id}/export/pdf",
)
def export_resume_pdf(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ResumeExportService = Depends(
        get_resume_export_service,
    ),
) -> Response:
    """
    Export a user's resume as a PDF document.
    """

    rendered_resume = service.export_resume(
        user_id=current_user.id,
        resume_id=resume_id,
        export_format=ResumeExportFormat.PDF,
    )

    return Response(
        content=rendered_resume.content,
        media_type=rendered_resume.media_type,
        headers={
            "Content-Disposition": (
                f'attachment; filename="{rendered_resume.filename}"'
            ),
        },
    )


@router.get(
    "/{resume_id}/export/docx",
)
def export_resume_docx(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ResumeExportService = Depends(
        get_resume_export_service,
    ),
) -> Response:
    """
    Export a user's resume as a DOCX document.
    """

    rendered_resume = service.export_resume(
        user_id=current_user.id,
        resume_id=resume_id,
        export_format=ResumeExportFormat.DOCX,
    )

    return Response(
        content=rendered_resume.content,
        media_type=rendered_resume.media_type,
        headers={
            "Content-Disposition": (
                f'attachment; filename="{rendered_resume.filename}"'
            ),
        },
    )