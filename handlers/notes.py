"""Telegram note command handlers."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from database.session import AsyncSessionLocal
from services.notes import NoteService
from services.users import UserService


def _split_payload(text: str, separator: str = "|") -> tuple[str, str]:
    """Split a text payload into title and content."""

    parts = [part.strip() for part in text.split(separator, 1)]
    if len(parts) != 2:
        return "", ""
    return parts[0], parts[1]


async def create_note_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create a note using a title and content separated by a pipe."""

    if update.message is None or update.effective_user is None:
        return

    payload = " ".join(context.args).strip()
    title, content = _split_payload(payload)
    if not title or not content:
        await update.message.reply_text("Usage: /note title | content")
        return

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user_id = await user_service.register_telegram_user(
            telegram_id=update.effective_user.id,
            full_name=update.effective_user.full_name,
            username=update.effective_user.username,
        )
        note_service = NoteService(session)
        note = await note_service.create_note(user_id=user_id, title=title, content=content)
        await session.commit()

    await update.message.reply_text(f"Saved note #{note.id}: {title}")


async def list_notes_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List the current user's notes."""

    if update.message is None or update.effective_user is None:
        return

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user_id = await user_service.register_telegram_user(
            telegram_id=update.effective_user.id,
            full_name=update.effective_user.full_name,
            username=update.effective_user.username,
        )
        note_service = NoteService(session)
        notes = await note_service.list_notes(user_id=user_id)

    if not notes:
        await update.message.reply_text("No notes yet. Use /note title | content")
        return

    lines = [f"#{note.id} {note.title}" for note in notes[:10]]
    await update.message.reply_text("Your notes:\n" + "\n".join(lines))
