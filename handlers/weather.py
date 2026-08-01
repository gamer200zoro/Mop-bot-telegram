"""Telegram weather command handlers."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from services.weather import WeatherService


async def weather_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return the current weather for a location."""

    if update.message is None:
        return

    location = " ".join(context.args).strip()
    if not location:
        await update.message.reply_text("Usage: /weather city name")
        return

    try:
        report = await WeatherService().lookup(location)
    except Exception:
        await update.message.reply_text("Could not fetch weather for that location")
        return

    text = (
        f"Weather for {report.location}\n"
        f"{report.summary}\n"
        f"Temperature: {report.temperature_c:.1f}°C\n"
        f"Wind: {report.wind_speed_kph:.1f} km/h"
    )
    await update.message.reply_text(text)
