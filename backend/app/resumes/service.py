from uuid import UUID

from app.resumes.exceptions import (
    ResumeAccessDenied,
    ResumeNotFound,
)
from app.resumes.models import Resume
from app.resumes.repository import ResumeRepository


class ResumeService:
    """
    Business logic for resume management.
    """

    def __init__(
        self,
        repository: ResumeRepository,
    ):
        self.repository = repository

    def create_resume(
        self,
        *,
        user_id: UUID,
        title: str,
        summary: str | None,
    ) -> Resume:
        resume = Resume(
            user_id=user_id,
            title=title,
            summary=summary,
        )

        return self.repository.create(resume)

    def list_resumes(
        self,
        user_id: UUID,
    ) -> list[Resume]:
        return self.repository.list_by_user(user_id)

    def get_resume(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
    ) -> Resume:
        resume = self.repository.get_by_id(resume_id)

        if resume is None:
            raise ResumeNotFound("Resume not found.")

        if resume.user_id != user_id:
            raise ResumeAccessDenied(
                "You do not have permission to access this resume."
            )

        return resume

    def update_resume(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        title: str,
        summary: str | None,
    ) -> Resume:
        resume = self.get_resume(
            user_id=user_id,
            resume_id=resume_id,
        )

        resume.title = title
        resume.summary = summary

        return self.repository.update(resume)

    def delete_resume(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
    ) -> None:
        resume = self.get_resume(
            user_id=user_id,
            resume_id=resume_id,
        )

        self.repository.delete(resume)
