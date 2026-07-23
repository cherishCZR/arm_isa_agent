"""Chat API routes — SSE streaming chat with pipeline progress."""

from __future__ import annotations

import json
import time
from typing import Any

import structlog
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from arm_isa_agent.api.deps import get_llm, get_rag, get_sqlite
from arm_isa_agent.api.schemas import ChatStreamRequest

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


def _sse(event: str, data: dict[str, Any]) -> str:
    """Format a single SSE event."""
    return f"event: {event}\ndata: {json.dumps(data, default=str)}\n\n"


def _detect_instruction(message: str) -> str | None:
    """Extract ARM instruction mnemonic from a chat message if verification is requested."""
    import re

    text = message.upper()
    # Common patterns: "verify ADD", "generate tests for SUB", "run LDR"
    patterns = [
        r"(?:VERIFY|GENERATE\s+(?:TEST|CASES?)\s+(?:FOR\s+)?|RUN\s+)([A-Z][A-Z0-9]{1,7})",
        r"(?:TEST\s+)([A-Z][A-Z0-9]{1,7})",
        r"\b(?:INSTRUCTION\s+)?([A-Z][A-Z0-9]{1,7})\b.*(?:VERIFY|TEST|GENERATE|PIPELINE)",
    ]

    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return m.group(1)

    # Fallback: look for common ARM mnemonics
    common_mnemonics = [
        "ADD", "SUB", "MUL", "MADD", "LDR", "STR", "STP", "LDP",
        "MOV", "CMP", "B", "BL", "ADRP", "FADD", "FMADD", "CSEL",
        "AND", "ORR", "EOR", "BIC", "LSL", "LSR", "ASR",
        "CBZ", "CBNZ", "TBZ", "TBNZ", "RET", "BR", "BLR",
    ]
    words = re.findall(r"\b([A-Z][A-Z0-9]{1,7})\b", text)
    for w in words:
        if w in common_mnemonics:
            return w

    return None


@router.post("/chat/stream")
async def chat_stream(request: ChatStreamRequest):
    """Streaming chat endpoint with SSE.

    If the message requests instruction verification, this will stream
    stage_start/stage_complete/result events just like the verification endpoint.
    Otherwise it streams a tokenized response from the agent.
    """
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="message field is required")

    logger.info("api.chat.stream", message=message[:100])

    try:
        sqlite = get_sqlite()
        rag = get_rag()

        # Check if this is a verification request
        instruction = _detect_instruction(message)

        # Verification requests don't need an LLM; general Q&A does
        llm = None
        if instruction is None:
            llm = get_llm()

        async def event_generator():
            if instruction:
                # Use verification pipeline for instruction-specific requests
                from arm_isa_agent.verification.orchestrator import VerificationOrchestrator

                orchestrator = VerificationOrchestrator(
                    sqlite_client=sqlite,
                    llm=llm,
                    use_llm_planning=False,
                    use_llm_review=False,
                )

                yield _sse("message", {
                    "role": "assistant",
                    "content": f"Running verification pipeline for {instruction}...",
                })

                async for sse_msg in orchestrator.verify_stream(instruction):
                    yield sse_msg

            else:
                # Use agent for general Q&A
                try:
                    from arm_isa_agent.agent.graph import AgentGraph

                    agent = AgentGraph(
                        rag_pipeline=rag,
                        sqlite_client=sqlite,
                    )
                    agent.initialize()

                    # Build chat history
                    history: list[dict[str, str]] = []
                    for h in request.history:
                        history.append({"role": h.get("role", "user"), "content": h.get("content", "")})

                    result = agent.run(message, chat_history=history)

                    answer = result.get("answer", "No response generated.")
                    iterations = result.get("iterations", 0)

                    # Stream the answer as SSE tokens
                    words = answer.split(" ")
                    for i, word in enumerate(words):
                        yield _sse("token", {
                            "content": word + (" " if i < len(words) - 1 else ""),
                            "done": i == len(words) - 1,
                        })

                    yield _sse("done", {"iterations": iterations})

                except Exception as agent_err:
                    logger.error("api.chat.agent_error", error=str(agent_err)[:200])
                    yield _sse("message", {
                        "role": "assistant",
                        "content": f"I wasn't able to process that request. You can use the /verify page for instruction verification. ({str(agent_err)[:100]})",
                    })
                    yield _sse("done", {})

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    except Exception as e:
        logger.error("api.chat.stream.error", error=str(e)[:300])
        raise HTTPException(status_code=500, detail=f"Chat stream failed: {str(e)[:300]}")
