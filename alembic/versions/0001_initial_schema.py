"""Initial Jarvis schema.

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-08-01 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("create extension if not exists pgcrypto")

    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False, unique=True),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_users_telegram_id", "users", ["telegram_id"], unique=True)
    op.create_index("idx_users_last_seen_at", "users", ["last_seen_at"], unique=False)

    op.create_table(
        "notes",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("is_pinned", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_notes_user_id", "notes", ["user_id"], unique=False)
    op.create_index("idx_notes_is_pinned", "notes", ["is_pinned"], unique=False)

    op.create_table(
        "todos",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("is_done", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("priority", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_todos_user_id", "todos", ["user_id"], unique=False)
    op.create_index("idx_todos_is_done", "todos", ["is_done"], unique=False)
    op.create_index("idx_todos_priority", "todos", ["priority"], unique=False)

    op.create_table(
        "reminders",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("remind_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_sent", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_reminders_user_id", "reminders", ["user_id"], unique=False)
    op.create_index("idx_reminders_remind_at", "reminders", ["remind_at"], unique=False)
    op.create_index("idx_reminders_is_sent", "reminders", ["is_sent"], unique=False)

    op.create_table(
        "log_entries",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("level", sa.String(length=16), nullable=False),
        sa.Column("source", sa.String(length=128), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("idx_log_entries_level", "log_entries", ["level"], unique=False)
    op.create_index("idx_log_entries_source", "log_entries", ["source"], unique=False)
    op.create_index("idx_log_entries_created_at", "log_entries", ["created_at"], unique=False)

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

    for table_name in ("users", "notes", "todos", "reminders", "log_entries"):
        trigger_name = f"trg_{table_name}_updated_at"
        op.execute(f"drop trigger if exists {trigger_name} on public.{table_name}")
        op.execute(
            f"""
            create trigger {trigger_name}
            before update on public.{table_name}
            for each row execute function public.set_updated_at();
            """
        )


def downgrade() -> None:
    for table_name in ("log_entries", "reminders", "todos", "notes", "users"):
        op.execute(f"drop trigger if exists trg_{table_name}_updated_at on public.{table_name}")

    op.execute("drop function if exists public.set_updated_at()")
    op.drop_index("idx_log_entries_created_at", table_name="log_entries")
    op.drop_index("idx_log_entries_source", table_name="log_entries")
    op.drop_index("idx_log_entries_level", table_name="log_entries")
    op.drop_table("log_entries")
    op.drop_index("idx_reminders_is_sent", table_name="reminders")
    op.drop_index("idx_reminders_remind_at", table_name="reminders")
    op.drop_index("idx_reminders_user_id", table_name="reminders")
    op.drop_table("reminders")
    op.drop_index("idx_todos_priority", table_name="todos")
    op.drop_index("idx_todos_is_done", table_name="todos")
    op.drop_index("idx_todos_user_id", table_name="todos")
    op.drop_table("todos")
    op.drop_index("idx_notes_is_pinned", table_name="notes")
    op.drop_index("idx_notes_user_id", table_name="notes")
    op.drop_table("notes")
    op.drop_index("idx_users_last_seen_at", table_name="users")
    op.drop_index("idx_users_telegram_id", table_name="users")
    op.drop_table("users")
