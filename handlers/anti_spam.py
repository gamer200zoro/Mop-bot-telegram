"""Telegram anti-spam guard handler."""

from __future__ import annotations

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ApplicationHandlerStop, ContextTypes

from services.anti_spam import AntiSpamService
from services.permissions import PermissionService


async def anti_spam_guard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop rapid-fire spam before it reaches the main command handlers."""

    message = update.effective_message
    user = update.effective_user
    if message is None or user is None:
        return

    if PermissionService(user.id).is_admin():
        return

    text = (message.text or message.caption or "").strip()
    if not text:
        return

    service = context.application.bot_data.setdefault("anti_spam_service", AntiSpamService())
    decision = service.check(user.id, text)
    if decision.allowed:
        return

    with contextlib.suppress(BadRequest):
        await message.delete()
    with contextlib.suppress(Exception):
        await context.bot.send_message(chat_id=message.chat_id, text=f"Please slow down. {decision.reason}")
    raise ApplicationHandlerStop
