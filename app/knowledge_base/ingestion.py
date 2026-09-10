from langchain_chroma import Chroma
from app.config.settings import CHROMA_DIR
from app.knowledge_base.loader import load_raw_documents
from app.knowledge_base.cleaner import clean_documents
from app.knowledge_base.chunker import chunk_documents
from app.knowledge_base.embeddings import get_embeddings


def build_vectorstore():
    """Full RAG ingestion pipeline: load -> clean -> chunk -> embed -> persist."""
    raw_documents = load_raw_documents()
    cleaned_documents = clean_documents(raw_documents)
    chunks = chunk_documents(cleaned_documents)

    embeddings = get_embeddings()

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    print(f"Vector store built with {len(chunks)} chunks from {len(raw_documents)} source documents.")


if __name__ == "__main__":
    build_vectorstore()