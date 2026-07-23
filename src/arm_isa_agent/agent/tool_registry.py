"""Tool registry — register, describe, and invoke agent tools.

Tools are decorated with @register_tool and automatically become available
to the LangGraph executor via a name→callable registry.
"""

from __future__ import annotations

import inspect
from typing import Any, Callable

import structlog

logger = structlog.get_logger(__name__)

# Module-level service references (injected at agent startup)
_rag_pipeline: Any = None
_sqlite_client: Any = None
_llm: Any = None


def set_services(rag_pipeline: Any = None, sqlite_client: Any = None, llm: Any = None) -> None:
    """Inject shared service instances accessible from all tools."""
    global _rag_pipeline, _sqlite_client, _llm
    if rag_pipeline is not None:
        _rag_pipeline = rag_pipeline
    if sqlite_client is not None:
        _sqlite_client = sqlite_client
    if llm is not None:
        _llm = llm


def get_rag() -> Any:
    if _rag_pipeline is None:
        raise RuntimeError("RAG pipeline not injected. Call set_services() first.")
    return _rag_pipeline


def get_sqlite() -> Any:
    if _sqlite_client is None:
        raise RuntimeError("SQLite client not injected. Call set_services() first.")
    return _sqlite_client


def get_llm() -> Any:
    if _llm is None:
        raise RuntimeError("LLM not injected. Call set_services() first.")
    return _llm


# ── Registry ────────────────────────────────────────────────────

_registry: dict[str, dict[str, Any]] = {}


def register_tool(
    name: str,
    description: str,
    parameters: dict[str, Any] | None = None,
) -> Callable:
    """Decorator to register a tool function in the global registry.

    Args:
        name: Unique tool name (e.g. "retrieve_instruction").
        description: Human-readable description for the LLM planner.
        parameters: JSON Schema for tool arguments (auto-generated if None).

    Example:
        @register_tool("retrieve_instruction", "Search ARM instructions by semantics")
        def retrieve_instruction(query: str, top_k: int = 5) -> str:
            ...
    """

    def decorator(fn: Callable) -> Callable:
        sig = inspect.signature(fn)
        _params: dict[str, Any] = parameters or {}
        if not _params:
            props: dict[str, Any] = {}
            required: list[str] = []
            for pname, param in sig.parameters.items():
                if pname in ("self", "cls"):
                    continue
                ptype = "string"
                if param.annotation is int:
                    ptype = "integer"
                elif param.annotation is float:
                    ptype = "number"
                elif param.annotation is bool:
                    ptype = "boolean"

                prop: dict[str, Any] = {"type": ptype, "description": f"{pname} parameter"}
                if param.default is not inspect.Parameter.empty:
                    prop["default"] = param.default
                else:
                    required.append(pname)

                props[pname] = prop

            _params = {"type": "object", "properties": props}
            if required:
                _params["required"] = required

        _registry[name] = {
            "name": name,
            "description": description,
            "parameters": _params,
            "fn": fn,
        }
        logger.debug("tool.registered", name=name)
        return fn

    return decorator


def get_tool(name: str) -> Callable | None:
    """Get a tool function by name."""
    entry = _registry.get(name)
    return entry["fn"] if entry else None


def get_all_tools() -> dict[str, dict[str, Any]]:
    """Return all registered tools (name → metadata)."""
    return dict(_registry)


def get_tools_for_llm() -> list[dict[str, Any]]:
    """Return tools as OpenAI-compatible function definitions."""
    return [
        {
            "type": "function",
            "function": {
                "name": meta["name"],
                "description": meta["description"],
                "parameters": meta["parameters"],
            },
        }
        for meta in _registry.values()
    ]


def get_tools_descriptions() -> str:
    """Return human-readable tool descriptions for the planner prompt."""
    lines: list[str] = []
    for meta in _registry.values():
        lines.append(f"- **{meta['name']}**: {meta['description']}")
    return "\n".join(lines)
