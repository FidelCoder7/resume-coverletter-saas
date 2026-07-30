from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.resumes.models import Resume


class ResumeRepository:
    """
    Repository for resume persistence.

    Repositories do not commit transactions.
    Transaction ownership belongs to the service layer.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        resume: Resume,
    ) -> Resume:
        self.db.add(resume)
        self.db.flush()
        self.db.refresh(resume)

        return resume

    def create_without_commit(
        self,
        resume: Resume,
    ) -> Resume:
        """
        Add a resume to the current transaction without committing.

        Used by workflows that persist a resume together with related
        records and version history as one atomic transaction.
        """

        self.db.add(resume)
        self.db.flush()

        return resume

    def get_by_id(
        self,
        resume_id: UUID,
    ) -> Resume | None:
        statement = select(Resume).where(
            Resume.id == resume_id,
        )

        return self.db.scalar(statement)

    def get_for_generation(
        self,
        resume_id: UUID,
    ) -> Resume | None:
        """
        Return a resume with all related resume content eagerly loaded.
        """

        statement = (
            select(Resume)
            .options(
                selectinload(Resume.experiences),
                selectinload(Resume.educations),
                selectinload(Resume.skills),
                selectinload(Resume.projects),
                selectinload(Resume.certifications),
            )
            .where(
                Resume.id == resume_id,
            )
        )

        return self.db.scalar(statement)


    def get_for_export(
            self,
            resume_id: UUID,
        ) -> Resume | None:
            """
            Return a resume with all persisted resume content eagerly loaded.
    
            This is the dedicated loading boundary for export workflows.
            The returned resume contains all child collections required to
            render a complete export without relying on lazy loading after
            the database session boundary.
            """
    
            statement = (
                select(Resume)
                .options(
                    selectinload(Resume.experiences),
                    selectinload(Resume.educations),
                    selectinload(Resume.skills),
                    selectinload(Resume.projects),
                    selectinload(Resume.certifications),
                )
                .where(
                    Resume.id == resume_id,
                )
            )
    
            return self.db.scalar(statement)

    def get_for_restore(
        self,
        resume_id: UUID,
    ) -> Resume | None:
        """
        Return a resume with all child collections eagerly loaded.

        This ensures the restore workflow can replace the complete
        resume state inside one database transaction.
        """

        statement = (
            select(Resume)
            .options(
                selectinload(Resume.experiences),
                selectinload(Resume.educations),
                selectinload(Resume.skills),
                selectinload(Resume.projects),
                selectinload(Resume.certifications),
            )
            .where(
                Resume.id == resume_id,
            )
        )

        return self.db.scalar(statement)


    

    def list_by_user(
        self,
        user_id: UUID,
    ) -> list[Resume]:
        statement = (
            select(Resume)
            .where(
                Resume.user_id == user_id,
            )
            .order_by(
                Resume.created_at.desc(),
            )
        )

        return list(self.db.scalars(statement))

    def update(
        self,
        resume: Resume,
    ) -> Resume:
        self.db.flush()
        self.db.refresh(resume)

        return resume

    def delete(
        self,
        resume: Resume,
    ) -> None:
        self.db.delete(resume)
        self.db.flush()

    def get_default_for_user(
        self,
        user_id: UUID,
    ) -> Resume | None:
        statement = select(Resume).where(
            Resume.user_id == user_id,
            Resume.is_default.is_(True),
        )

        return self.db.scalar(statement)
