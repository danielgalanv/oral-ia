"""Add explicit self-study retention authorization.

Revision ID: t114_retention_auth
Revises: t090_output_auth
Create Date: 2026-10-16 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "t114_retention_auth"
down_revision: str | Sequence[str] | None = "t090_output_auth"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "self_study_activity_config",
        sa.Column("retention_authorized", sa.Boolean(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("self_study_activity_config", "retention_authorized")
