from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(documents: list[dict]) -> list[Document]:
    """Splits cleaned documents into overlapping chunks, preserving source metadata."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = []
    for doc in documents:
        pieces = splitter.split_text(doc["content"])
        for piece in pieces:
            chunks.append(Document(page_content=piece, metadata={"source": doc["source"]}))
    return chunks