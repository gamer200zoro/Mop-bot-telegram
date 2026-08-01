"""Central command registry for Jarvis."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from handlers.admin import ban_user_handler, kick_user_handler, mute_user_handler, warn_user_handler
from handlers.currency import currency_handler
from handlers.files import download_file_handler, upload_file_handler
from handlers.help import help_handler
from handlers.news import news_handler
from handlers.notes import create_note_handler, list_notes_handler
from handlers.qr import qr_handler
from handlers.reminders import create_reminder_handler, list_reminders_handler
from handlers.start import start_handler
from handlers.todos import create_todo_handler, list_todos_handler
from handlers.uploads import list_uploads_handler
from handlers.weather import weather_handler


@dataclass(frozen=True, slots=True)
class CommandSpec:
    """Describe a Telegram command and its handler."""

    name: str
    description: str
    handler: object


COMMANDS: tuple[CommandSpec, ...] = (
    CommandSpec(name="start", description="Initialize Jarvis", handler=start_handler),
    CommandSpec(name="help", description="Show available commands", handler=help_handler),
    CommandSpec(name="note", description="Create a note", handler=create_note_handler),
    CommandSpec(name="notes", description="List notes", handler=list_notes_handler),
    CommandSpec(name="todo", description="Create a todo", handler=create_todo_handler),
    CommandSpec(name="todos", description="List todos", handler=list_todos_handler),
    CommandSpec(name="remind", description="Create a reminder", handler=create_reminder_handler),
    CommandSpec(name="reminders", description="List reminders", handler=list_reminders_handler),
    CommandSpec(name="upload", description="Upload a replied media file", handler=upload_file_handler),
    CommandSpec(name="uploads", description="List uploaded files", handler=list_uploads_handler),
    CommandSpec(name="download", description="Download a stored file", handler=download_file_handler),
    CommandSpec(name="weather", description="Get current weather", handler=weather_handler),
    CommandSpec(name="news", description="Get headline news", handler=news_handler),
    CommandSpec(name="fx", description="Convert currencies", handler=currency_handler),
    CommandSpec(name="qr", description="Generate a QR code", handler=qr_handler),
    CommandSpec(name="ban", description="Ban a user", handler=ban_user_handler),
    CommandSpec(name="kick", description="Kick a user", handler=kick_user_handler),
    CommandSpec(name="mute", description="Mute a user", handler=mute_user_handler),
    CommandSpec(name="warn", description="Warn a user", handler=warn_user_handler),
)


def iter_command_names() -> Iterable[str]:
    """Return all command names in order."""

    return (command.name for command in COMMANDS)
