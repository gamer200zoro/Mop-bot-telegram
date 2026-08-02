"""Tests for the timing utilities."""

from __future__ import annotations

from services.timing import CalendarService, StopwatchService, parse_duration


def test_parse_duration_supports_mixed_units() -> None:
    """Duration parsing should support compact mixed-unit values."""

    assert parse_duration("90") == 90
    assert parse_duration("2h30m") == 9000
    assert parse_duration("15m") == 900
    assert parse_duration("45s") == 45


def test_stopwatch_service_lifecycle() -> None:
    """The stopwatch service should support start, lap, status, and stop."""

    service = StopwatchService()
    user_id = 123
    service.start(user_id)
    status = service.status(user_id)
    assert status is not None
    elapsed, laps = status
    assert elapsed >= 0
    assert laps == []
    lap = service.lap(user_id)
    assert lap >= 0
    elapsed_after, laps_after = service.stop(user_id)
    assert elapsed_after >= 0
    assert len(laps_after) == 1


def test_calendar_service_renders_month() -> None:
    """The calendar service should render a predictable month grid."""

    rendered = CalendarService().render_month(2026, 8)
    assert "August 2026" in rendered
    assert "Mo Tu We Th Fr Sa Su" in rendered
