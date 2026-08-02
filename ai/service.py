"""AI service layer for Jarvis.

This module provides one service object that can either call an OpenAI-compatible
chat/completions endpoint or fall back to local deterministic text utilities for
basic summaries and grammar cleanup.
"""

from __future__ import annotations

import base64
import re
from dataclasses import dataclass
from io import BytesIO
from typing import Any

import httpx

from config.settings import get_settings

settings = get_settings()


@dataclass(slots=True)
class AIResult:
    """A normalized AI response."""

    content: str
    provider: str


class AIService:
    """High-level AI helper with provider and local fallback modes."""

    def __init__(self) -> None:
        self.api_key = settings.openai_api_key.get_secret_value().strip()
        self.base_url = settings.openai_base_url.rstrip("/")
        self.model = settings.openai_model.strip() or "gpt-4o-mini"

    @property
    def provider_enabled(self) -> bool:
        """Return True when an OpenAI-compatible provider is configured."""

        return bool(self.api_key)

    async def chat(self, prompt: str) -> AIResult:
        """Respond to a general chat prompt."""

        if self.provider_enabled:
            content = await self._chat_completion(
                [
                    {"role": "system", "content": "You are Jarvis, a concise and helpful assistant."},
                    {"role": "user", "content": prompt},
                ]
            )
            return AIResult(content=content, provider="openai-compatible")
        return AIResult(content=self._local_chat(prompt), provider="local")

    async def summarize(self, text: str) -> AIResult:
        """Summarize long text into a compact note."""

        if self.provider_enabled:
            content = await self._chat_completion(
                [
                    {"role": "system", "content": "Summarize the text in a compact, factual way."},
                    {"role": "user", "content": text},
                ]
            )
            return AIResult(content=content, provider="openai-compatible")
        return AIResult(content=self._local_summarize(text), provider="local")

    async def correct_grammar(self, text: str) -> AIResult:
        """Apply a light grammar and punctuation cleanup."""

        if self.provider_enabled:
            content = await self._chat_completion(
                [
                    {"role": "system", "content": "Correct grammar, spelling, and punctuation. Preserve meaning."},
                    {"role": "user", "content": text},
                ]
            )
            return AIResult(content=content, provider="openai-compatible")
        return AIResult(content=self._local_grammar(text), provider="local")

    async def translate(self, text: str, target_language: str) -> AIResult:
        """Translate text to the requested language."""

        if not self.provider_enabled:
            raise RuntimeError("Translation requires OPENAI_API_KEY or another OpenAI-compatible provider")

        content = await self._chat_completion(
            [
                {"role": "system", "content": f"Translate the text into {target_language}. Keep meaning intact."},
                {"role": "user", "content": text},
            ]
        )
        return AIResult(content=content, provider="openai-compatible")

    async def explain_code(self, code: str) -> AIResult:
        """Explain what the code does and point out the structure."""

        if self.provider_enabled:
            content = await self._chat_completion(
                [
                    {"role": "system", "content": "Explain the code clearly and concisely."},
                    {"role": "user", "content": code},
                ]
            )
            return AIResult(content=content, provider="openai-compatible")
        return AIResult(content=self._local_code_explanation(code), provider="local")

    async def caption_image(self, image_bytes: bytes, filename: str | None = None) -> AIResult:
        """Generate a short caption for an image."""

        if self.provider_enabled:
            content = await self._chat_completion(
                [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Write one short caption for this image."},
                            {"type": "image_url", "image_url": {"url": self._data_url(image_bytes, filename)}},
                        ],
                    }
                ]
            )
            return AIResult(content=content, provider="openai-compatible")
        return AIResult(content=self._local_image_caption(image_bytes, filename), provider="local")

    async def ocr_image(self, image_bytes: bytes, filename: str | None = None) -> AIResult:
        """Extract text from an image."""

        if self.provider_enabled:
            content = await self._chat_completion(
                [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract every readable word from this image. Return only the text."},
                            {"type": "image_url", "image_url": {"url": self._data_url(image_bytes, filename)}},
                        ],
                    }
                ]
            )
            return AIResult(content=content, provider="openai-compatible")
        return AIResult(content=self._local_image_caption(image_bytes, filename), provider="local")

    async def _chat_completion(self, messages: list[dict[str, Any]]) -> str:
        """Call an OpenAI-compatible chat completion endpoint."""

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": messages, "temperature": 0.3}
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError("AI provider returned no choices")
        message = choices[0].get("message") or {}
        content = str(message.get("content", "")).strip()
        if not content:
            raise RuntimeError("AI provider returned empty content")
        return content

    def _data_url(self, image_bytes: bytes, filename: str | None = None) -> str:
        """Return a base64 data URL for an image payload."""

        _ = filename
        encoded = base64.b64encode(image_bytes).decode("ascii")
        return f"data:image/png;base64,{encoded}"

    def _local_chat(self, prompt: str) -> str:
        """Offer a concise local response when a provider is unavailable."""

        summary = self._local_summarize(prompt)
        return (
            "Local assistant mode is active.\n"
            f"Prompt digest: {summary}\n"
            "Enable OPENAI_API_KEY for richer answers."
        )

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into rough sentence chunks."""

        chunks = re.split(r"(?<=[.!?])\s+", text.strip())
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def _local_summarize(self, text: str) -> str:
        """Summarize text with a simple extractive strategy."""

        normalized = " ".join(text.split())
        if not normalized:
            return "No content provided."
        sentences = self._split_sentences(normalized)
        if len(sentences) <= 2:
            return normalized
        return " ".join(sentences[:2])

    def _local_grammar(self, text: str) -> str:
        """Perform light punctuation and whitespace cleanup."""

        cleaned = " ".join(text.split()).strip()
        if not cleaned:
            return ""
        cleaned = cleaned[0].upper() + cleaned[1:]
        if cleaned[-1] not in ".!?":
            cleaned += "."
        return cleaned

    def _local_code_explanation(self, code: str) -> str:
        """Return a structural explanation of the supplied code."""

        lines = [line.rstrip() for line in code.splitlines() if line.strip()]
        if not lines:
            return "No code provided."
        return (
            f"This snippet has {len(lines)} non-empty line(s).\n"
            f"First line: {lines[0]}\n"
            f"Last line: {lines[-1]}\n"
            "Use a provider for deeper semantic explanation."
        )

    def _local_image_caption(self, image_bytes: bytes, filename: str | None = None) -> str:
        """Describe basic properties of an image payload."""

        try:
            from PIL import Image

            with Image.open(BytesIO(image_bytes)) as image:
                width, height = image.size
                mode = image.mode
        except Exception:
            width = height = 0
            mode = "unknown"
        label = filename or "image"
        return f"{label}: {width}x{height} image in {mode} mode."
