"""Chroma vector store and embeddings for RagFlow (naive RAG, 2022).

One embedding model, one Chroma collection, one similarity search. There is no
hybrid search and no reranking, which is exactly what makes this the naive
baseline of the line.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.core.config import get_settings


def _build_embeddings():
    s = get_settings()
    if s.embedding_provider == "ollama":
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(
            model=s.ollama_embedding_model, base_url=s.ollama_base_url
        )
    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(model=s.embedding_model, api_key=s.openai_api_key or None)


@lru_cache
def get_vectorstore():
    from langchain_chroma import Chroma

    s = get_settings()
    os.makedirs(s.chroma_dir, exist_ok=True)
    return Chroma(
        collection_name=s.collection_name,
        embedding_function=_build_embeddings(),
        persist_directory=s.chroma_dir,
    )


def _load(path: str) -> List[Document]:
    """Read a file into a single Document. PDFs go through pypdf, everything else
    is read as text. Loading files directly keeps the dependency surface small,
    no heavy loader framework is pulled in."""
    if path.lower().endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    return [Document(page_content=text, metadata={"source": path})]


def load_and_split(path: str, file_id: str, filename: str = "") -> List[Document]:
    s = get_settings()
    docs = _load(path)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=s.chunk_size, chunk_overlap=s.chunk_overlap
    )
    chunks = splitter.split_documents(docs)
    label = filename or os.path.basename(path)
    for chunk in chunks:
        chunk.metadata["file_id"] = file_id
        chunk.metadata["filename"] = label
    return chunks


def index_document(path: str, file_id: str, filename: str = "") -> int:
    """Chunk, embed, and store a document. Returns the number of chunks."""
    chunks = load_and_split(path, file_id, filename)
    get_vectorstore().add_documents(chunks)
    return len(chunks)


def delete_document(file_id: str) -> None:
    get_vectorstore().delete(where={"file_id": file_id})
