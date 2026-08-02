"""Smoke tests for the PDF service."""

from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader, PdfWriter

from services.pdf import PDFService


def _make_pdf(page_count: int) -> bytes:
    """Create a tiny in-memory PDF with the requested number of pages."""

    writer = PdfWriter()
    for _ in range(page_count):
        writer.add_blank_page(width=72, height=72)
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def test_pdf_service_merge_pages() -> None:
    """Merging two PDFs should combine the page counts."""

    service = PDFService()
    merged = service.merge([_make_pdf(1), _make_pdf(2)])
    reader = PdfReader(BytesIO(merged))
    assert len(reader.pages) == 3


def test_pdf_service_split_range() -> None:
    """Splitting a PDF should return only the selected page range."""

    service = PDFService()
    split = service.split_range(_make_pdf(3), 2, 3)
    reader = PdfReader(BytesIO(split))
    assert len(reader.pages) == 2
