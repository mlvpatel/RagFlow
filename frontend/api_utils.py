"""Thin HTTP client the Streamlit UI uses to talk to the RagFlow API."""

from __future__ import annotations

import os
from typing import Dict, List, Optional

import requests

API_URL = os.environ.get("RAGFLOW_API_URL", "http://localhost:8000")
API_KEY = os.environ.get("API_KEY", "change_me")
_HEADERS = {"X-API-Key": API_KEY}


def ask(question: str, session_id: Optional[str]) -> Dict:
    payload = {"question": question, "session_id": session_id}
    r = requests.post(f"{API_URL}/v1/chat", json=payload, headers=_HEADERS, timeout=120)
    r.raise_for_status()
    return r.json()


def upload(name: str, data: bytes) -> Dict:
    files = {"file": (name, data)}
    r = requests.post(
        f"{API_URL}/v1/upload-doc", files=files, headers=_HEADERS, timeout=300
    )
    r.raise_for_status()
    return r.json()


def list_docs() -> List[Dict]:
    r = requests.get(f"{API_URL}/v1/list-docs", headers=_HEADERS, timeout=30)
    r.raise_for_status()
    return r.json().get("documents", [])


def delete_doc(file_id: str) -> Dict:
    r = requests.post(
        f"{API_URL}/v1/delete-doc",
        json={"file_id": file_id},
        headers=_HEADERS,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()
