"""Add T090 output authorization policy persistence.

Revision ID: t090_output_auth
Revises: 8df2dd196803
Create Date: 2026-10-15 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

from oralia.infrastructure.db.ddl.t090_activity_policy_trigger import (
    CREATE_ACTIVITY_POLICY_TRIGGER_SQL,
    DROP_ACTIVITY_POLICY_TRIGGER_SQL,
)

revision: str = "t090_output_auth"
down_revision: str | Sequence[str] | None = "8df2dd196803"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add nullable policy and authorization-context columns without backfill."""

    op.add_column(
        "activity_configuration",
        sa.Column("output_authorization_policy_json", sa.Text(), nullable=True),
    )
    op.add_column(
        "activity_configuration",
        sa.Column("output_authorization_policy_sha256", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "verification_result",
        sa.Column("authorization_context", sa.JSON(), nullable=True),
    )
    op.execute(CREATE_ACTIVITY_POLICY_TRIGGER_SQL)


def downgrade() -> None:
    """Remove every column introduced by this revision."""

    op.execute(DROP_ACTIVITY_POLICY_TRIGGER_SQL)
    op.drop_column("verification_result", "authorization_context")
    op.drop_column("activity_configuration", "output_authorization_policy_sha256")
    op.drop_column("activity_configuration", "output_authorization_policy_json")
