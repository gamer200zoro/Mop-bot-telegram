"""Smoke tests for the Telegram command registry."""

from __future__ import annotations

from commands.registry import iter_command_names


def test_command_registry_includes_core_modules() -> None:
    """The registry should expose the current production command set."""

    command_names = set(iter_command_names())
    expected = {
        "start",
        "help",
        "note",
        "notes",
        "todo",
        "todos",
        "remind",
        "reminders",
        "upload",
        "uploads",
        "download",
        "weather",
        "news",
        "fx",
        "qr",
        "ban",
        "kick",
        "mute",
        "warn",
    }
    assert expected.issubset(command_names)
