"""Smoke tests for the AI service fallback behavior."""

from __future__ import annotations

import pytest

from ai.service import AIService


@pytest.mark.asyncio
async def test_ai_service_local_summarize() -> None:
    """Summarization should work without an API key."""

    result = await AIService().summarize("Jarvis is built step by step. It is getting stronger.")
    assert result.provider == "local"
    assert "Jarvis is built step by step" in result.content


@pytest.mark.asyncio
async def test_ai_service_local_grammar_cleanup() -> None:
    """Grammar cleanup should normalize punctuation locally."""

    result = await AIService().correct_grammar("jarvis is growing fast")
    assert result.provider == "local"
    assert result.content.endswith(".")
    assert result.content[0].isupper()


@pytest.mark.asyncio
async def test_ai_service_local_code_explanation() -> None:
    """Code explanation should return a structural summary locally."""

    result = await AIService().explain_code("print('hello')\nprint('world')")
    assert result.provider == "local"
    assert "2 non-empty line" in result.content
