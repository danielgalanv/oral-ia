"""Complete clean-install schema for the existing material index rebuild lock.

Revision ID: t007_demo_install
Revises: t005_governance
"""

import sqlalchemy as sa
from alembic import op

revision = "t007_demo_install"
down_revision = "t005_governance"
branch_labels = None
depends_on = None


def upgrade():
    # Some local installations were initialized with metadata.create_all. Preserve
    # their existing lock rows; only fill the omission in the historical migrations.
    if "index_rebuild_lock" not in sa.inspect(op.get_bind()).get_table_names():
        op.create_table(
            "index_rebuild_lock",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("active_lock_token", sa.String(10), nullable=True),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("active_lock_token", name="uq_index_rebuild_single_active_lock"),
        )


def downgrade():
    op.drop_table("index_rebuild_lock")
