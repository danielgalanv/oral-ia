"""Canonical SQLite trigger protecting the T090 activity policy columns.

This module is immutable for the current migration revision. Future trigger changes
must use another versioned module so historical migrations retain their exact SQL.
"""

from sqlalchemy import DDL, Table, event

ACTIVITY_POLICY_TRIGGER_NAME = "trg_t090_activity_policy_immutable"

CREATE_ACTIVITY_POLICY_TRIGGER_SQL = f"""
CREATE TRIGGER IF NOT EXISTS {ACTIVITY_POLICY_TRIGGER_NAME}
BEFORE UPDATE OF immutable_since, output_authorization_policy_json,
                 output_authorization_policy_sha256
ON activity_configuration
FOR EACH ROW
WHEN OLD.immutable_since IS NOT NULL
 AND (
    NEW.immutable_since IS NOT OLD.immutable_since
    OR NEW.output_authorization_policy_json IS NOT OLD.output_authorization_policy_json
    OR NEW.output_authorization_policy_sha256 IS NOT OLD.output_authorization_policy_sha256
 )
BEGIN
    SELECT RAISE(ABORT, 'immutable activity output authorization policy');
END
""".strip()

DROP_ACTIVITY_POLICY_TRIGGER_SQL = f"DROP TRIGGER IF EXISTS {ACTIVITY_POLICY_TRIGGER_NAME}"


def register_activity_policy_trigger(table: Table) -> None:
    """Install the canonical trigger after SQLAlchemy creates the activity table."""

    event.listen(
        table,
        "after_create",
        DDL(CREATE_ACTIVITY_POLICY_TRIGGER_SQL).execute_if(dialect="sqlite"),
    )


__all__ = [
    "ACTIVITY_POLICY_TRIGGER_NAME",
    "CREATE_ACTIVITY_POLICY_TRIGGER_SQL",
    "DROP_ACTIVITY_POLICY_TRIGGER_SQL",
    "register_activity_policy_trigger",
]
