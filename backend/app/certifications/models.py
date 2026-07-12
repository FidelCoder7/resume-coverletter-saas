from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.resumes.models import Resume


class Certification(Base):
    __tablename__ = "certifications"

    resume_id: Mapped[UUID] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    issuing_organization: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    credential_id: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    credential_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    issue_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    expiration_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    does_not_expire: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    resume: Mapped["Resume"] = relationship(
        "Resume",
        back_populates="certifications",
    )

    __table_args__ = (
        UniqueConstraint(
            "resume_id",
            "name",
            name="uq_certification_resume_name",
        ),
    )
