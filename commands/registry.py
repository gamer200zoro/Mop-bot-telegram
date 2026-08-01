"""Central command registry for Jarvis."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from handlers.help import help_handler
from handlers.start import start_handler


@dataclass(frozen=True, slots=True)
class CommandSpec:
    """Describe a Telegram command and its handler."""

    name: str
    description: str
    handler: object


COMMANDS: tuple[CommandSpec, ...] = (
    CommandSpec(name="start", description="Initialize Jarvis", handler=start_handler),
    CommandSpec(name="help", description="Show available commands", handler=help_handler),
)


def iter_command_names() -> Iterable[str]:
    """Return all command names in order."""

    return (command.name for command in COMMANDS)
