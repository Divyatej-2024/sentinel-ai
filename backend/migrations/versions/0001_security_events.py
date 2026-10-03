"""Create normalized security event store."""

from alembic import op
import sqlalchemy as sa

revision = "0001_security_events"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "security_events",
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("source", sa.String(length=128), nullable=False),
        sa.Column("source_ip", sa.String(length=45), nullable=True),
        sa.Column("destination_ip", sa.String(length=45), nullable=True),
        sa.Column("source_port", sa.Integer(), nullable=True),
        sa.Column("destination_port", sa.Integer(), nullable=True),
        sa.Column("protocol", sa.String(length=32), nullable=True),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("hostname", sa.String(length=255), nullable=True),
        sa.Column("process_name", sa.String(length=255), nullable=True),
        sa.Column("action", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=True),
        sa.Column("severity", sa.String(length=16), nullable=True),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("event_id"),
    )
    for field in ("timestamp", "event_type", "source", "source_ip", "destination_ip", "username", "hostname", "status", "severity"):
        op.create_index(f"ix_security_events_{field}", "security_events", [field])


def downgrade() -> None:
    op.drop_table("security_events")
