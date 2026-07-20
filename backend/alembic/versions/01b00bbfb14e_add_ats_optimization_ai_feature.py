"""add ats optimization ai feature

Revision ID: 01b00bbfb14e
Revises: b5da2fea84f3
Create Date: 2026-07-20 18:55:56.487266

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "01b00bbfb14e"
down_revision: Union[str, Sequence[str], None] = "b5da2fea84f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TYPE ai_feature
        ADD VALUE IF NOT EXISTS 'ATS_OPTIMIZATION';
        """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
