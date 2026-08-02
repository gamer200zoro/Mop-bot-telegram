"""Telegram timing command handlers."""

from __future__ import annotations

import asyncio
from datetime import datetime
import calendar as calendar_module

from telegram import Update
from telegram.ext import ContextTypes

from services.timing import CalendarService, StopwatchService, parse_duration, schedule_timer


def _get_stopwatch_service(context: ContextTypes.DEFAULT_TYPE) -> StopwatchService:
    """Return the shared stopwatch service instance for the app."""

    service = context.application.bot_data.setdefault("stopwatch_service", StopwatchService())
    return service


async def timer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a one-shot timer that notifies the user later."""

    if update.message is None or update.effective_user is None:
        return

    if not context.args:
        await update.message.reply_text("Usage: /timer 10m reminder text")
        return

    try:
        delay_seconds = parse_duration(context.args[0])
    except ValueError:
        await update.message.reply_text("Usage: /timer 10m reminder text")
        return

    reminder_text = " ".join(context.args[1:]).strip() or "Timer finished"
    task = asyncio.create_task(schedule_timer(context.bot, update.effective_chat.id, delay_seconds, reminder_text))
    timers = context.application.bot_data.setdefault("timer_tasks", set())
    timers.add(task)
    task.add_done_callback(lambda done_task: timers.discard(done_task))

    await update.message.reply_text(f"Timer set for {delay_seconds} second(s).")


async def stopwatch_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Control the shared stopwatch for the current user."""

    if update.message is None or update.effective_user is None:
        return

    action = (context.args[0].lower() if context.args else "status")
    service = _get_stopwatch_service(context)
    user_id = update.effective_user.id

    try:
        if action == "start":
            service.start(user_id)
            await update.message.reply_text("Stopwatch started.")
            return
        if action == "lap":
            elapsed = service.lap(user_id)
            await update.message.reply_text(f"Lap: {elapsed:.2f} seconds")
            return
        if action == "stop":
            elapsed, laps = service.stop(user_id)
            lap_text = ", ".join(f"{lap:.2f}" for lap in laps) if laps else "none"
            await update.message.reply_text(f"Stopped at {elapsed:.2f} seconds. Laps: {lap_text}")
            return

        status = service.status(user_id)
        if status is None:
            await update.message.reply_text("Stopwatch not started. Use /stopwatch start")
            return
        elapsed, laps = status
        lap_text = ", ".join(f"{lap:.2f}" for lap in laps) if laps else "none"
        await update.message.reply_text(f"Running: {elapsed:.2f} seconds. Laps: {lap_text}")
    except ValueError as exc:
        await update.message.reply_text(str(exc))


async def calendar_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Render a monthly calendar."""

    if update.message is None:
        return

    now = datetime.now()
    month = now.month
    year = now.year

    if context.args:
        try:
            month = int(context.args[0])
            if len(context.args) > 1:
                year = int(context.args[1])
        except ValueError:
            await update.message.reply_text("Usage: /calendar [month] [year]")
            return

    try:
        rendered = CalendarService().render_month(year, month)
    except ValueError:
        await update.message.reply_text("Usage: /calendar [month] [year]")
        return

    await update.message.reply_text(f"<pre>{rendered}</pre>", parse_mode="HTML")
