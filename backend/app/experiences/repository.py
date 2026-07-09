from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.experiences.models import Experience


class ExperienceRepository:
    """
    Repository for experience persistence.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        experience: Experience,
    ) -> Experience:
        self.db.add(experience)
        self.db.commit()
        self.db.refresh(experience)

        return experience

    def get_by_id(
        self,
        experience_id: UUID,
    ) -> Experience | None:
        statement = select(Experience).where(
            Experience.id == experience_id,
        )

        return self.db.scalar(statement)

    def list_by_resume(
        self,
        resume_id: UUID,
    ) -> list[Experience]:
        statement = (
            select(Experience)
            .where(
                Experience.resume_id == resume_id,
            )
            .order_by(
                Experience.display_order.asc(),
                Experience.created_at.asc(),
            )
        )

        return list(self.db.scalars(statement))

    def update(
        self,
        experience: Experience,
    ) -> Experience:
        self.db.commit()
        self.db.refresh(experience)

        return experience

    def delete(
        self,
        experience: Experience,
    ) -> None:
        self.db.delete(experience)
        self.db.commit()
