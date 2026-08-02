"""Timing utilities for Jarvis.

This module provides reusable helpers for timers, stopwatches, and calendar
rendering. The timer handler uses asyncio tasks while the stopwatch and calendar
logic stay deterministic and testable.
"""

from __future__ import annotations

import asyncio
import calendar as calendar_module
import re
from dataclasses import dataclass, field
from time import monotonic

from telegram import Bot

_DURATION_PATTERN = re.compile(r"(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s?)?$", re.IGNORECASE)


def parse_duration(value: str) -> int:
    """Parse a human-friendly duration string into seconds.

    Supported forms include plain seconds (``90``), or mixed units like
    ``2h30m`` / ``15m`` / ``45s``.
    """

    normalized = value.strip().lower()
    if not normalized:
        raise ValueError("duration is required")
    if normalized.isdigit():
        return int(normalized)

    match = _DURATION_PATTERN.fullmatch(normalized)
    if not match:
        raise ValueError(f"Invalid duration: {value}")

    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    seconds = int(match.group("seconds") or 0)
    total = hours * 3600 + minutes * 60 + seconds
    if total <= 0:
        raise ValueError(f"Invalid duration: {value}")
    return total


@dataclass(slots=True)
class StopwatchState:
    """Track one stopwatch session for a user."""

    started_at: float = field(default_factory=monotonic)
    laps: list[float] = field(default_factory=list)


class StopwatchService:
    """Manage stopwatch sessions in memory."""

    def __init__(self) -> None:
        self._sessions: dict[int, StopwatchState] = {}

    def start(self, user_id: int) -> None:
        """Start or restart a stopwatch for a user."""

        self._sessions[user_id] = StopwatchState()

    def lap(self, user_id: int) -> float:
        """Record a lap and return the elapsed seconds."""

        session = self._require_session(user_id)
        elapsed = monotonic() - session.started_at
        session.laps.append(elapsed)
        return elapsed

    def stop(self, user_id: int) -> tuple[float, list[float]]:
        """Stop the stopwatch and return the total elapsed time and laps."""

        session = self._require_session(user_id)
        elapsed = monotonic() - session.started_at
        laps = list(session.laps)
        self._sessions.pop(user_id, None)
        return elapsed, laps

    def status(self, user_id: int) -> tuple[float, list[float]] | None:
        """Return the current elapsed time and laps if the stopwatch is active."""

        session = self._sessions.get(user_id)
        if session is None:
            return None
        return monotonic() - session.started_at, list(session.laps)

    def _require_session(self, user_id: int) -> StopwatchState:
        """Return the active session or raise a ValueError."""

        session = self._sessions.get(user_id)
        if session is None:
            raise ValueError("Stopwatch not started")
        return session


class CalendarService:
    """Render simple monthly calendars."""

    def render_month(self, year: int, month: int) -> str:
        """Return a text calendar for a given month and year."""

        if month < 1 or month > 12:
            raise ValueError("Month must be between 1 and 12")
        return calendar_module.TextCalendar(firstweekday=0).formatmonth(year, month)


async def schedule_timer(bot: Bot, chat_id: int, delay_seconds: int, message: str) -> None:
    """Send a message after a delay using the current event loop."""

    await asyncio.sleep(delay_seconds)
    await bot.send_message(chat_id=chat_id, text=f"⏰ Timer finished: {message}")
