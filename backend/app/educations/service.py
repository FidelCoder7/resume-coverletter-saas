from datetime import date
from uuid import UUID

from app.common.constants import ResumeVersionSource
from app.educations.exceptions import (
    EducationAccessDenied,
    EducationNotFound,
)
from app.educations.models import Education
from app.educations.repository import EducationRepository
from app.resume_versions.service import ResumeVersionService
from app.resumes.repository import ResumeRepository


class EducationService:
    """
    Business logic for resume education management.
    """

    def __init__(
        self,
        repository: EducationRepository,
        resume_repository: ResumeRepository,
        resume_version_service: ResumeVersionService,
    ) -> None:
        self.repository = repository
        self.resume_repository = resume_repository
        self.resume_version_service = resume_version_service

    def _verify_resume_owner(
        self,
        *,
        resume_id: UUID,
        user_id: UUID,
    ):
        """
        Ensure the resume belongs to the authenticated user.
        """

        resume = self.resume_repository.get_by_id(
            resume_id,
        )

        if resume is None:
            raise EducationNotFound(
                "Resume not found.",
            )

        if resume.user_id != user_id:
            raise EducationAccessDenied(
                "You do not have permission to access this resume.",
            )

        return resume

    def create_education(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        institution: str,
        degree: str,
        field_of_study: str,
        location: str | None,
        grade: str | None,
        start_date: date,
        end_date: date | None,
        is_current: bool,
        description: str | None,
        display_order: int,
    ) -> Education:
        resume = self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        education = Education(
            resume_id=resume_id,
            institution=institution,
            degree=degree,
            field_of_study=field_of_study,
            location=location,
            grade=grade,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current,
            description=description,
            display_order=display_order,
        )

        education = self.repository.create(
            education,
        )

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.USER,
            change_summary="Education added to resume.",
        )

        self.repository.db.commit()
        self.repository.db.refresh(education)

        return education

    def list_educations(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
    ) -> list[Education]:
        self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        return self.repository.list_by_resume(
            resume_id,
        )

    def get_education(
        self,
        *,
        user_id: UUID,
        education_id: UUID,
    ) -> Education:
        education = self.repository.get_by_id(
            education_id,
        )

        if education is None:
            raise EducationNotFound(
                "Education not found.",
            )

        self._verify_resume_owner(
            resume_id=education.resume_id,
            user_id=user_id,
        )

        return education

    def update_education(
        self,
        *,
        user_id: UUID,
        education_id: UUID,
        institution: str,
        degree: str,
        field_of_study: str,
        location: str | None,
        grade: str | None,
        start_date: date,
        end_date: date | None,
        is_current: bool,
        description: str | None,
        display_order: int,
    ) -> Education:
        education = self.get_education(
            user_id=user_id,
            education_id=education_id,
        )

        education.institution = institution
        education.degree = degree
        education.field_of_study = field_of_study
        education.location = location
        education.grade = grade
        education.start_date = start_date
        education.end_date = end_date
        education.is_current = is_current
        education.description = description
        education.display_order = display_order

        education = self.repository.update(
            education,
        )

        resume = self._verify_resume_owner(
            resume_id=education.resume_id,
            user_id=user_id,
        )

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.USER,
            change_summary="Education updated on resume.",
        )

        self.repository.db.commit()
        self.repository.db.refresh(education)

        return education

    def delete_education(
        self,
        *,
        user_id: UUID,
        education_id: UUID,
    ) -> None:
        education = self.get_education(
            user_id=user_id,
            education_id=education_id,
        )

        resume = self._verify_resume_owner(
            resume_id=education.resume_id,
            user_id=user_id,
        )

        self.repository.delete(
            education,
        )

        self.resume_version_service.create_version_from_resume(
            resume=resume,
            source=ResumeVersionSource.USER,
            change_summary="Education removed from resume.",
        )

        self.repository.db.commit()
