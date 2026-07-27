"""seed initial plan limits

Revision ID: e2dc1777fba6
Revises: ff99813ad247
Create Date: 2026-07-27 15:42:22.137898

"""

from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e2dc1777fba6"
down_revision: Union[str, Sequence[str], None] = "ff99813ad247"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed the initial subscription plan limits."""

    plan_limits_table = sa.table(
        "plan_limits",
        sa.column(
            "id",
            sa.UUID(),
        ),
        sa.column(
            "subscription_plan",
            sa.Enum(
                "FREE",
                "PRO",
                name="subscription_plan",
                create_type=False,
            ),
        ),
        sa.column(
            "feature",
            sa.Enum(
                "COVER_LETTER_GENERATION",
                "COVER_LETTER_REGENERATION",
                "RESUME_GENERATION",
                "ATS_OPTIMIZATION",
                name="ai_feature",
                create_type=False,
            ),
        ),
        sa.column(
            "limit_value",
            sa.Integer(),
        ),
        sa.column(
            "period",
            sa.Enum(
                "monthly",
                name="subscription_limit_period",
                create_type=False,
            ),
        ),
    )
    op.bulk_insert(
        plan_limits_table,
        [
            {
                "id": uuid4(),
                "subscription_plan": "FREE",
                "feature": "RESUME_GENERATION",
                "limit_value": 3,
                "period": "monthly",
            },
            {
                "id": uuid4(),
                "subscription_plan": "FREE",
                "feature": "COVER_LETTER_GENERATION",
                "limit_value": 3,
                "period": "monthly",
            },
            {
                "id": uuid4(),
                "subscription_plan": "FREE",
                "feature": "COVER_LETTER_REGENERATION",
                "limit_value": 1,
                "period": "monthly",
            },
            {
                "id": uuid4(),
                "subscription_plan": "FREE",
                "feature": "ATS_OPTIMIZATION",
                "limit_value": 1,
                "period": "monthly",
            },
            {
                "id": uuid4(),
                "subscription_plan": "PRO",
                "feature": "RESUME_GENERATION",
                "limit_value": 10,
                "period": "monthly",
            },
            {
                "id": uuid4(),
                "subscription_plan": "PRO",
                "feature": "COVER_LETTER_GENERATION",
                "limit_value": 10,
                "period": "monthly",
            },
            {
                "id": uuid4(),
                "subscription_plan": "PRO",
                "feature": "COVER_LETTER_REGENERATION",
                "limit_value": 5,
                "period": "monthly",
            },
            {
                "id": uuid4(),
                "subscription_plan": "PRO",
                "feature": "ATS_OPTIMIZATION",
                "limit_value": 5,
                "period": "monthly",
            },
        ],
    )


def downgrade() -> None:
    """Remove the initial subscription plan limits."""

    plan_limits_table = sa.table(
        "plan_limits",
        sa.column("id", sa.UUID()),
        sa.column(
            "subscription_plan",
            sa.Enum(
                "FREE",
                "PRO",
                name="subscription_plan",
                create_type=False,
            ),
        ),
        sa.column(
            "feature",
            sa.Enum(
                "COVER_LETTER_GENERATION",
                "COVER_LETTER_REGENERATION",
                "RESUME_GENERATION",
                "ATS_OPTIMIZATION",
                name="ai_feature",
                create_type=False,
            ),
        ),
        sa.column(
            "period",
            sa.Enum(
                "monthly",
                name="subscription_limit_period",
                create_type=False,
            ),
        ),
    )

    op.execute(
        plan_limits_table.delete().where(
            sa.tuple_(
                plan_limits_table.c.subscription_plan,
                plan_limits_table.c.feature,
                plan_limits_table.c.period,
            ).in_(
                [
                    ("FREE", "RESUME_GENERATION", "monthly"),
                    ("FREE", "COVER_LETTER_GENERATION", "monthly"),
                    ("FREE", "COVER_LETTER_REGENERATION", "monthly"),
                    ("FREE", "ATS_OPTIMIZATION", "monthly"),
                    ("PRO", "RESUME_GENERATION", "monthly"),
                    ("PRO", "COVER_LETTER_GENERATION", "monthly"),
                    ("PRO", "COVER_LETTER_REGENERATION", "monthly"),
                    ("PRO", "ATS_OPTIMIZATION", "monthly"),
                ],
            ),
        ),
    )
