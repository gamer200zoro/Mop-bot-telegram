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
        "/timer - set a timer\n"
        "/stopwatch - use the stopwatch\n"
        "/calendar - show a calendar\n"
        "/upload - upload a replied media file\n"
        "/uploads - list uploaded files\n"
        "/download - download a stored file\n"
        "/weather - get current weather\n"
        "/news - get headline news\n"
        "/fx - convert currencies\n"
        "/qr - generate a QR code\n"
        "/ask - chat with Jarvis\n"
        "/summarize - summarize text\n"
        "/grammar - correct grammar\n"
        "/translate - translate text\n"
        "/explain - explain code\n"
        "/ocr - extract text from an image\n"
        "/caption - caption an image\n"
        "/pdfmerge - merge PDFs\n"
        "/pdfsplit - split a PDF\n"
        "/imginfo - inspect an image\n"
        "/imgconvert - convert an image\n"
        "/imgcompress - compress an image\n\n"
        "More modules are being added in layers: admin and deeper dashboard features."
    )
    await update.message.reply_text(text)
