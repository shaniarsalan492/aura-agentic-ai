import re
from collections import Counter
from langchain_core.documents import Document


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _lexical_overlap_score(query_tokens: list[str], doc_text: str) -> float:
    """Computes a term-overlap score between the query and a document chunk —
    a sparse signal used alongside dense (embedding) similarity. Measured as the
    fraction of the query's own terms that appear in the document, which better
    reflects relevance than raw term density in the document."""
    if not query_tokens:
        return 0.0
    doc_tokens = set(_tokenize(doc_text))
    matched = sum(1 for t in query_tokens if t in doc_tokens)
    return matched / len(query_tokens)

def rerank(query: str, candidates: list[Document], top_k: int = 2) -> list[Document]:
    """Reranks vector-retrieved candidates using a hybrid dense+sparse score:
    the candidate's original vector-similarity rank is combined with a lexical
    overlap score against the query, favoring chunks that are both semantically
    close AND contain the query's actual keywords."""
    query_tokens = _tokenize(query)
    scored = []
    for rank_position, doc in enumerate(candidates):
        dense_score = 1.0 - (rank_position / max(len(candidates), 1))
        sparse_score = _lexical_overlap_score(query_tokens, doc.page_content)
        combined_score = (0.6 * dense_score) + (0.4 * sparse_score)
        scored.append((combined_score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]