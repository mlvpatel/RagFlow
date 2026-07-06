"""API key auth, rate limiting, and input sanitization for RagFlow."""

from __future__ import annotations

import bleach
from fastapi import Header, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.core.config import get_settings

limiter = Limiter(key_func=get_remote_address)


def require_api_key(x_api_key: str = Header(default="")) -> None:
    """Reject any request without the configured X-API-Key header."""
    expected = get_settings().api_key
    if not x_api_key or x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )


def sanitize(text: str) -> str:
    """Strip any HTML so a question cannot smuggle markup into the pipeline."""
    return bleach.clean(text or "", tags=[], strip=True).strip()
