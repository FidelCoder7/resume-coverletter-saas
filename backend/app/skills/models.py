from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.constants import SkillLevel
from app.database.base import Base
from app.database.enums import skill_level_enum

if TYPE_CHECKING:
    from app.resumes.models import Resume


class Skill(Base):
    __tablename__ = "skills"

    resume_id: Mapped[UUID] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    proficiency: Mapped[SkillLevel] = mapped_column(
        skill_level_enum,
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
        nullable=False,
    )

    resume: Mapped["Resume"] = relationship(
        "Resume",
        back_populates="skills",
    )

    __table_args__ = (
        UniqueConstraint(
            "resume_id",
            "name",
            name="uq_skill_resume_name",
        ),
        Index(
            "ix_skills_resume_order",
            "resume_id",
            "display_order",
        ),
    )
