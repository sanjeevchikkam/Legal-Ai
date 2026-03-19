import io
from pypdf import PdfReader
from docx import Document


def load_document(file_bytes: bytes, filename: str) -> str:
    """
    Accepts raw file bytes and filename.
    Returns extracted plain text.
    Supports PDF and DOCX only.
    """
    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        return _load_pdf(file_bytes)
    elif ext == "docx":
        return _load_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: .{ext}. Upload a PDF or DOCX.")


def _load_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text.strip())
    return "\n\n".join(pages)


def _load_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)