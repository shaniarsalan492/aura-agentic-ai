import re


def clean_text(text: str) -> str:
    """Cleans raw document text before chunking: strips BOM/control characters,
    collapses excess whitespace, and normalizes line breaks so embedding quality
    isn't degraded by formatting artifacts."""
    text = text.replace("\ufeff", "")  # strip byte-order-mark artifacts
    text = text.replace("\r\n", "\n").replace("\r", "\n")  # normalize line endings
    text = re.sub(r"\n{3,}", "\n\n", text)  # collapse excess blank lines
    text = re.sub(r"[ \t]{2,}", " ", text)  # collapse repeated spaces/tabs
    text = "\n".join(line.strip() for line in text.split("\n"))  # trim each line
    return text.strip()


def clean_documents(documents: list[dict]) -> list[dict]:
    """Applies clean_text to a list of {"source", "content"} documents."""
    return [{"source": d["source"], "content": clean_text(d["content"])} for d in documents]