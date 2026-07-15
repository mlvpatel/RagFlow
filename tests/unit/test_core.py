import os
import tempfile

from src.api.security import sanitize
from src.core.config import Settings


def test_sanitize_strips_html():
    cleaned = sanitize("<b>hello</b> <script>x</script>")
    assert "<" not in cleaned and ">" not in cleaned
    assert "hello" in cleaned
    assert sanitize("  spaced  ") == "spaced"
    assert sanitize("") == ""


def test_settings_defaults():
    s = Settings()
    assert s.top_k == 4
    assert s.embedding_provider in ("openai", "ollama")
    assert s.collection_name == "rag_naive_documents"


def test_load_and_split_tags_file_id():
    from src.embeddings.vectorstore import load_and_split

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
        handle.write("This is a test document. " * 300)
        path = handle.name
    try:
        chunks = load_and_split(path, "abc123")
        assert len(chunks) >= 1
        assert all(c.metadata.get("file_id") == "abc123" for c in chunks)
    finally:
        os.unlink(path)
