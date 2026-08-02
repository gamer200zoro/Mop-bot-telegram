"""Telegram image processing handlers."""

from __future__ import annotations

from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes

from services.images import ImageService


def _extract_image_file(update: Update) -> tuple[str, str] | None:
    """Extract a Telegram file identifier and filename from a reply."""

    if update.message is None or update.message.reply_to_message is None:
        return None

    source = update.message.reply_to_message
    if source.document is not None:
        mime_type = source.document.mime_type or ""
        if not mime_type.startswith("image/") and not source.document.file_name:
            return None
        return source.document.file_id, source.document.file_name or "image.png"
    if source.photo:
        return source.photo[-1].file_id, "photo.jpg"
    return None


async def image_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show metadata for a replied image."""

    _ = context
    if update.message is None:
        return

    descriptor = _extract_image_file(update)
    if descriptor is None:
        await update.message.reply_text("Reply to an image and use /imginfo")
        return

    file_id, filename = descriptor
    telegram_file = await context.bot.get_file(file_id)
    payload = await telegram_file.download_as_bytearray()
    meta = ImageService().metadata(bytes(payload))
    await update.message.reply_text(
        f"{filename}\nFormat: {meta.format or 'unknown'}\nSize: {meta.width}x{meta.height}\nMode: {meta.mode}\nBytes: {meta.file_size_bytes}"
    )


async def image_convert_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Convert a replied image to a different output format."""

    if update.message is None:
        return

    if not context.args:
        await update.message.reply_text("Usage: /imgconvert format")
        return

    descriptor = _extract_image_file(update)
    if descriptor is None:
        await update.message.reply_text("Reply to an image and use /imgconvert format")
        return

    output_format = context.args[0]
    file_id, filename = descriptor
    telegram_file = await context.bot.get_file(file_id)
    payload = await telegram_file.download_as_bytearray()
    try:
        converted = ImageService().convert(bytes(payload), output_format)
    except Exception:
        await update.message.reply_text("Could not convert that image")
        return

    buffer = BytesIO(converted)
    extension = output_format.lower().lstrip(".")
    buffer.name = f"converted.{extension}"
    await update.message.reply_document(document=buffer, filename=buffer.name)


async def image_compress_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Compress a replied image."""

    if update.message is None:
        return

    descriptor = _extract_image_file(update)
    if descriptor is None:
        await update.message.reply_text("Reply to an image and use /imgcompress [quality]")
        return

    quality = 75
    if context.args:
        try:
            quality = int(context.args[0])
        except ValueError:
            quality = 75

    file_id, filename = descriptor
    telegram_file = await context.bot.get_file(file_id)
    payload = await telegram_file.download_as_bytearray()
    try:
        compressed = ImageService().compress(bytes(payload), quality=quality)
    except Exception:
        await update.message.reply_text("Could not compress that image")
        return

    buffer = BytesIO(compressed)
    buffer.name = f"compressed_{filename}"
    await update.message.reply_document(document=buffer, filename=buffer.name)
