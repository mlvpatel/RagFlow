"""Load the bundled sample documents into RagFlow.

For a fully local, keyless run with Ollama:

    ollama serve &
    ollama pull nomic-embed-text
    EMBEDDING_PROVIDER=ollama python scripts/load_sample_data.py

Each file is chunked, embedded with the configured provider, and stored in
Chroma, exactly as an upload through the UI would be.
"""

import os
import sys
import uuid
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api import memory  # noqa: E402
from src.embeddings.vectorstore import index_document  # noqa: E402

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def main() -> None:
    memory.init_db()
    files = sorted(SAMPLE_DIR.glob("*.txt"))
    if not files:
        print(f"No .txt sample files found in {SAMPLE_DIR}")
        return
    print(f"Loading {len(files)} sample documents from {SAMPLE_DIR.name}/")
    for path in files:
        file_id = uuid.uuid4().hex
        chunks = index_document(str(path), file_id, path.name)
        memory.register_document(file_id, path.name, chunks)
        print(f"  {path.name}: {chunks} chunks")
    print("Done. Start the UI and ask a question, see sample_data/README.md.")


if __name__ == "__main__":
    main()
