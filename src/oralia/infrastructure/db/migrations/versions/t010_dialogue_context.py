"""Add bounded dialogue context, teacher units and idempotency receipts.

Revision ID: t010_dialogue_context
Revises: t007_demo_install
"""

import sqlalchemy as sa
from alembic import op

revision = "t010_dialogue_context"
down_revision = "t007_demo_install"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("cognitive_state", sa.Column("dialogue_context", sa.JSON(), nullable=True))
    op.create_table(
        "teaching_units",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("family_id", sa.String(36), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.String(36), sa.ForeignKey("course.id"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("kind", sa.String(20), nullable=False),
        sa.Column("topic_ref", sa.String(100), nullable=False),
        sa.Column("subgoal_ref", sa.String(100), nullable=False),
        sa.Column("reviewed_content", sa.Text(), nullable=False),
        sa.Column("source_refs", sa.JSON(), nullable=False),
        sa.Column("relations", sa.JSON(), nullable=False),
        sa.Column("reveal_policy", sa.String(30), nullable=False),
        sa.Column("activity_refs", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("family_id", "version", name="uq_teaching_unit_family_version"),
    )
    op.create_table(
        "turn_request_receipts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("session_id", sa.String(36), sa.ForeignKey("session.id"), nullable=False),
        sa.Column("client_request_id", sa.String(36), nullable=False),
        sa.Column("payload_sha256", sa.String(64), nullable=False),
        sa.Column("turn_id", sa.String(36), sa.ForeignKey("turn.id"), nullable=True),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("session_id", "client_request_id", name="uq_turn_request_receipt"),
    )


def downgrade():
    op.drop_table("turn_request_receipts")
    op.drop_table("teaching_units")
    with op.batch_alter_table("cognitive_state") as batch:
        batch.drop_column("dialogue_context")
