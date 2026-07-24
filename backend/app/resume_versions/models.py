from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.constants import ResumeVersionSource
from app.database.base import Base
from app.database.enums import resume_version_source_enum

if TYPE_CHECKING:
    from app.resumes.models import Resume


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    resume_id: Mapped[UUID] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
    )

    version_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    snapshot: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    change_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    source: Mapped[ResumeVersionSource] = mapped_column(
        resume_version_source_enum,
        nullable=False,
    )

    resume: Mapped["Resume"] = relationship(
        "Resume",
        back_populates="versions",
    )

    __table_args__ = (
        UniqueConstraint(
            "resume_id",
            "version_number",
            name="uq_resume_version_number",
        ),
        Index(
            "ix_resume_versions_resume_id_version_number",
            "resume_id",
            "version_number",
        ),
    )
