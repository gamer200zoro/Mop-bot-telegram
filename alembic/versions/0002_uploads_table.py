"""Add uploads tracking table.

Revision ID: 0002_uploads_table
Revises: 0001_initial_schema
Create Date: 2026-08-01 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0002_uploads_table"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "uploads",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("storage_path", sa.String(length=512), nullable=False, unique=True),
        sa.Column("bucket", sa.String(length=128), nullable=False),
        sa.Column("content_type", sa.String(length=128), nullable=True),
        sa.Column("public_url", sa.Text(), nullable=True),
        sa.Column("file_size", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_uploads_user_id", "uploads", ["user_id"], unique=False)
    op.create_index("idx_uploads_storage_path", "uploads", ["storage_path"], unique=True)
    op.create_index("idx_uploads_created_at", "uploads", ["created_at"], unique=False)

    op.execute(
        """
        create or replace function public.set_updated_at()
        returns trigger
        language plpgsql
        as $$
        begin
            new.updated_at = now();
            return new;
        end;
        $$;
        """
    )
    op.execute("drop trigger if exists trg_uploads_updated_at on public.uploads")
    op.execute(
        """
        create trigger trg_uploads_updated_at
        before update on public.uploads
        for each row execute function public.set_updated_at();
        """
    )


def downgrade() -> None:
    op.execute("drop trigger if exists trg_uploads_updated_at on public.uploads")
    op.drop_index("idx_uploads_created_at", table_name="uploads")
    op.drop_index("idx_uploads_storage_path", table_name="uploads")
    op.drop_index("idx_uploads_user_id", table_name="uploads")
    op.drop_table("uploads")
