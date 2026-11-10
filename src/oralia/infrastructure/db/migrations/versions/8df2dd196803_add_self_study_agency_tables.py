"""add self study agency tables

Revision ID: 8df2dd196803
Revises: eeb4d1ff8e92
Create Date: 2026-09-02 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8df2dd196803"
down_revision: str | Sequence[str] | None = "eeb4d1ff8e92"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "self_study_activity_config",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("activity_configuration_id", sa.String(length=36), nullable=False),
        sa.Column("enabled_modes", sa.JSON(), nullable=False),
        sa.Column("summary_authorized", sa.Boolean(), nullable=False),
        sa.Column("practice_reveals_solution", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["activity_configuration_id"],
            ["activity_configuration.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("activity_configuration_id"),
    )
    op.create_table(
        "practice_question",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("turn_id", sa.String(length=36), nullable=False),
        sa.Column("question_type", sa.String(length=30), nullable=False),
        sa.Column("objective_ref", sa.String(length=500), nullable=False),
        sa.Column("concepts", sa.JSON(), nullable=False),
        sa.Column("fragment_ids", sa.JSON(), nullable=False),
        sa.Column("difficulty_hint", sa.String(length=10), nullable=False),
        sa.Column("reveals_solution", sa.Boolean(), nullable=False),
        sa.Column("generator_used", sa.String(length=20), nullable=False),
        sa.Column("non_disclosure_attempts", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["session.id"],
        ),
        sa.ForeignKeyConstraint(
            ["turn_id"],
            ["turn.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "coherence_incident",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("turn_id", sa.String(length=36), nullable=False),
        sa.Column("incident_type", sa.String(length=40), nullable=False),
        sa.Column("affected_proposal_ref", sa.String(length=36), nullable=True),
        sa.Column("recovery_action", sa.String(length=30), nullable=False),
        sa.Column("combined_verdict_source", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["session.id"],
        ),
        sa.ForeignKeyConstraint(
            ["turn_id"],
            ["turn.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("coherence_incident")
    op.drop_table("practice_question")
    op.drop_table("self_study_activity_config")
