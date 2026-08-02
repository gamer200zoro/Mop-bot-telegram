"""Tests for the anti-spam service."""

from __future__ import annotations

from services.anti_spam import AntiSpamService


def test_anti_spam_allows_initial_messages() -> None:
    """The first few messages should be allowed."""

    service = AntiSpamService(max_messages=3, window_seconds=60.0)
    assert service.check(1, "hello").allowed is True
    assert service.check(1, "how are you").allowed is True


def test_anti_spam_blocks_repeated_messages() -> None:
    """Repeated messages should be blocked."""

    service = AntiSpamService(max_messages=3, window_seconds=60.0)
    assert service.check(1, "spam").allowed is True
    decision = service.check(1, "spam")
    assert decision.allowed is False
    assert decision.reason == "Repeated message detected"
