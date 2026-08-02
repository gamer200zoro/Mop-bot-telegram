"""Telegram PDF command handlers."""

from __future__ import annotations

from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes

from services.pdf import PDFService


async def _download_file_bytes(context: ContextTypes.DEFAULT_TYPE, file_id: str) -> bytes:
    """Download a Telegram file into memory."""

    telegram_file = await context.bot.get_file(file_id)
    payload = await telegram_file.download_as_bytearray()
    return bytes(payload)


async def merge_pdfs_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Merge multiple PDFs specified by Telegram file IDs."""

    if update.message is None:
        return

    file_ids = [arg.strip() for arg in context.args if arg.strip()]
    if len(file_ids) < 2:
        await update.message.reply_text("Usage: /pdfmerge file_id_1 file_id_2 [file_id_3 ...]")
        return

    documents = [await _download_file_bytes(context, file_id) for file_id in file_ids]
    merged_pdf = PDFService().merge(documents)
    buffer = BytesIO(merged_pdf)
    buffer.name = "merged.pdf"
    await update.message.reply_document(document=buffer, filename=buffer.name)


async def split_pdf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Split a replied PDF into a page range."""

    if update.message is None or update.message.reply_to_message is None:
        return

    source = update.message.reply_to_message.document
    if source is None or (source.mime_type or "") != "application/pdf":
        await update.message.reply_text("Reply to a PDF document and use /pdfsplit start [end]")
        return

    if not context.args:
        await update.message.reply_text("Usage: /pdfsplit start [end]")
        return

    try:
        start_page = int(context.args[0])
        end_page = int(context.args[1]) if len(context.args) > 1 else None
    except ValueError:
        await update.message.reply_text("Usage: /pdfsplit start [end]")
        return

    payload = await _download_file_bytes(context, source.file_id)
    try:
        split_pdf = PDFService().split_range(payload, start_page, end_page)
    except Exception:
        await update.message.reply_text("Could not split that PDF")
        return

    suffix = f"{start_page}-{end_page or start_page}"
    buffer = BytesIO(split_pdf)
    buffer.name = f"split_{suffix}.pdf"
    await update.message.reply_document(document=buffer, filename=buffer.name)
