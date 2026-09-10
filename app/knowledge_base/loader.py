import os
from pypdf import PdfReader
from app.config.settings import KNOWLEDGE_BASE_DIR


def _load_txt(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def _load_pdf(filepath: str) -> str:
    reader = PdfReader(filepath)
    text_parts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(text_parts)


def load_raw_documents() -> list[dict]:
    """Loads raw documents (.txt and .pdf) from the knowledge base directory.
    Returns a list of dicts: {"source": filename, "content": raw_text}."""
    documents = []
    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)

        if filename.endswith(".txt"):
            content = _load_txt(filepath)
        elif filename.endswith(".pdf"):
            content = _load_pdf(filepath)
        else:
            continue

        documents.append({"source": filename, "content": content})

    return documents