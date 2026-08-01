"""Telegram /help command handler."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Explain the currently available commands."""

    _ = context
    if update.message is None:
        return

    text = (
        "Jarvis commands available now:\n"
        "/start - initialize the bot\n"
        "/help - show this help\n"
        "/note - create a note\n"
        "/notes - list notes\n"
        "/todo - create a todo\n"
        "/todos - list todos\n"
        "/remind - create a reminder\n"
        "/reminders - list reminders\n"
        "/upload - upload a replied media file\n"
        "/uploads - list uploaded files\n"
        "/download - download a stored file\n\n"
        "More modules are being added in layers: admin, AI, PDF tools, weather, news, and dashboard features."
    )
    await update.message.reply_text(text)
