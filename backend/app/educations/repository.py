from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.educations.models import Education


class EducationRepository:
    """
    Data access layer for education records.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        education: Education,
    ) -> Education:
        """
        Persist an education record.
        """

        self.db.add(education)
        self.db.commit()
        self.db.refresh(education)

        return education

    def get_by_id(
        self,
        education_id: UUID,
    ) -> Education | None:
        """
        Return an education by its ID.
        """

        statement = select(Education).where(
            Education.id == education_id,
        )

        return self.db.scalar(statement)

    def list_by_resume(
        self,
        resume_id: UUID,
    ) -> list[Education]:
        """
        Return all education entries for a resume.
        """

        statement = (
            select(Education)
            .where(
                Education.resume_id == resume_id,
            )
            .order_by(
                Education.display_order.asc(),
                Education.start_date.desc(),
            )
        )

        return list(self.db.scalars(statement))

    def update(
        self,
        education: Education,
    ) -> Education:
        """
        Persist updates to an education.
        """

        self.db.commit()
        self.db.refresh(education)

        return education

    def delete(
        self,
        education: Education,
    ) -> None:
        """
        Delete an education.
        """

        self.db.delete(education)
        self.db.commit()
