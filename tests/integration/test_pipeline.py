"""Integration test: index a document and retrieve from it with real embeddings.

Runs only when Ollama is reachable, so CI (which has no Ollama) skips it.
"""

import os
import tempfile

import pytest
import requests

OLLAMA = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")


def _ollama_up() -> bool:
    try:
        requests.get(OLLAMA, timeout=2)
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _ollama_up(), reason="Ollama not reachable")


def test_index_and_retrieve(monkeypatch, tmp_path):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "ollama")
    monkeypatch.setenv("CHROMA_DIR", str(tmp_path / "chroma"))
    monkeypatch.setenv("COLLECTION_NAME", "test_collection")

    from src.core.config import get_settings

    get_settings.cache_clear()
    from src.embeddings import vectorstore

    vectorstore.get_vectorstore.cache_clear()

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
        handle.write("The Nimbus Pro plan costs 49 dollars per month billed annually.")
        path = handle.name
    try:
        count = vectorstore.index_document(path, "testdoc")
        assert count >= 1
        results = vectorstore.get_vectorstore().similarity_search(
            "How much is the Nimbus Pro plan?", k=2
        )
        assert any("49" in d.page_content for d in results)
    finally:
        os.unlink(path)
        vectorstore.get_vectorstore.cache_clear()
        get_settings.cache_clear()
