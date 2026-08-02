"""Smoke tests for the image service."""

from __future__ import annotations

from io import BytesIO

from PIL import Image

from services.images import ImageService


def _make_image_bytes() -> bytes:
    """Create a tiny in-memory PNG image."""

    image = Image.new("RGB", (8, 8), color="red")
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def test_image_service_metadata() -> None:
    """Metadata should expose the decoded image properties."""

    meta = ImageService().metadata(_make_image_bytes())
    assert meta.width == 8
    assert meta.height == 8
    assert meta.format == "PNG"


def test_image_service_convert_and_compress() -> None:
    """Convert and compression operations should return valid image bytes."""

    service = ImageService()
    converted = service.convert(_make_image_bytes(), "jpeg")
    compressed = service.compress(_make_image_bytes(), quality=70)
    assert len(converted) > 0
    assert len(compressed) > 0
