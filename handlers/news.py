"""Telegram news command handlers."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from services.news import NewsService


async def news_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return recent headlines for a topic."""

    if update.message is None:
        return

    topic = " ".join(context.args).strip()
    if not topic:
        await update.message.reply_text("Usage: /news topic")
        return

    try:
        items = await NewsService().top_headlines(topic)
    except Exception:
        await update.message.reply_text("Could not fetch news right now")
        return

    if not items:
        await update.message.reply_text("No headlines found")
        return

    lines = [f"• {item.title}" for item in items]
    await update.message.reply_text("Top headlines:\n" + "\n".join(lines))
