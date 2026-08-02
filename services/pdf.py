"""PDF processing service for Jarvis.

This module provides deterministic PDF merge and split operations built on top of
``pypdf`` so the Telegram bot can manipulate document uploads without external
services.
"""

from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader, PdfWriter


class PDFService:
    """Merge and split PDF documents in memory."""

    def merge(self, documents: list[bytes]) -> bytes:
        """Merge multiple PDF documents into a single file."""

        writer = PdfWriter()
        for document in documents:
            reader = PdfReader(BytesIO(document))
            for page in reader.pages:
                writer.add_page(page)

        output = BytesIO()
        writer.write(output)
        return output.getvalue()

    def split_range(self, document: bytes, start_page: int, end_page: int | None = None) -> bytes:
        """Extract a page range from a PDF document.

        Page numbers are 1-based and inclusive.
        """

        reader = PdfReader(BytesIO(document))
        total_pages = len(reader.pages)
        if total_pages == 0:
            raise ValueError("PDF contains no pages")
        if start_page < 1:
            raise ValueError("start_page must be at least 1")

        end_page = end_page or start_page
        if end_page < start_page:
            raise ValueError("end_page must be greater than or equal to start_page")

        writer = PdfWriter()
        for page_index in range(start_page - 1, min(end_page, total_pages)):
            writer.add_page(reader.pages[page_index])

        output = BytesIO()
        writer.write(output)
        return output.getvalue()

    def page_count(self, document: bytes) -> int:
        """Return the number of pages in the PDF document."""

        reader = PdfReader(BytesIO(document))
        return len(reader.pages)
