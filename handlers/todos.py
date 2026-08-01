"""Telegram todo command handlers."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from database.session import AsyncSessionLocal
from services.todos import TodoService
from services.users import UserService


def _parse_title_and_priority(payload: str) -> tuple[str, int]:
    """Parse a todo title and optional priority."""

    parts = [part.strip() for part in payload.split("|", 1)]
    title = parts[0] if parts else ""
    priority = 0
    if len(parts) == 2 and parts[1]:
        try:
            priority = int(parts[1])
        except ValueError:
            priority = 0
    return title, priority


async def create_todo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create a todo item."""

    if update.message is None or update.effective_user is None:
        return

    payload = " ".join(context.args).strip()
    title, priority = _parse_title_and_priority(payload)
    if not title:
        await update.message.reply_text("Usage: /todo title | priority")
        return

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user_id = await user_service.register_telegram_user(
            telegram_id=update.effective_user.id,
            full_name=update.effective_user.full_name,
            username=update.effective_user.username,
        )
        todo_service = TodoService(session)
        todo = await todo_service.create_todo(user_id=user_id, title=title, priority=priority)
        await session.commit()

    await update.message.reply_text(f"Saved todo #{todo.id}: {title}")


async def list_todos_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List current user's todos."""

    if update.message is None or update.effective_user is None:
        return

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user_id = await user_service.register_telegram_user(
            telegram_id=update.effective_user.id,
            full_name=update.effective_user.full_name,
            username=update.effective_user.username,
        )
        todo_service = TodoService(session)
        todos = await todo_service.list_todos(user_id=user_id)

    if not todos:
        await update.message.reply_text("No todos yet. Use /todo title | priority")
        return

    lines = [f"#{todo.id} [{'x' if todo.is_done else ' '}] {todo.title}" for todo in todos[:10]]
    await update.message.reply_text("Your todos:\n" + "\n".join(lines))
