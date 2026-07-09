from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.resumes.models import Resume


class ResumeRepository:
    """
    Repository for resume persistence.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        resume: Resume,
    ) -> Resume:
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)

        return resume

    def get_by_id(
        self,
        resume_id: UUID,
    ) -> Resume | None:
        statement = select(Resume).where(
            Resume.id == resume_id,
        )

        return self.db.scalar(statement)

    def list_by_user(
        self,
        user_id: UUID,
    ) -> list[Resume]:
        statement = (
            select(Resume)
            .where(Resume.user_id == user_id)
            .order_by(Resume.created_at.desc())
        )

        return list(self.db.scalars(statement))

    def update(
        self,
        resume: Resume,
    ) -> Resume:
        self.db.commit()
        self.db.refresh(resume)

        return resume

    def delete(
        self,
        resume: Resume,
    ) -> None:
        self.db.delete(resume)
        self.db.commit()

    def get_default_for_user(
        self,
        user_id: UUID,
    ) -> Resume | None:
        statement = select(Resume).where(
            Resume.user_id == user_id,
            Resume.is_default.is_(True),
        )

        return self.db.scalar(statement)
