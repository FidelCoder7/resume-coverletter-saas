from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.constants import (
    AIFeature,
    AIRequestStatus,
)
from app.database.base import Base
from app.database.enums import (
    ai_feature_enum,
    ai_request_status_enum,
)

if TYPE_CHECKING:
    from app.cover_letters.models import CoverLetter
    from app.resumes.models import Resume
    from app.users.models import User


class AIUsage(Base):
    """
    Audit record for every AI request executed by the platform.

    This entity is provider-agnostic and is designed to support
    telemetry, analytics, billing, subscription enforcement,
    and future reporting.
    """

    __tablename__ = "ai_usage"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    resume_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "resumes.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    cover_letter_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "cover_letters.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    feature: Mapped[AIFeature] = mapped_column(
        ai_feature_enum,
        nullable=False,
        index=True,
    )

    provider: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    prompt_version: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    prompt_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    completion_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    total_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    estimated_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(
            10,
            6,
        ),
        nullable=True,
    )

    latency_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[AIRequestStatus] = mapped_column(
        ai_request_status_enum,
        nullable=False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="ai_usage",
    )

    resume: Mapped["Resume | None"] = relationship(
        "Resume",
        back_populates="ai_usage",
    )

    cover_letter: Mapped["CoverLetter | None"] = relationship(
        "CoverLetter",
        back_populates="ai_usage",
    )

    __table_args__ = (
        Index(
            "ix_ai_usage_created_at",
            "created_at",
        ),
        Index(
            "ix_ai_usage_user_created_at",
            "user_id",
            "created_at",
        ),
        Index(
            "ix_ai_usage_feature_created_at",
            "feature",
            "created_at",
        ),
    )
