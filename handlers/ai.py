"""Telegram AI command handlers."""

from __future__ import annotations

from io import BytesIO

from telegram import Update
from telegram.ext import ContextTypes

from ai.service import AIService


async def ask_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answer a general chat prompt."""

    if update.message is None:
        return

    prompt = " ".join(context.args).strip()
    if not prompt:
        await update.message.reply_text("Usage: /ask question")
        return

    result = await AIService().chat(prompt)
    await update.message.reply_text(result.content)


async def summarize_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Summarize the provided text."""

    if update.message is None:
        return

    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("Usage: /summarize text")
        return

    result = await AIService().summarize(text)
    await update.message.reply_text(result.content)


async def grammar_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Correct grammar and punctuation."""

    if update.message is None:
        return

    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("Usage: /grammar text")
        return

    result = await AIService().correct_grammar(text)
    await update.message.reply_text(result.content)


async def translate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Translate text into a target language."""

    if update.message is None:
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /translate target_language text")
        return

    target_language = context.args[0]
    text = " ".join(context.args[1:]).strip()
    if not text:
        await update.message.reply_text("Usage: /translate target_language text")
        return

    try:
        result = await AIService().translate(text, target_language)
    except Exception:
        await update.message.reply_text("Translation requires an AI provider key")
        return
    await update.message.reply_text(result.content)


async def explain_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Explain a code snippet."""

    if update.message is None:
        return

    code = " ".join(context.args).strip()
    if not code:
        await update.message.reply_text("Usage: /explain code")
        return

    result = await AIService().explain_code(code)
    await update.message.reply_text(result.content)


def _extract_replied_image(update: Update) -> tuple[bytes, str] | None:
    """Extract image bytes from the replied-to message."""

    if update.message is None or update.message.reply_to_message is None:
        return None

    source = update.message.reply_to_message
    if source.document is not None:
        return source.document.file_id.encode("utf-8"), source.document.file_name or "image.png"
    if source.photo:
        return source.photo[-1].file_id.encode("utf-8"), "photo.jpg"
    if source.video is not None:
        return source.video.file_id.encode("utf-8"), source.video.file_name or "video.mp4"
    return None


async def ocr_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Extract text from a replied image."""

    _ = context
    if update.message is None:
        return

    descriptor = _extract_replied_image(update)
    if descriptor is None:
        await update.message.reply_text("Reply to an image or document and use /ocr")
        return

    file_id_bytes, filename = descriptor
    telegram_file = await update.get_bot().get_file(file_id_bytes.decode("utf-8"))
    payload = await telegram_file.download_as_bytearray()
    result = await AIService().ocr_image(bytes(payload), filename)
    await update.message.reply_text(result.content)


async def caption_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a short caption for a replied image."""

    _ = context
    if update.message is None:
        return

    descriptor = _extract_replied_image(update)
    if descriptor is None:
        await update.message.reply_text("Reply to an image or document and use /caption")
        return

    file_id_bytes, filename = descriptor
    telegram_file = await update.get_bot().get_file(file_id_bytes.decode("utf-8"))
    payload = await telegram_file.download_as_bytearray()
    result = await AIService().caption_image(bytes(payload), filename)
    await update.message.reply_text(result.content)
