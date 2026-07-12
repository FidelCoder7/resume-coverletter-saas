from datetime import date
from uuid import UUID

from app.projects.exceptions import (
    InvalidProjectDate,
    ProjectAccessDenied,
    ProjectNotFound,
)
from app.projects.models import Project
from app.projects.repository import ProjectRepository
from app.resumes.repository import ResumeRepository


class ProjectService:
    """
    Business logic for resume project management.
    """

    def __init__(
        self,
        repository: ProjectRepository,
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
            raise ProjectNotFound(
                "Resume not found.",
            )

        if resume.user_id != user_id:
            raise ProjectAccessDenied(
                "You do not have permission to modify this resume.",
            )

        return resume

    def _validate_dates(
        self,
        *,
        start_date: date | None,
        end_date: date | None,
        is_ongoing: bool,
    ) -> None:
        """
        Validate project date business rules.
        """

        if is_ongoing and end_date is not None:
            raise InvalidProjectDate(
                "Ongoing projects cannot have an end date.",
            )

        if start_date is not None and end_date is not None and end_date < start_date:
            raise InvalidProjectDate(
                "End date cannot be earlier than start date.",
            )

    def create_project(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
        name: str,
        description: str,
        technologies: str,
        project_url: str | None,
        repository_url: str | None,
        start_date: date | None,
        end_date: date | None,
        is_ongoing: bool,
        display_order: int,
    ) -> Project:
        self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        self._validate_dates(
            start_date=start_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
        )

        project = Project(
            resume_id=resume_id,
            name=name,
            description=description,
            technologies=technologies,
            project_url=project_url,
            repository_url=repository_url,
            start_date=start_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
            display_order=display_order,
        )

        return self.repository.create(
            project,
        )

    def list_projects(
        self,
        *,
        user_id: UUID,
        resume_id: UUID,
    ) -> list[Project]:
        self._verify_resume_owner(
            resume_id=resume_id,
            user_id=user_id,
        )

        return self.repository.list_by_resume(
            resume_id,
        )

    def get_project(
        self,
        *,
        user_id: UUID,
        project_id: UUID,
    ) -> Project:
        project = self.repository.get_by_id(
            project_id,
        )

        if project is None:
            raise ProjectNotFound(
                "Project not found.",
            )

        self._verify_resume_owner(
            resume_id=project.resume_id,
            user_id=user_id,
        )

        return project

    def update_project(
        self,
        *,
        user_id: UUID,
        project_id: UUID,
        name: str,
        description: str,
        technologies: str,
        project_url: str | None,
        repository_url: str | None,
        start_date: date | None,
        end_date: date | None,
        is_ongoing: bool,
        display_order: int,
    ) -> Project:
        project = self.get_project(
            user_id=user_id,
            project_id=project_id,
        )

        self._validate_dates(
            start_date=start_date,
            end_date=end_date,
            is_ongoing=is_ongoing,
        )

        project.name = name
        project.description = description
        project.technologies = technologies
        project.project_url = project_url
        project.repository_url = repository_url
        project.start_date = start_date
        project.end_date = end_date
        project.is_ongoing = is_ongoing
        project.display_order = display_order

        return self.repository.update(
            project,
        )

    def delete_project(
        self,
        *,
        user_id: UUID,
        project_id: UUID,
    ) -> None:
        project = self.get_project(
            user_id=user_id,
            project_id=project_id,
        )

        self.repository.delete(
            project,
        )
