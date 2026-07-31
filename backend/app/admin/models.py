from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.constants import AdminAuditAction
from app.database.base import Base
from app.database.enums import admin_audit_action_enum

if TYPE_CHECKING:
    from app.users.models import User


class AdminAuditLog(Base):
    """
    Immutable audit record for an administrative action.

    Each record identifies:
    - the administrator who performed the action,
    - the user affected by the action,
    - the administrative action performed,
    - an optional reason,
    - optional structured metadata.
    """

    __tablename__ = "admin_audit_logs"

    # ------------------------------------------------------------------
    # Administrator
    # ------------------------------------------------------------------

    admin_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    admin: Mapped["User"] = relationship(
        "User",
        foreign_keys=[admin_id],
    )

    # ------------------------------------------------------------------
    # Target User
    # ------------------------------------------------------------------

    target_user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    target_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[target_user_id],
    )

    # ------------------------------------------------------------------
    # Action
    # ------------------------------------------------------------------

    action: Mapped[AdminAuditAction] = mapped_column(
        admin_audit_action_enum,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Context
    # ------------------------------------------------------------------

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    event_metadata: Mapped[dict | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Indexes
    # ------------------------------------------------------------------

    __table_args__ = (
        Index(
            "ix_admin_audit_logs_admin_id",
            "admin_id",
        ),
        Index(
            "ix_admin_audit_logs_target_user_id",
            "target_user_id",
        ),
        Index(
            "ix_admin_audit_logs_action",
            "action",
        ),
        Index(
            "ix_admin_audit_logs_created_at",
            "created_at",
        ),
        Index(
            "ix_admin_audit_logs_target_user_created_at",
            "target_user_id",
            "created_at",
        ),
    )
