"""Smoke tests for file helper utilities."""

from __future__ import annotations

from utils.files import build_storage_path, sanitize_filename


def test_sanitize_filename_removes_bad_characters() -> None:
    """Unsafe filename characters should be normalized away."""

    result = sanitize_filename("../my file?.png")
    assert ".." not in result
    assert " " not in result
    assert "?" not in result


def test_build_storage_path_uses_bucket_style_prefix() -> None:
    """Storage paths should include the prefix and user folder."""

    path = build_storage_path(user_id=42, filename="report.pdf")
    assert path.startswith("uploads/42/")
    assert path.endswith("report.pdf")
