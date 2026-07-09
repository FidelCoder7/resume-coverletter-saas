from uuid import UUID

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

        return (
            self.db.query(Education)
            .filter(
                Education.id == education_id,
            )
            .first()
        )

    def list_by_resume(
        self,
        resume_id: UUID,
    ) -> list[Education]:
        """
        Return all education entries for a resume.
        """

        return (
            self.db.query(Education)
            .filter(
                Education.resume_id == resume_id,
            )
            .order_by(
                Education.display_order,
                Education.start_date.desc(),
            )
            .all()
        )

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
