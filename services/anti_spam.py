"""In-memory anti-spam heuristics for Jarvis."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from time import monotonic


@dataclass(slots=True)
class AntiSpamDecision:
    """Describe the outcome of a spam check."""

    allowed: bool
    reason: str | None = None


class AntiSpamService:
    """Track recent message activity and flag rapid-fire text spam."""

    def __init__(self, max_messages: int = 5, window_seconds: float = 10.0) -> None:
        self.max_messages = max_messages
        self.window_seconds = window_seconds
        self._recent_messages: dict[int, deque[tuple[float, str]]] = defaultdict(deque)

    def check(self, user_id: int, text: str) -> AntiSpamDecision:
        """Record a message and decide whether it should be allowed."""

        now = monotonic()
        bucket = self._recent_messages[user_id]
        cutoff = now - self.window_seconds

        while bucket and bucket[0][0] < cutoff:
            bucket.popleft()

        normalized_text = " ".join(text.lower().split())
        if bucket and bucket[-1][1] == normalized_text:
            bucket.append((now, normalized_text))
            return AntiSpamDecision(allowed=False, reason="Repeated message detected")

        bucket.append((now, normalized_text))
        if len(bucket) > self.max_messages:
            return AntiSpamDecision(allowed=False, reason="Message rate limit exceeded")

        return AntiSpamDecision(allowed=True)
