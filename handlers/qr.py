"""Telegram QR code command handlers."""

from __future__ import annotations

from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes

from services.qr import QRService


async def qr_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a QR code for the provided text."""

    if update.message is None:
        return

    payload = " ".join(context.args).strip()
    if not payload:
        await update.message.reply_text("Usage: /qr text or url")
        return

    png_bytes = QRService().generate_png(payload)
    buffer = BytesIO(png_bytes)
    buffer.name = "qr.png"
    await update.message.reply_photo(photo=buffer, caption="QR code generated")
