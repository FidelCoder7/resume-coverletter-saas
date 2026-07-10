from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.skills.models import Skill


class SkillRepository:
    """
    Repository for skill persistence.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        skill: Skill,
    ) -> Skill:
        self.db.add(skill)
        self.db.commit()
        self.db.refresh(skill)

        return skill

    def get_by_id(
        self,
        skill_id: UUID,
    ) -> Skill | None:
        statement = select(Skill).where(
            Skill.id == skill_id,
        )

        return self.db.scalar(statement)

    def list_by_resume(
        self,
        resume_id: UUID,
    ) -> list[Skill]:
        statement = (
            select(Skill)
            .where(
                Skill.resume_id == resume_id,
            )
            .order_by(
                Skill.display_order.asc(),
                Skill.created_at.asc(),
            )
        )

        return list(self.db.scalars(statement))

    def update(
        self,
        skill: Skill,
    ) -> Skill:
        self.db.commit()
        self.db.refresh(skill)

        return skill

    def delete(
        self,
        skill: Skill,
    ) -> None:
        self.db.delete(skill)
        self.db.commit()
