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
        "/help - show this help\n\n"
        "More modules are being added in layers: notes, todos, reminders, admin, AI, and files."
    )
    await update.message.reply_text(text)
