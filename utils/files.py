"""File and path helpers for Jarvis."""

from __future__ import annotations

import re
from pathlib import Path
from uuid import uuid4

_FILENAME_SAFE = re.compile(r"[^A-Za-z0-9._-]+")


def sanitize_filename(filename: str) -> str:
    """Return a filesystem-safe filename."""

    clean = _FILENAME_SAFE.sub("_", filename.strip())
    clean = clean.strip("._")
    return clean or f"file_{uuid4().hex}"


def build_storage_path(user_id: int, filename: str, prefix: str = "uploads") -> str:
    """Build a stable object path for Supabase Storage."""

    safe_filename = sanitize_filename(Path(filename).name)
    return f"{prefix}/{user_id}/{uuid4().hex}_{safe_filename}"
