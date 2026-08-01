"""Telegram file transfer handlers."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from database.session import AsyncSessionLocal
from services.storage import StorageService
from services.uploads import UploadService
from services.users import UserService
from utils.files import build_storage_path, sanitize_filename


def _extract_media_descriptor(update: Update) -> tuple[str, str, str] | None:
    """Return the Telegram file ID, filename, and content type from a reply."""

    message = update.message
    if message is None or message.reply_to_message is None:
        return None

    source = message.reply_to_message
    if source.document is not None:
        return (
            source.document.file_id,
            sanitize_filename(source.document.file_name or "document.bin"),
            source.document.mime_type or "application/octet-stream",
        )
    if source.audio is not None:
        return (
            source.audio.file_id,
            sanitize_filename(source.audio.file_name or "audio.mp3"),
            source.audio.mime_type or "audio/mpeg",
        )
    if source.video is not None:
        return (
            source.video.file_id,
            sanitize_filename(source.video.file_name or "video.mp4"),
            source.video.mime_type or "video/mp4",
        )
    if source.voice is not None:
        return (
            source.voice.file_id,
            "voice.ogg",
            source.voice.mime_type or "audio/ogg",
        )
    if source.video_note is not None:
        return (source.video_note.file_id, "video_note.mp4", "video/mp4")
    if source.photo:
        return (source.photo[-1].file_id, "photo.jpg", "image/jpeg")
    return None


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

    descriptor = _extract_media_descriptor(update)
    if descriptor is None:
        await update.message.reply_text("No supported media found in the replied message")
        return

    telegram_file_id, filename, content_type = descriptor
    telegram_file = await context.bot.get_file(telegram_file_id)
    payload = await telegram_file.download_as_bytearray()
    storage_path = build_storage_path(user_id=user_id, filename=filename)
    stored = storage.upload_bytes(storage_path, bytes(payload), content_type=content_type)

    async with AsyncSessionLocal() as session:
        upload_service = UploadService(session)
        await upload_service.record_upload(
            user_id=user_id,
            original_filename=filename,
            storage_path=stored.path,
            bucket=stored.bucket,
            content_type=content_type,
            public_url=stored.public_url,
            file_size=len(payload),
        )
        await session.commit()

    reply = f"Uploaded as `{stored.path}`"
    if stored.public_url:
        reply += f"\nURL: {stored.public_url}"
    await update.message.reply_text(reply, parse_mode="Markdown")


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
