from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, Text, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.skills.models import Skill

if TYPE_CHECKING:
    from app.certifications.models import Certification
    from app.educations.models import Education
    from app.experiences.models import Experience
    from app.projects.models import Project
    from app.users.models import User


class Resume(Base):
    __tablename__ = "resumes"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="resumes",
    )

    experiences: Mapped[list["Experience"]] = relationship(
        "Experience",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    educations: Mapped[list["Education"]] = relationship(
        "Education",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="Skill.display_order",
    )

    projects: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="Project.display_order",
    )

    certifications: Mapped[list["Certification"]] = relationship(
        "Certification",
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="Certification.display_order",
    )
