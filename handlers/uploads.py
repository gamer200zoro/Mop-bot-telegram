"""Telegram upload history handlers."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from database.session import AsyncSessionLocal
from services.uploads import UploadService
from services.users import UserService


async def list_uploads_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List the most recent stored uploads for the current user."""

    _ = context
    if update.message is None or update.effective_user is None:
        return

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user_id = await user_service.register_telegram_user(
            telegram_id=update.effective_user.id,
            full_name=update.effective_user.full_name,
            username=update.effective_user.username,
        )
        upload_service = UploadService(session)
        uploads = await upload_service.list_uploads(user_id=user_id)

    if not uploads:
        await update.message.reply_text("No uploads yet. Use /upload by replying to a media message.")
        return

    lines = [f"#{upload.id} {upload.original_filename} -> {upload.storage_path}" for upload in uploads[:10]]
    await update.message.reply_text("Your uploads:\n" + "\n".join(lines))
