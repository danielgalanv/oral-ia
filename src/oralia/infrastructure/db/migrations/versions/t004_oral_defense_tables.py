"""Add Feature 004 oral-defense tables.

Revision ID: t004_oral_defense
Revises: t114_retention_auth
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "t004_oral_defense"
down_revision: str | Sequence[str] | None = "t114_retention_auth"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "defense_activity_config",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("activity_configuration_id", sa.String(36), nullable=False, unique=True),
        sa.Column("initial_questions", sa.JSON(), nullable=False),
        sa.Column("topics", sa.JSON(), nullable=False),
        sa.Column("difficulty_hint", sa.String(10), nullable=False),
        sa.Column("voice_input_allowed", sa.Boolean(), nullable=False),
        sa.Column("voice_output_allowed", sa.Boolean(), nullable=False),
        sa.Column("summary_authorized", sa.Boolean(), nullable=False),
        sa.Column("transcript_retention_authorized", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["activity_configuration_id"], ["activity_configuration.id"]),
    )
    op.create_table(
        "transcript",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("session_id", sa.String(36), nullable=False),
        sa.Column("turn_id", sa.String(36), nullable=True),
        sa.Column("raw_text", sa.String(4000), nullable=False),
        sa.Column("segments", sa.JSON(), nullable=False),
        sa.Column("overall_confidence", sa.Float(), nullable=False),
        sa.Column("low_confidence", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["session.id"]),
        sa.ForeignKeyConstraint(["turn_id"], ["turn.id"]),
    )
    op.create_table(
        "transcript_correction",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("transcript_id", sa.String(36), nullable=False, unique=True),
        sa.Column("session_id", sa.String(36), nullable=False),
        sa.Column("corrected_text", sa.String(4000), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["transcript_id"], ["transcript.id"]),
        sa.ForeignKeyConstraint(["session_id"], ["session.id"]),
    )
    op.create_table(
        "consent_record",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("session_id", sa.String(36), nullable=False, unique=True),
        sa.Column("decision", sa.String(10), nullable=False),
        sa.Column("scope", sa.JSON(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["session.id"]),
    )


def downgrade() -> None:
    op.drop_table("consent_record")
    op.drop_table("transcript_correction")
    op.drop_table("transcript")
    op.drop_table("defense_activity_config")
