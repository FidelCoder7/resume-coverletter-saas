"""add_generated_resume_fields

Revision ID: b5da2fea84f3
Revises: 6c7718072769
Create Date: 2026-07-15 11:49:40.203769
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b5da2fea84f3"
down_revision: Union[str, Sequence[str], None] = "6c7718072769"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "resumes",
        sa.Column(
            "generated_content",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "resumes",
        sa.Column(
            "generated_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "resumes",
        "generated_at",
    )

    op.drop_column(
        "resumes",
        "generated_content",
    )
