from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.ai_usage.models import AIUsage
    from app.resumes.models import Resume


class CoverLetter(Base):
    __tablename__ = "cover_letters"

    resume_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "resumes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    job_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    resume: Mapped["Resume"] = relationship(
        "Resume",
        back_populates="cover_letters",
    )

    __table_args__ = (
        UniqueConstraint(
            "resume_id",
            "title",
            name="uq_cover_letter_resume_title",
        ),
    )

    ai_usage: Mapped[list["AIUsage"]] = relationship(
        "AIUsage",
        back_populates="cover_letter",
    )
