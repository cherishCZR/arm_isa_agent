"""Verification data models — VerificationReport, CoverageBreakdown, StageResult, SSE types."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════
# Pipeline Stage (frontend-facing)
# ═══════════════════════════════════════════════════════════════

PipelineStage = Literal["planner", "retrieval", "llm", "generator", "reviewer", "compiler", "repair"]
StageStatus = Literal["pending", "running", "ok", "warning", "error", "skipped"]
VerificationLevel = Literal["generated", "statically_reviewed", "compiled"]
LayerStatus = Literal["NOT_STARTED", "PASS", "WARNING", "FAIL", "SKIPPED"]
OverallStatus = Literal["PASS", "FAIL", "REPAIRED", "ERROR", "GENERATED", "REVIEWED", "COMPILED", "FAILED"]

# Map internal 6-stage names → frontend 5-stage names
INTERNAL_TO_FRONTEND_STAGE: dict[str, PipelineStage] = {
    "analyzer": "retrieval",
    "planning": "planner",
    "constraint_analysis": "planner",
    "test_planning": "planner",
    "retrieval": "retrieval",
    "test_generation": "generator",
    "test_review": "reviewer",
    "llm": "llm",
    "compile": "compiler",
    "repair": "repair",
}


# ═══════════════════════════════════════════════════════════════
# Coverage Breakdown
# ═══════════════════════════════════════════════════════════════

class CoverageBreakdown(BaseModel):
    """Per-dimension coverage percentages (0–100%)."""

    boundary: float = Field(default=0.0, ge=0.0, le=100.0, description="Boundary value coverage")
    alias: float = Field(default=0.0, ge=0.0, le=100.0, description="Alias equivalence coverage")
    invalid: float = Field(default=0.0, ge=0.0, le=100.0, description="Invalid operand coverage")
    normal: float = Field(default=0.0, ge=0.0, le=100.0, description="Normal operation coverage")
    encoding: float = Field(default=0.0, ge=0.0, le=100.0, description="Encoding variant coverage")
    feature: float = Field(default=0.0, ge=0.0, le=100.0, description="Feature dependency coverage")

    @property
    def overall(self) -> float:
        """Average across all non-zero dimensions."""
        scores = [v for v in [self.boundary, self.alias, self.invalid, self.normal, self.encoding, self.feature] if v > 0]
        if not scores:
            return 0.0
        return sum(scores) / len(scores)


# ═══════════════════════════════════════════════════════════════
# Stage Result (original — used internally)
# ═══════════════════════════════════════════════════════════════

class StageResult(BaseModel):
    """Result from a single pipeline stage (internal naming)."""

    stage: Literal["retrieval", "constraint_analysis", "test_planning", "llm", "test_generation", "test_review", "compile", "repair"]
    status: Literal["ok", "warning", "error", "skipped"] = "ok"
    duration_ms: float = Field(default=0.0, description="Stage execution time in milliseconds")
    output_summary: str = Field(default="", description="Human-readable stage summary")
    error: str = Field(default="", description="Error message if status is 'error'")


# ═══════════════════════════════════════════════════════════════
# Stage Detail (frontend-facing, enhanced)
# ═══════════════════════════════════════════════════════════════

class StageDetail(BaseModel):
    """Enhanced stage result for the frontend — with reasoning, findings, and snapshots."""

    stage: PipelineStage = Field(description="Frontend stage name: planner|retrieval|generator|reviewer|repair")
    status: StageStatus = "ok"
    duration_ms: float = Field(default=0.0, description="Stage execution time in milliseconds")
    summary: str = Field(default="", description="One-line summary for the frontend")
    reasoning: str = Field(default="", description="Full reasoning chain from this stage")
    key_findings: list[str] = Field(default_factory=list, description="Key bullet-point findings")
    data_snapshot: dict[str, Any] = Field(
        default_factory=dict,
        description="Key metrics snapshot, e.g. encoding_count, operand_count, total_tests",
    )
    error: str = Field(default="", description="Error message if status is 'error'")


# ═══════════════════════════════════════════════════════════════
# Test File Entry
# ═══════════════════════════════════════════════════════════════

class TestFileEntry(BaseModel):
    """A single generated test file with content and metadata."""

    file_id: str = Field(description="Unique file identifier, e.g. ADD_test_normal_01")
    filename: str = Field(description="Filename, e.g. ADD_test_normal_01.s")
    format: Literal["s", "c", "cpp", "llvm"] = Field(description="File format: s|c|cpp|llvm")
    test_type: str = Field(
        description="Test category: normal|boundary|alias|invalid|feature|inline_asm|llvm_mc|cpp_verify"
    )
    content: str = Field(description="Full file content (assembly / C / C++ / LLVM MC)")
    status: Literal["pass", "fail"] = Field(default="pass", description="Review pass/fail status")
    description: str = Field(default="", description="What this test verifies")
    issue_count: int = Field(default=0, description="Number of review issues on this file")


class CompileResult(BaseModel):
    """Result from compiling/assembling a generated test file."""

    file_id: str = ""
    filename: str = ""
    status: Literal["PASS", "FAIL", "SKIPPED"] = "SKIPPED"
    toolchain: str = ""
    command: list[str] = Field(default_factory=list)
    return_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    duration_ms: float = 0.0
    reason: str = ""


class CompileSummary(BaseModel):
    """Aggregated compile results for one verification report."""

    status: Literal["PASS", "FAIL", "SKIPPED"] = "SKIPPED"
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    results: list[CompileResult] = Field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
# SSE Event Models
# ═══════════════════════════════════════════════════════════════

class SSEStageStart(BaseModel):
    """SSE event: a stage has started."""
    stage: PipelineStage
    message: str = Field(description="Human-readable message, e.g. 'Analyzing ADD constraints...'")
    timestamp: float = Field(default_factory=lambda: datetime.now(timezone.utc).timestamp())
    instruction: Optional[str] = None


class SSEStageProgress(BaseModel):
    """SSE event: progress update within a stage."""
    stage: PipelineStage
    detail: str = Field(description="Progress detail, e.g. 'Generating Normal tests... 4/6'")
    instruction: Optional[str] = None


class SSEStageComplete(BaseModel):
    """SSE event: a stage has completed."""
    stage: PipelineStage
    status: StageStatus
    duration_ms: float
    summary: str
    findings: list[str] = Field(default_factory=list)
    snapshot: dict[str, Any] = Field(default_factory=dict)
    instruction: Optional[str] = None


class SSEInstructionStart(BaseModel):
    """SSE event: an instruction in a batch has started."""
    index: int
    instruction: str
    total: int


class SSEInstructionComplete(BaseModel):
    """SSE event: an instruction in a batch has completed."""
    index: int
    instruction: str
    status: str
    review_score: float
    duration_ms: float
    test_files: list[dict[str, Any]] = Field(default_factory=list)


class SSEBatchStart(BaseModel):
    """SSE event: a batch verification has started."""
    total: int
    instructions: list[str]


class SSEBatchComplete(BaseModel):
    """SSE event: a batch verification has completed."""
    total: int
    passed: int
    failed: int
    total_duration_ms: float
    reports: list[dict[str, Any]] = Field(default_factory=list)


class SSEResult(BaseModel):
    """SSE event: final verification result."""
    instruction: str
    status: str
    review_score: float
    total_tests: int
    passing_tests: int
    failing_tests: int
    total_duration_ms: float
    stage_details: list[dict[str, Any]] = Field(default_factory=list)
    test_files: list[dict[str, Any]] = Field(default_factory=list)
    coverage: dict[str, float] = Field(default_factory=dict)
    issues: list[dict[str, Any]] = Field(default_factory=list)
    verification_level: VerificationLevel = "generated"
    generated_status: LayerStatus = "NOT_STARTED"
    static_review_status: LayerStatus = "NOT_STARTED"
    compile_status: LayerStatus = "NOT_STARTED"
    compile_results: list[dict[str, Any]] = Field(default_factory=list)
    generation_mode: str = "rule_based"
    generation_trace: list[str] = Field(default_factory=list)
    budget: dict[str, Any] = Field(default_factory=dict)
    required_features: list[str] = Field(default_factory=list)
    canonical_targets: list[dict[str, Any]] = Field(default_factory=list)
    scenario_plan: list[dict[str, Any]] = Field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
# Verification Report — the core output
# ═══════════════════════════════════════════════════════════════

class VerificationReport(BaseModel):
    """Complete compiler verification report for a single ARM instruction.

    Generated by VerificationOrchestrator after running the full pipeline:
    Retrieval → Constraint Analysis → Test Planning → Test Generation → Review + Repair Loop.

    JSON Schema:
    {
      "instruction": "ADD",
      "status": "PASS",
      "generated_tests": 20,
      "coverage": { "boundary": 100, "alias": 80, "invalid": 100, "normal": 100, "encoding": 100, "feature": 0 },
      "review_score": 96,
      "issues": [],
      "repair_attempts": 0,
      "stage_results": [...],
      "stage_details": [...],
      "test_files": [...],
      "generated_at": "2026-01-01T00:00:00Z",
      "instruction_profile": {...},
      ...
    }
    """

    # ── Core fields ────────────────────────────────────────
    instruction: str = Field(description="Target instruction mnemonic, e.g. 'ADD'")
    status: OverallStatus = Field(
        default="PASS",
        description="Overall verification status",
    )
    verification_level: VerificationLevel = "generated"
    generated_status: LayerStatus = "NOT_STARTED"
    static_review_status: LayerStatus = "NOT_STARTED"
    compile_status: LayerStatus = "NOT_STARTED"
    generated_tests: int = Field(default=0, description="Total number of generated test cases")
    passing_test_count: int = Field(default=0, description="Number of passing test files")
    failing_test_count: int = Field(default=0, description="Number of failing test files")

    # ── Coverage ───────────────────────────────────────────
    coverage: CoverageBreakdown = Field(default_factory=CoverageBreakdown)

    # ── Review ─────────────────────────────────────────────
    review_score: float = Field(default=0.0, ge=0.0, le=100.0)
    review_passed: bool = Field(default=False, description="Whether review passed")

    # ── Issues ─────────────────────────────────────────────
    issues: list[dict[str, Any]] = Field(
        default_factory=list,
        description="All review issues (type, severity, description, location, suggestion, dimension)",
    )
    suggestions: list[str] = Field(
        default_factory=list,
        description="Concrete fix suggestions from reviewer",
    )

    # ── Repair ─────────────────────────────────────────────
    repair_attempts: int = Field(default=0, description="Number of repair loop iterations")
    repair_successful: bool = Field(default=False, description="Whether repair fixed all issues")

    # ── Pipeline stages ────────────────────────────────────
    stage_results: list[StageResult] = Field(
        default_factory=list,
        description="Per-stage execution results with timing (internal names)",
    )
    stage_details: list[StageDetail] = Field(
        default_factory=list,
        description="Per-stage enhanced details for frontend (frontend names, reasoning, findings, snapshot)",
    )
    total_duration_ms: float = Field(default=0.0, description="Total pipeline execution time")

    # ── Test Files ─────────────────────────────────────────
    test_files: list[TestFileEntry] = Field(
        default_factory=list,
        description="All generated test files with content and metadata",
    )
    compile_results: list[CompileResult] = Field(default_factory=list)
    compile_summary: CompileSummary = Field(default_factory=CompileSummary)
    failed_files: list[str] = Field(default_factory=list)
    toolchain: str = ""
    generation_mode: str = "rule_based"
    generation_trace: list[str] = Field(default_factory=list)
    budget: dict[str, Any] = Field(default_factory=dict)
    required_features: list[str] = Field(default_factory=list)
    canonical_targets: list[dict[str, Any]] = Field(default_factory=list)
    scenario_plan: list[dict[str, Any]] = Field(default_factory=list)

    # ── Metadata ───────────────────────────────────────────
    generated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 timestamp of report generation",
    )
    instruction_profile_summary: dict[str, Any] = Field(
        default_factory=dict,
        description="Compact instruction metadata (class, encoding_count, operand_count, features)",
    )
    test_plan_summary: str = Field(default="", description="Test plan summary from planning stage")
    plan_reasoning: str = Field(default="", description="Planning stage reasoning chain")
    test_suite_preview: str = Field(default="", description="First 2000 chars of generated test suite (deprecated, use test_files)")
    test_suite_full: str = Field(default="", description="Full generated test suite content")

    # ── Serialization ──────────────────────────────────────

    def to_markdown(self) -> str:
        """Render as a Markdown verification report."""
        status_icon = {"PASS": "[PASS]", "FAIL": "[FAIL]", "REPAIRED": "[REPAIRED]", "ERROR": "[ERROR]"}.get(
            self.status, "[?]"
        )
        lines: list[str] = [
            f"# {status_icon} Compiler Verification Report: `{self.instruction}`",
            "",
            "## Summary",
            f"| Metric                | Value                          |",
            f"|-----------------------|--------------------------------|",
            f"| Instruction           | `{self.instruction}`           |",
            f"| Status                | **{self.status}**              |",
            f"| Generated Tests       | {self.generated_tests}         |",
            f"| Review Score          | {self.review_score:.0f}/100    |",
            f"| Review Passed         | {self.review_passed}           |",
            f"| Repair Attempts       | {self.repair_attempts}         |",
            f"| Repair Successful     | {self.repair_successful}       |",
            f"| Total Duration        | {self.total_duration_ms:.0f}ms |",
            f"| Generated At          | {self.generated_at}            |",
            "",
            "## Coverage",
            f"| Dimension  | Coverage  |",
            f"|------------|-----------|",
            f"| normal     | {self.coverage.normal:.0f}%     |",
            f"| boundary   | {self.coverage.boundary:.0f}%   |",
            f"| encoding   | {self.coverage.encoding:.0f}%   |",
            f"| alias      | {self.coverage.alias:.0f}%      |",
            f"| invalid    | {self.coverage.invalid:.0f}%    |",
            f"| feature    | {self.coverage.feature:.0f}%    |",
            f"| **Overall**| **{self.coverage.overall:.0f}%**|",
            "",
            "## Pipeline Stages",
            "| Stage              | Status  | Duration   |",
            "|--------------------|---------|------------|",
        ]
        for sr in self.stage_results:
            status_mark = {"ok": "[OK]", "warning": "[WARN]", "error": "[ERR]", "skipped": "[SKIP]"}.get(
                sr.status, "[?]"
            )
            lines.append(f"| {sr.stage:<18} | {status_mark} | {sr.duration_ms:.0f}ms |")
        lines.append("")

        if self.issues:
            lines.append("## Issues Found")
            lines.append("| # | Type | Severity | Location | Description | Suggestion |")
            lines.append("|---|------|----------|----------|-------------|------------|")
            for i, iss in enumerate(self.issues, 1):
                lines.append(
                    f"| {i} | {iss.get('type','?')} | {iss.get('severity','?')} | "
                    f"{iss.get('location','-')} | {iss.get('description','')[:50]} | "
                    f"{iss.get('suggestion','')[:40]} |"
                )
            lines.append("")

        if self.suggestions:
            lines.append("## Suggestions")
            for s in self.suggestions:
                lines.append(f"- {s}")
            lines.append("")

        if self.test_plan_summary:
            lines.append("## Test Plan")
            lines.append(self.test_plan_summary[:1000])
            lines.append("")

        if self.test_suite_preview:
            lines.append("## Generated Test Suite (preview)")
            lines.append("```")
            lines.append(self.test_suite_preview[:2000])
            if len(self.test_suite_preview) > 2000:
                lines.append("... (truncated)")
            lines.append("```")
            lines.append("")

        return "\n".join(lines)

    def to_json_api(self) -> dict[str, Any]:
        """Export as JSON-serializable dict for API responses."""
        return self.model_dump(exclude_none=True)
