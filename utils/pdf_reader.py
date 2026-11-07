"""PDF text extraction using PyMuPDF."""
try:
    import pymupdf
except ImportError:  # older PyMuPDF versions
    import fitz as pymupdf


def extract_text_from_pdf(file_bytes: bytes) -> tuple[str, int]:
    """Return (full_text, page_count) from raw PDF bytes."""
    pages = []
    with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
        page_count = len(doc)
        for i, page in enumerate(doc, start=1):
            text = page.get_text().strip()
            if text:
                pages.append(f"[Page {i}]\n{text}")
    return "\n\n".join(pages), page_count
