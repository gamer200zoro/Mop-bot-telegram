"""Telegram moderation command handlers."""

from __future__ import annotations

from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes


async def _parse_target_id(context: ContextTypes.DEFAULT_TYPE) -> int | None:
    """Parse the first positional argument as a Telegram user ID."""

    if not context.args:
        return None
    try:
        return int(context.args[0])
    except ValueError:
        return None


async def _ensure_group_chat(update: Update) -> bool:
    """Return True when the command is used inside a chat."""

    return update.effective_chat is not None and update.effective_message is not None


async def ban_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ban a member from the current chat."""

    if not await _ensure_group_chat(update):
        return
    target_id = await _parse_target_id(context)
    if target_id is None:
        await update.effective_message.reply_text("Usage: /ban user_id")
        return

    await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=target_id)
    await update.effective_message.reply_text(f"Banned user {target_id}.")


async def kick_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Kick a member from the current chat."""

    if not await _ensure_group_chat(update):
        return
    target_id = await _parse_target_id(context)
    if target_id is None:
        await update.effective_message.reply_text("Usage: /kick user_id")
        return

    await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=target_id)
    await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=target_id)
    await update.effective_message.reply_text(f"Kicked user {target_id}.")


async def mute_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Restrict a member from sending messages."""

    if not await _ensure_group_chat(update):
        return
    target_id = await _parse_target_id(context)
    if target_id is None:
        await update.effective_message.reply_text("Usage: /mute user_id")
        return

    permissions = ChatPermissions(can_send_messages=False)
    await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=target_id, permissions=permissions)
    await update.effective_message.reply_text(f"Muted user {target_id}.")


async def warn_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Issue a warning to a member."""

    if not await _ensure_group_chat(update):
        return
    target_id = await _parse_target_id(context)
    if target_id is None:
        await update.effective_message.reply_text("Usage: /warn user_id")
        return

    reason = " ".join(context.args[1:]).strip()
    warning = f"Warning issued to {target_id}."
    if reason:
        warning = f"Warning issued to {target_id}: {reason}"
    await update.effective_message.reply_text(warning)
