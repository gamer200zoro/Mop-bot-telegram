"""Image processing service for Jarvis.

The service supports metadata inspection, format conversion, and compression
using Pillow so Telegram uploads can be transformed without external APIs.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

from PIL import Image


@dataclass(slots=True)
class ImageMetadata:
    """Describe a decoded image payload."""

    width: int
    height: int
    mode: str
    format: str | None
    file_size_bytes: int


class ImageService:
    """Convert, compress, and inspect image files."""

    _supported_output_formats = {"PNG", "JPEG", "JPG", "WEBP"}

    def metadata(self, image_bytes: bytes) -> ImageMetadata:
        """Return basic metadata for an image payload."""

        with Image.open(BytesIO(image_bytes)) as image:
            return ImageMetadata(
                width=image.width,
                height=image.height,
                mode=image.mode,
                format=image.format,
                file_size_bytes=len(image_bytes),
            )

    def convert(self, image_bytes: bytes, output_format: str) -> bytes:
        """Convert an image to the requested output format."""

        normalized_format = self._normalize_format(output_format)
        with Image.open(BytesIO(image_bytes)) as image:
            converted = self._normalize_mode(image, normalized_format)
            output = BytesIO()
            converted.save(output, format=normalized_format)
            return output.getvalue()

    def compress(self, image_bytes: bytes, quality: int = 75) -> bytes:
        """Compress an image by re-saving it with optimization flags."""

        quality = max(1, min(quality, 95))
        with Image.open(BytesIO(image_bytes)) as image:
            format_name = self._normalize_format(image.format or "JPEG")
            optimized = self._normalize_mode(image, format_name)
            output = BytesIO()
            save_kwargs: dict[str, object] = {"optimize": True}
            if format_name in {"JPEG", "JPG", "WEBP"}:
                save_kwargs["quality"] = quality
            optimized.save(output, format=format_name, **save_kwargs)
            return output.getvalue()

    def _normalize_format(self, output_format: str) -> str:
        """Validate and normalize an output format name."""

        normalized = output_format.strip().upper().lstrip(".")
        if normalized == "JPG":
            normalized = "JPEG"
        if normalized not in self._supported_output_formats:
            raise ValueError(f"Unsupported image format: {output_format}")
        return normalized

    def _normalize_mode(self, image: Image.Image, output_format: str) -> Image.Image:
        """Coerce image mode for the target output format."""

        if output_format == "JPEG" and image.mode not in {"RGB", "L"}:
            return image.convert("RGB")
        if output_format == "WEBP" and image.mode == "P":
            return image.convert("RGBA")
        return image.copy()
