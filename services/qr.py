"""QR generation service for Jarvis."""

from __future__ import annotations

from io import BytesIO

import qrcode


class QRService:
    """Generate QR codes as PNG bytes."""

    def generate_png(self, payload: str) -> bytes:
        """Return a PNG image containing the provided payload."""

        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
        qr.add_data(payload)
        qr.make(fit=True)
        image = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()
