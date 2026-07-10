"""create skills table

Revision ID: 043d5d690ef3
Revises: a49560fad820
Create Date: 2026-07-10 12:48:26.796353

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
from app.database.enums import skill_level_enum

# revision identifiers, used by Alembic.
revision: str = "043d5d690ef3"
down_revision: Union[str, Sequence[str], None] = "a49560fad820"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "skills",
        sa.Column("resume_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("proficiency", skill_level_enum, nullable=False),
        sa.Column(
            "display_order",
            sa.Integer(),
            server_default="0",
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resumes.id"],
            name=op.f("fk_skills_resume_id_resumes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_skills"),
        ),
        sa.UniqueConstraint(
            "resume_id",
            "name",
            name="uq_skill_resume_name",
        ),
    )

    op.create_index(
        op.f("ix_skills_resume_id"),
        "skills",
        ["resume_id"],
        unique=False,
    )

    op.create_index(
        "ix_skills_resume_order",
        "skills",
        ["resume_id", "display_order"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_skills_resume_order",
        table_name="skills",
    )

    op.drop_index(
        op.f("ix_skills_resume_id"),
        table_name="skills",
    )

    op.drop_table("skills")
