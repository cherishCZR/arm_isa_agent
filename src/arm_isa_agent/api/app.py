"""FastAPI application factory for ARM ISA Copilot Agent.

Usage:
    from arm_isa_agent.api.app import create_app
    app = create_app(sqlite_client, rag_pipeline, llm)
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI

from arm_isa_agent.api.deps import set_services
from arm_isa_agent.api.routes.chat import router as chat_router
from arm_isa_agent.api.routes.explore import router as explore_router
from arm_isa_agent.api.routes.verification import router as verification_router
from arm_isa_agent.core.config import Settings, get_settings
from arm_isa_agent.kb.sqlite.client import SQLiteClient
from arm_isa_agent.rag.pipeline import build_rag_pipeline

logger = structlog.get_logger(__name__)


def _build_llm(settings: Settings) -> ChatOpenAI | None:
    """Build a LangChain LLM client if credentials are configured."""
    if not settings.llm_api_key and not settings.llm_base_url:
        logger.warning("api.llm_not_configured")
        return None

    llm_kwargs: dict[str, Any] = {
        "model": settings.llm_model,
        "temperature": settings.llm_temperature,
    }
    if settings.llm_api_key:
        llm_kwargs["api_key"] = settings.llm_api_key
    if settings.llm_base_url:
        llm_kwargs["base_url"] = settings.llm_base_url

    try:
        return ChatOpenAI(**llm_kwargs)
    except Exception as e:
        logger.error("api.llm_build_failed", error=str(e))
        return None


def create_app(
    sqlite_client: Any = None,
    rag_pipeline: Any = None,
    llm: Any = None,
    settings: Settings | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        sqlite_client: Initialized SQLiteClient for structured queries.
        rag_pipeline: Initialized RAGPipeline for semantic search.
        llm: LangChain ChatOpenAI instance for LLM-assisted features.
        settings: Optional Settings override.

    Returns:
        Configured FastAPI app ready for uvicorn.
    """
    settings = settings or get_settings()

    set_services(sqlite_client=sqlite_client, llm=llm, rag_pipeline=rag_pipeline)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        nonlocal sqlite_client, rag_pipeline, llm

        if sqlite_client is None:
            logger.info("api.sqlite.auto_initializing", db_path=str(settings.sqlite_db_path))
            sqlite_client = SQLiteClient(str(settings.sqlite_db_path))
            sqlite_client.initialize()

        if rag_pipeline is None:
            logger.info("api.rag.auto_initializing")
            rag_pipeline = build_rag_pipeline()

        if llm is None:
            logger.info("api.llm.auto_initializing")
            llm = _build_llm(settings)

        set_services(sqlite_client=sqlite_client, llm=llm, rag_pipeline=rag_pipeline)
        logger.info("api.startup", port=settings.api_port)
        yield
        logger.info("api.shutdown")

    app = FastAPI(
        title="ARM ISA Copilot Agent",
        description="AI-powered Compiler Verification Agent for ARM A64 instruction set.",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(verification_router)
    app.include_router(explore_router)
    app.include_router(chat_router)

    return app
