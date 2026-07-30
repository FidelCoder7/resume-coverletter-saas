"""create payment transactions table

Revision ID: 7c015b0ea6fc
Revises: e2dc1777fba6
Create Date: 2026-07-28 10:43:25.751590

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7c015b0ea6fc"
down_revision: Union[str, Sequence[str], None] = "e2dc1777fba6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create payment transactions table."""

    bind = op.get_bind()

    # ------------------------------------------------------------------
    # Create billing-specific PostgreSQL enum types.
    #
    # These types are created explicitly before the table.
    # checkfirst=True prevents failure if a previous partial migration
    # attempt already created one of them.
    # ------------------------------------------------------------------

    billing_transaction_type_enum = postgresql.ENUM(
        "subscription_purchase",
        "subscription_renewal",
        "subscription_upgrade",
        "subscription_downgrade",
        name="billing_transaction_type",
    )

    payment_provider_enum = postgresql.ENUM(
        "pesapal",
        name="payment_provider",
    )

    payment_method_enum = postgresql.ENUM(
        "mpesa",
        "card",
        "bank",
        "other",
        name="payment_method",
    )

    payment_status_enum = postgresql.ENUM(
        "pending",
        "completed",
        "failed",
        "cancelled",
        "expired",
        name="payment_status",
    )

    billing_transaction_type_enum.create(
        bind,
        checkfirst=True,
    )

    payment_provider_enum.create(
        bind,
        checkfirst=True,
    )

    payment_method_enum.create(
        bind,
        checkfirst=True,
    )

    payment_status_enum.create(
        bind,
        checkfirst=True,
    )

    # ------------------------------------------------------------------
    # Define enum references for table columns.
    #
    # create_type=False is critical here.
    #
    # The enum types have already been created explicitly above.
    # SQLAlchemy must therefore NOT attempt to create them again when
    # op.create_table() is executed.
    # ------------------------------------------------------------------

    billing_transaction_type_column_enum = postgresql.ENUM(
        "subscription_purchase",
        "subscription_renewal",
        "subscription_upgrade",
        "subscription_downgrade",
        name="billing_transaction_type",
        create_type=False,
    )

    payment_provider_column_enum = postgresql.ENUM(
        "pesapal",
        name="payment_provider",
        create_type=False,
    )

    payment_method_column_enum = postgresql.ENUM(
        "mpesa",
        "card",
        "bank",
        "other",
        name="payment_method",
        create_type=False,
    )

    payment_status_column_enum = postgresql.ENUM(
        "pending",
        "completed",
        "failed",
        "cancelled",
        "expired",
        name="payment_status",
        create_type=False,
    )

    # subscription_plan is an existing shared PostgreSQL enum.
    #
    # It was created by an earlier migration and must never be created
    # or dropped by this migration.
    subscription_plan_enum = postgresql.ENUM(
        "FREE",
        "PRO",
        name="subscription_plan",
        create_type=False,
    )

    # ------------------------------------------------------------------
    # Create payment transactions table.
    # ------------------------------------------------------------------

    op.create_table(
        "payment_transactions",
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "subscription_plan",
            subscription_plan_enum,
            nullable=False,
        ),
        sa.Column(
            "transaction_type",
            billing_transaction_type_column_enum,
            nullable=False,
        ),
        sa.Column(
            "provider",
            payment_provider_column_enum,
            nullable=False,
        ),
        sa.Column(
            "provider_order_id",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "provider_transaction_id",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "amount",
            sa.Numeric(
                precision=12,
                scale=2,
            ),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(length=3),
            nullable=False,
        ),
        sa.Column(
            "payment_method",
            payment_method_column_enum,
            nullable=True,
        ),
        sa.Column(
            "status",
            payment_status_column_enum,
            nullable=False,
        ),
        sa.Column(
            "failure_reason",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "provider_response",
            postgresql.JSONB(
                astext_type=sa.Text(),
            ),
            nullable=True,
        ),
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
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
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f(
                "fk_payment_transactions_user_id_users",
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f(
                "pk_payment_transactions",
            ),
        ),
        sa.UniqueConstraint(
            "provider",
            "provider_order_id",
            name="uq_payment_transactions_provider_order_id",
        ),
    )

    # ------------------------------------------------------------------
    # Indexes
    # ------------------------------------------------------------------

    op.create_index(
        "ix_payment_transactions_provider_transaction_id",
        "payment_transactions",
        ["provider", "provider_transaction_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_payment_transactions_user_id"),
        "payment_transactions",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        "ix_payment_transactions_user_status",
        "payment_transactions",
        ["user_id", "status"],
        unique=False,
    )


def downgrade() -> None:
    """Drop payment transactions table and billing enum types."""

    bind = op.get_bind()

    # ------------------------------------------------------------------
    # Drop indexes
    # ------------------------------------------------------------------

    op.drop_index(
        "ix_payment_transactions_user_status",
        table_name="payment_transactions",
    )

    op.drop_index(
        op.f("ix_payment_transactions_user_id"),
        table_name="payment_transactions",
    )

    op.drop_index(
        "ix_payment_transactions_provider_transaction_id",
        table_name="payment_transactions",
    )

    # ------------------------------------------------------------------
    # Drop table
    # ------------------------------------------------------------------

    op.drop_table(
        "payment_transactions",
    )

    # ------------------------------------------------------------------
    # Drop billing-specific enum types.
    #
    # subscription_plan is intentionally NOT dropped because it is
    # shared with the existing users/subscriptions schema.
    # ------------------------------------------------------------------

    payment_status_enum = postgresql.ENUM(
        "pending",
        "completed",
        "failed",
        "cancelled",
        "expired",
        name="payment_status",
    )

    payment_method_enum = postgresql.ENUM(
        "mpesa",
        "card",
        "bank",
        "other",
        name="payment_method",
    )

    payment_provider_enum = postgresql.ENUM(
        "pesapal",
        name="payment_provider",
    )

    billing_transaction_type_enum = postgresql.ENUM(
        "subscription_purchase",
        "subscription_renewal",
        "subscription_upgrade",
        "subscription_downgrade",
        name="billing_transaction_type",
    )

    payment_status_enum.drop(
        bind,
        checkfirst=True,
    )

    payment_method_enum.drop(
        bind,
        checkfirst=True,
    )

    payment_provider_enum.drop(
        bind,
        checkfirst=True,
    )

    billing_transaction_type_enum.drop(
        bind,
        checkfirst=True,
    )
