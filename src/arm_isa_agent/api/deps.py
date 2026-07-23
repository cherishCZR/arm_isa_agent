"""FastAPI dependency injection — provides shared services to route handlers."""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Optional

import structlog
from fastapi import HTTPException

from arm_isa_agent.core.config import Settings, get_settings
from arm_isa_agent.verification.orchestrator import VerificationOrchestrator

logger = structlog.get_logger(__name__)

# ── Global service singletons ─────────────────────────────────

_sqlite_client: Any = None
_llm: Any = None
_rag_pipeline: Any = None


def set_services(sqlite_client: Any = None, llm: Any = None, rag_pipeline: Any = None) -> None:
    """Inject shared services for API endpoints.

    Called once during application startup.
    """
    global _sqlite_client, _llm, _rag_pipeline
    _sqlite_client = sqlite_client or _sqlite_client
    _llm = llm or _llm
    _rag_pipeline = rag_pipeline or _rag_pipeline
    logger.info("api.services_set")


def get_sqlite() -> Any:
    if _sqlite_client is None:
        raise HTTPException(status_code=503, detail="SQLite service not initialized")
    return _sqlite_client


def get_llm() -> Any:
    if _llm is None:
        raise HTTPException(status_code=503, detail="LLM service not initialized")
    return _llm


def get_rag() -> Any:
    """Get the RAG pipeline. Returns None if not available (non-blocking)."""
    return _rag_pipeline


@lru_cache(maxsize=1)
def get_orchestrator(use_llm: bool = False) -> VerificationOrchestrator:
    """Get a cached VerificationOrchestrator instance."""
    return VerificationOrchestrator(
        sqlite_client=_sqlite_client,
        llm=_llm,
        use_llm_planning=use_llm,
        use_llm_review=use_llm,
    )
