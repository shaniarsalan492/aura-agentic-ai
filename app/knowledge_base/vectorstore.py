from langchain_chroma import Chroma
from app.config.settings import CHROMA_DIR, RETRIEVAL_CANDIDATES, FINAL_K
from app.knowledge_base.reranker import rerank
from app.knowledge_base.embeddings import get_embeddings


def get_vectorstore():
    embeddings = get_embeddings()
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)


def search_policy(query: str, k: int = FINAL_K) -> str:
    """Retrieves policy chunks using a two-stage pipeline: broad vector similarity
    search for candidates, followed by hybrid reranking for final precision."""
    vectorstore = get_vectorstore()
    candidates = vectorstore.similarity_search(query, k=RETRIEVAL_CANDIDATES)
    reranked = rerank(query, candidates, top_k=k)
    return "\n\n".join([doc.page_content for doc in reranked])