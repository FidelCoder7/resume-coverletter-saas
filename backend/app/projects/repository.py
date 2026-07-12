from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.projects.models import Project


class ProjectRepository:
    """
    Repository for project persistence.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        project: Project,
    ) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project

    def get_by_id(
        self,
        project_id: UUID,
    ) -> Project | None:
        statement = select(Project).where(
            Project.id == project_id,
        )

        return self.db.scalar(statement)

    def list_by_resume(
        self,
        resume_id: UUID,
    ) -> list[Project]:
        statement = (
            select(Project)
            .where(
                Project.resume_id == resume_id,
            )
            .order_by(
                Project.display_order.asc(),
                Project.created_at.asc(),
            )
        )

        return list(self.db.scalars(statement))

    def update(
        self,
        project: Project,
    ) -> Project:
        self.db.commit()
        self.db.refresh(project)

        return project

    def delete(
        self,
        project: Project,
    ) -> None:
        self.db.delete(project)
        self.db.commit()
