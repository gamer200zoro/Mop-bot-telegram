"""Telegram /start command handler."""

from __future__ import annotations

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greet the user and explain the bot's current capabilities."""

    _ = context
    user = update.effective_user
    if update.message is None or user is None:
        return

    name = user.full_name
    text = (
        f"Hello, {name}.\n\n"
        "Jarvis core is online. The foundation is active, and the rest of the system "
        "will be layered in module by module: database, dashboard, moderation, utilities, "
        "AI tools, and file services."
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
