"""State contracts for LangGraph-managed compiler verification runs."""

from __future__ import annotations

import operator
from typing import Annotated, Any, Literal, TypedDict

from arm_isa_agent.verification.models import VerificationReport


class VerificationGraphEvent(TypedDict, total=False):
    """A serializable event emitted by one verification graph node."""

    node: str
    status: Literal["started", "completed", "failed", "skipped"]
    message: str
    retry_count: int
    metadata: dict[str, Any]


class VerificationGraphState(TypedDict, total=False):
    """State shared by the LangGraph control plane and deterministic services."""

    request_id: str
    instruction: str
    normalized_instruction: str
    use_llm: bool
    instruction_count: int
    target_instruction_count: int
    retry_count: int
    max_retries: int
    report: VerificationReport | None
    events: Annotated[list[VerificationGraphEvent], operator.add]

