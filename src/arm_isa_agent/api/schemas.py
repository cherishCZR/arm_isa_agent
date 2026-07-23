"""API request/response Pydantic schemas."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


# ── Verification ─────────────────────────────────────────────

class GenerateTestcaseRequest(BaseModel):
    """Request body for POST /api/generate_testcase."""

    instruction: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="ARM instruction mnemonic, e.g. ADD, LDR, STP",
        examples=["ADD", "LDR", "MADD"],
    )
    use_llm: bool = Field(
        default=False,
        description="Enable LLM-assisted generation, planning and review (slower, higher quality)",
    )
    instruction_count: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Target number of instruction instances in each generated test program",
    )
    target_instruction_count: int = Field(default=1, ge=1, le=10000)


class GenerateTestcaseResponse(BaseModel):
    """Response body for POST /api/generate_testcase."""

    instruction: str = Field(description="Target instruction mnemonic")
    status: str = Field(description="PASS | FAIL | REPAIRED | ERROR")
    generated_tests: int = Field(description="Total number of generated test cases")
    passing_test_count: int = Field(default=0, description="Number of passing test files")
    failing_test_count: int = Field(default=0, description="Number of failing test files")
    coverage: dict[str, float] = Field(
        description="Per-dimension coverage percentages",
    )
    review_score: float = Field(description="Overall review score 0-100")
    review_passed: bool = Field(description="Whether review passed")
    repair_attempts: int = Field(description="Number of repair loop iterations")
    repair_successful: bool = Field(description="Whether repair fixed all issues")
    total_duration_ms: float = Field(description="Total pipeline execution time in milliseconds")
    stage_results: list[dict[str, Any]] = Field(description="Per-stage timing and status (internal names)")
    stage_details: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Per-stage enhanced details for frontend (reasoning, findings, snapshots)",
    )
    test_files: list[dict[str, Any]] = Field(
        default_factory=list,
        description="All generated test files with content and metadata",
    )
    issues: list[dict[str, Any]] = Field(description="All review issues found")
    suggestions: list[str] = Field(description="Fix suggestions")
    generated_at: str = Field(description="ISO 8601 timestamp")
    verification_level: str = Field(default="generated")
    generated_status: str = Field(default="NOT_STARTED")
    static_review_status: str = Field(default="NOT_STARTED")
    compile_status: str = Field(default="NOT_STARTED")
    compile_results: list[dict[str, Any]] = Field(default_factory=list)
    failed_files: list[str] = Field(default_factory=list)
    toolchain: str = Field(default="")
    generation_mode: str = Field(default="rule_based")
    generation_trace: list[str] = Field(default_factory=list)
    budget: dict[str, Any] = Field(default_factory=dict)
    required_features: list[str] = Field(default_factory=list)
    canonical_targets: list[dict[str, Any]] = Field(default_factory=list)
    scenario_plan: list[dict[str, Any]] = Field(default_factory=list)


# ── Health ───────────────────────────────────────────────────

class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "ok"
    version: str = "0.1.0"


# ── Batch Verification ───────────────────────────────────────

class BatchGenerateRequest(BaseModel):
    """Request body for POST /api/generate_testcases."""

    instructions: list[str] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of ARM instruction mnemonics",
        examples=[["ADD", "SUB", "LDR"]],
    )
    use_llm: bool = Field(default=False)
    instruction_count: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Target number of instruction instances in each generated test program",
    )


class BatchGenerateResponse(BaseModel):
    """Response body for POST /api/generate_testcases."""

    total: int = Field(description="Total instructions processed")
    reports: list[dict[str, Any]] = Field(description="Per-instruction verification reports")
    summary: str = Field(default="", description="Batch summary")


# ── Stream Verification (SSE) ────────────────────────────────

class StreamVerificationRequest(BaseModel):
    """Request body for POST /api/generate_testcase/stream."""
    instruction: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="ARM instruction mnemonic",
    )
    use_llm: bool = Field(default=False)
    instruction_count: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Target number of instruction instances in each generated test program",
    )
    target_instruction_count: int = Field(default=1, ge=1, le=10000)


class BatchStreamRequest(BaseModel):
    """Request body for POST /api/generate_testcases/stream."""
    instructions: list[str] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of ARM instruction mnemonics",
    )
    use_llm: bool = Field(default=False)
    instruction_count: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Target number of instruction instances in each generated test program",
    )


# ── Scenario Batch (Multi-instruction per test program) ───────

class ScenarioBatchStreamRequest(BaseModel):
    """Request body for POST /api/scenario/stream — multi-instruction scenarios.

    Each inner list = one test scenario whose instructions are combined into
    a single test program.  One scenario per row in the input box / file.
    """
    scenarios: list[list[str]] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="List of scenarios; each scenario is a list of instruction mnemonics to combine into one program",
        examples=[[["ADD", "SUB", "MOV"], ["LDR", "STR"], ["CMP", "B.cond"]]],
    )
    use_llm: bool = Field(default=False)
    instruction_count: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Target total instruction instances across the combined test program",
    )
    target_instruction_count: int = Field(default=1, ge=1, le=10000)


class ParseScenarioFileRequest(BaseModel):
    """Parse scenario input from uploaded text content (txt/csv)."""
    content: str = Field(
        ...,
        min_length=1,
        description="Raw text content in scenario format (one row per scenario, comma-separated instructions)",
    )


# ── Download / File -------------------------------------------------

class DownloadFileRequest(BaseModel):
    """Request to download test files for one or more instructions."""
    instruction: str = Field(description="Target instruction mnemonic")
    file_ids: Optional[list[str]] = Field(
        default=None,
        description="Specific file IDs to download; None = all passing files",
    )


class BatchDownloadRequest(BaseModel):
    """Request to batch-download test files across multiple instructions."""
    instructions: list[str] = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Instruction mnemonics whose test files to include",
    )
    only_passing: bool = Field(default=True, description="Include only passing tests")


# ── Chat Stream ──────────────────────────────────────────────

class ChatStreamRequest(BaseModel):
    """Request body for POST /api/chat/stream."""
    message: str = Field(..., min_length=1, description="User chat message")
    history: list[dict[str, str]] = Field(
        default_factory=list,
        description="Previous chat history: [{'role': 'user'|'assistant', 'content': '...'}]",
    )
