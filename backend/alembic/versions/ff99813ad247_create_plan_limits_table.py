"""create plan limits table

Revision ID: ff99813ad247
Revises: bf5055634aed
Create Date: 2026-07-24 21:55:49.165455

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ff99813ad247"
down_revision: Union[str, Sequence[str], None] = "bf5055634aed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    subscription_plan_enum = postgresql.ENUM(
        "free",
        "pro",
        name="subscription_plan",
        create_type=False,
    )

    ai_feature_enum = postgresql.ENUM(
        "cover_letter_generation",
        "cover_letter_regeneration",
        "resume_generation",
        "ats_optimization",
        name="ai_feature",
        create_type=False,
    )

    subscription_limit_period_enum = postgresql.ENUM(
        "monthly",
        name="subscription_limit_period",
        create_type=True,
    )

    op.create_table(
        "plan_limits",
        sa.Column(
            "subscription_plan",
            subscription_plan_enum,
            nullable=False,
        ),
        sa.Column(
            "feature",
            ai_feature_enum,
            nullable=False,
        ),
        sa.Column(
            "limit_value",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "period",
            subscription_limit_period_enum,
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_plan_limits"),
        ),
        sa.UniqueConstraint(
            "subscription_plan",
            "feature",
            "period",
            name="uq_plan_limit_plan_feature_period",
        ),
    )

    op.create_index(
        "ix_plan_limits_feature",
        "plan_limits",
        ["feature"],
        unique=False,
    )

    op.create_index(
        "ix_plan_limits_plan_period",
        "plan_limits",
        ["subscription_plan", "period"],
        unique=False,
    )

    op.create_index(
        "ix_plan_limits_subscription_plan",
        "plan_limits",
        ["subscription_plan"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_plan_limits_subscription_plan",
        table_name="plan_limits",
    )

    op.drop_index(
        "ix_plan_limits_plan_period",
        table_name="plan_limits",
    )

    op.drop_index(
        "ix_plan_limits_feature",
        table_name="plan_limits",
    )

    op.drop_table(
        "plan_limits",
    )