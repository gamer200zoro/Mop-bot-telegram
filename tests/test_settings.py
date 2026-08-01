"""Tests for typed application settings."""

from __future__ import annotations

from config.settings import get_settings


def test_settings_singleton() -> None:
    """The settings factory should return a cached object."""

    first = get_settings()
    second = get_settings()
    assert first is second
    assert first.app_name == "Jarvis"
