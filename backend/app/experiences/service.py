from datetime import date
from uuid import UUID

from app.experiences.exceptions import (
    ExperienceAccessDenied,
    ExperienceNotFound,
)
from app.experiences.models import Experience
from app.experiences.repository import ExperienceRepository
from app.resumes.repository import ResumeRepository


class ExperienceService:
    """
    Business logic for resume experience management.
    """

    def __init__(
        self,
        repository: ExperienceRepository,
        resume_repository: ResumeRepository,
    ):
        self.repository = repository
        self.resume_repository = resume_repository

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
            raise ExperienceNotFound(
                "Resume not found.",
            )

        if resume.user_id != user_id:
            raise ExperienceAccessDenied(
                "You do not have permission to access this resume.",
            )

        return resume

    def create_experience(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        company: str,
        job_title: str,
        location: str | None,
        employment_type,
        start_date: date,
        end_date: date | None,
        is_current: bool,
        description: str | None,
        display_order: int,
    ) -> Experience:
        self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        experience = Experience(
            resume_id=resume_id,
            company=company,
            job_title=job_title,
            location=location,
            employment_type=employment_type,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current,
            description=description,
            display_order=display_order,
        )

        return self.repository.create(
            experience,
        )

    def list_experiences(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
    ) -> list[Experience]:
        self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        return self.repository.list_by_resume(
            resume_id,
        )

    def get_experience(
        self,
        *,
        user_id: UUID,
        experience_id: UUID,
    ) -> Experience:
        experience = self.repository.get_by_id(
            experience_id,
        )

        if experience is None:
            raise ExperienceNotFound(
                "Experience not found.",
            )

        self._verify_resume_owner(
            resume_id=experience.resume_id,
            user_id=user_id,
        )

        return experience

    def update_experience(
        self,
        *,
        user_id: UUID,
        experience_id: UUID,
        company: str,
        job_title: str,
        location: str | None,
        employment_type,
        start_date: date,
        end_date: date | None,
        is_current: bool,
        description: str | None,
        display_order: int,
    ) -> Experience:
        experience = self.get_experience(
            user_id=user_id,
            experience_id=experience_id,
        )

        experience.company = company
        experience.job_title = job_title
        experience.location = location
        experience.employment_type = employment_type
        experience.start_date = start_date
        experience.end_date = end_date
        experience.is_current = is_current
        experience.description = description
        experience.display_order = display_order

        return self.repository.update(
            experience,
        )

    def delete_experience(
        self,
        *,
        user_id: UUID,
        experience_id: UUID,
    ) -> None:
        experience = self.get_experience(
            user_id=user_id,
            experience_id=experience_id,
        )

        self.repository.delete(
            experience,
        )
