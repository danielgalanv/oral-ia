"""Add governance metadata; preserve all historical table DDL.

Revision ID: t005_governance
Revises: t004_oral_defense
"""

import sqlalchemy as sa
from alembic import op

revision = "t005_governance"
down_revision = "t004_oral_defense"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "activity_governance",
        sa.Column(
            "activity_configuration_id",
            sa.String(36),
            sa.ForeignKey("activity_configuration.id"),
            primary_key=True,
        ),
        sa.Column("family_id", sa.String(36), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("model_id", sa.String(100), nullable=False),
        sa.Column(
            "source_activity_configuration_id",
            sa.String(36),
            sa.ForeignKey("activity_configuration.id"),
            nullable=True,
        ),
        sa.Column("material_versions", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("family_id", "version", name="uq_governance_family_version"),
    )
    op.create_table(
        "session_privacy_preference",
        sa.Column("session_id", sa.String(36), sa.ForeignKey("session.id"), primary_key=True),
        sa.Column("retain", sa.Boolean(), nullable=False),
        sa.Column("scope", sa.JSON(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "uq_governance_active_family",
        "activity_governance",
        ["family_id"],
        unique=True,
        sqlite_where=sa.text("status = 'active'"),
    )
    op.create_table(
        "session_deletion_receipt",
        sa.Column("session_id", sa.String(36), sa.ForeignKey("session.id"), primary_key=True),
        sa.Column("reason", sa.String(30), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("counts", sa.JSON(), nullable=False),
    )


def downgrade():
    op.drop_table("session_deletion_receipt")
    op.drop_table("session_privacy_preference")
    op.drop_table("activity_governance")
