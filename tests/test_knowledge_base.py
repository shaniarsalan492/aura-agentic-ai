"""Tests for the RAG pipeline components: cleaning, chunking, and reranking logic."""

from app.knowledge_base.cleaner import clean_text
from app.knowledge_base.reranker import rerank
from langchain_core.documents import Document


def test_clean_text_strips_bom():
    dirty = "\ufeffHello world"
    assert clean_text(dirty) == "Hello world"


def test_clean_text_collapses_blank_lines():
    dirty = "Line one\n\n\n\nLine two"
    cleaned = clean_text(dirty)
    assert "\n\n\n" not in cleaned


def test_reranker_prioritizes_keyword_overlap():
    docs = [
        Document(page_content="This document talks about unrelated shipping topics."),
        Document(page_content="This document explicitly discusses the refund policy and eligibility."),
    ]
    results = rerank(query="refund policy eligibility", candidates=docs, top_k=1)
    assert "refund policy" in results[0].page_content.lower()


def test_reranker_respects_top_k():
    docs = [Document(page_content=f"chunk {i}") for i in range(5)]
    results = rerank(query="chunk", candidates=docs, top_k=2)
    assert len(results) == 2