"""Telegram file transfer handlers."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from database.session import AsyncSessionLocal
from services.users import UserService
from services.storage import StorageService
from utils.files import build_storage_path, sanitize_filename

_MEDIA_PRIORITY = ("document", "audio", "video", "voice", "video_note", "photo")


def _extract_media_name(update: Update) -> tuple[bytes, str, str] | None:
    """Extract the media bytes and a safe filename from a replied-to message."""

    message = update.message
    if message is None or message.reply_to_message is None:
        return None

    source = message.reply_to_message
    media_file_id: str | None = None
    filename = "file.bin"
    content_type = "application/octet-stream"

    if source.document is not None:
        media_file_id = source.document.file_id
        filename = source.document.file_name or filename
        content_type = source.document.mime_type or content_type
    elif source.audio is not None:
        media_file_id = source.audio.file_id
        filename = source.audio.file_name or "audio.mp3"
        content_type = source.audio.mime_type or content_type
    elif source.video is not None:
        media_file_id = source.video.file_id
        filename = source.video.file_name or "video.mp4"
        content_type = source.video.mime_type or content_type
    elif source.voice is not None:
        media_file_id = source.voice.file_id
        filename = "voice.ogg"
        content_type = source.voice.mime_type or "audio/ogg"
    elif source.video_note is not None:
        media_file_id = source.video_note.file_id
        filename = "video_note.mp4"
        content_type = "video/mp4"
    elif source.photo:
        media_file_id = source.photo[-1].file_id
        filename = "photo.jpg"
        content_type = "image/jpeg"
    else:
        return None

    return media_file_id.encode("utf-8"), sanitize_filename(filename), content_type


async def upload_file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Upload a replied-to Telegram media file to Supabase Storage."""

    _ = context
    if update.message is None or update.effective_user is None:
        return
    if update.message.reply_to_message is None:
        await update.message.reply_text("Reply to a media message and use /upload")
        return

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        user_id = await user_service.register_telegram_user(
            telegram_id=update.effective_user.id,
            full_name=update.effective_user.full_name,
            username=update.effective_user.username,
        )
        await session.commit()

    storage = StorageService()
    if not storage.is_enabled:
        await update.message.reply_text("Storage is not configured yet")
        return

    media_info = _extract_media_name(update)
    if media_info is None:
        await update.message.reply_text("No supported media found in the replied message")
        return

    media_file_id_bytes, filename, content_type = media_info
    media_file_id = media_file_id_bytes.decode("utf-8")
    telegram_file = await context.bot.get_file(media_file_id)
    payload = await telegram_file.download_as_bytearray()
    storage_path = build_storage_path(user_id=user_id, filename=filename)
    stored = storage.upload_bytes(storage_path, bytes(payload), content_type=content_type)

    await update.message.reply_text(
        f"Uploaded as `{stored.path}`" + (f"\nURL: {stored.public_url}" if stored.public_url else ""),
        parse_mode="Markdown",
    )


async def download_file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Download a stored file from Supabase Storage and send it back."""

    if update.message is None:
        return

    storage_path = " ".join(context.args).strip()
    if not storage_path:
        await update.message.reply_text("Usage: /download storage/path/file.ext")
        return

    storage = StorageService()
    if not storage.is_enabled:
        await update.message.reply_text("Storage is not configured yet")
        return

    try:
        payload = storage.download_bytes(storage_path)
    except Exception:
        await update.message.reply_text("Could not download that file")
        return

    filename = Path(storage_path).name or "download.bin"
    buffer = BytesIO(payload)
    buffer.name = filename
    await update.message.reply_document(document=buffer, filename=filename)
