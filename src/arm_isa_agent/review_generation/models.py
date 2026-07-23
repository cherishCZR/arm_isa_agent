"""Reviewer data models — structured review results for all 5 dimensions."""

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════
# Review Issue
# ═══════════════════════════════════════════════════════════════

class ReviewIssue(BaseModel):
    """A single issue found during review."""

    type: Literal[
        "syntax_error",
        "constraint_error",
        "encoding_error",
        "semantic_error",
        "coverage_gap",
    ] = Field(description="Category of the issue")
    description: str = Field(description="Human-readable issue description")
    severity: Literal["high", "medium", "low"] = Field(description="Severity level")
    location: str = Field(
        default="",
        description="Where the issue occurs, e.g. 'line 5', 'instruction: ADD X0, X1, #999999'",
    )
    suggestion: str = Field(default="", description="How to fix the issue")
    dimension: str = Field(default="", description="Which review dimension found this")

    def to_markdown(self) -> str:
        emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(self.severity, "⚪")
        loc = f" `{self.location}`" if self.location else ""
        sug = f"\n  → **Fix:** {self.suggestion}" if self.suggestion else ""
        return f"- {emoji} **[{self.type}]**{loc}: {self.description}{sug}"


# ═══════════════════════════════════════════════════════════════
# Dimension Score
# ═══════════════════════════════════════════════════════════════

class DimensionScore(BaseModel):
    """Per-dimension review score."""

    dimension: Literal[
        "syntax",
        "constraint",
        "encoding",
        "semantic",
        "coverage",
    ] = Field(description="Review dimension name")
    score: float = Field(default=100.0, ge=0.0, le=100.0, description="Score 0-100")
    issues_count: int = Field(default=0, description="Number of issues found")
    max_severity: str = Field(default="none", description="Highest severity: high|medium|low|none")
    details: str = Field(default="", description="Human-readable dimension summary")


# ═══════════════════════════════════════════════════════════════
# Review Result — the core output model
# ═══════════════════════════════════════════════════════════════

class ReviewResult(BaseModel):
    """Complete review result for a test suite or individual testcase.

    This is the core output of the TestcaseReviewer agent, consumed by the
    LangGraph decision node to decide pass/fail and trigger repair loops.

    JSON Schema (for serialization):
    {
      "passed": true | false,
      "score": 0-100,
      "dimension_scores": [...],
      "issues": [...],
      "suggestions": [...],
      "reviewer_notes": "..."
    }
    """

    passed: bool = Field(
        default=False,
        description="Overall pass/fail. Pass if score >= threshold and no high-severity issues.",
    )
    score: float = Field(default=100.0, ge=0.0, le=100.0, description="Overall score 0-100")

    # Per-dimension breakdown
    dimension_scores: list[DimensionScore] = Field(
        default_factory=list,
        description="Scores for each of the 5 review dimensions",
    )

    # Issue collection
    issues: list[ReviewIssue] = Field(
        default_factory=list,
        description="All issues found across all dimensions",
    )

    # Actionable suggestions
    suggestions: list[str] = Field(
        default_factory=list,
        description="Concrete suggestions for fixing issues",
    )

    # Metadata
    reviewer_notes: str = Field(default="", description="Overall reviewer commentary")
    instruction_mnemonic: str = Field(default="", description="Target instruction")
    review_timestamp: str = Field(default="", description="ISO timestamp of review")

    # ── Derived properties ──────────────────────────────────

    @property
    def high_severity_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "high")

    @property
    def medium_severity_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "medium")

    @property
    def low_severity_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "low")

    @property
    def total_issues(self) -> int:
        return len(self.issues)

    def _compute_passed(self, pass_threshold: float = 70.0) -> bool:
        """Compute pass/fail from score and issues."""
        if self.score < pass_threshold:
            return False
        if self.high_severity_count > 0:
            return False
        return True

    def model_post_init(self, __context: Any) -> None:
        """Auto-compute passed flag if not explicitly set."""
        # Only auto-compute if issues exist; otherwise trust the caller
        if self.issues and self.passed:
            # Re-check: any high severity → fail
            self.passed = self._compute_passed()

    # ── Serialization ───────────────────────────────────────

    def to_markdown(self) -> str:
        """Render as a Markdown review report."""
        lines: list[str] = []
        status_icon = "✅" if self.passed else "❌"
        lines.append(f"# {status_icon} Testcase Review Report")
        if self.instruction_mnemonic:
            lines.append(f"**Instruction:** `{self.instruction_mnemonic}`")
        lines.append(f"**Score:** {self.score:.0f}/100  |  **Result:** {'PASS' if self.passed else 'FAIL'}")
        lines.append(f"**Issues:** {self.total_issues} "
                     f"(🔴 {self.high_severity_count} high, "
                     f"🟡 {self.medium_severity_count} medium, "
                     f"🟢 {self.low_severity_count} low)")
        lines.append("")

        # Dimension scores table
        lines.append("## Dimension Scores")
        lines.append("| Dimension | Score | Issues | Max Severity |")
        lines.append("|-----------|-------|--------|-------------|")
        for ds in self.dimension_scores:
            lines.append(f"| {ds.dimension} | {ds.score:.0f} | {ds.issues_count} | {ds.max_severity} |")
        lines.append("")

        # Detailed issues
        if self.issues:
            lines.append("## Issues Found")
            for issue in self.issues:
                lines.append(issue.to_markdown())
            lines.append("")

        # Suggestions
        if self.suggestions:
            lines.append("## Suggestions")
            for s in self.suggestions:
                lines.append(f"- {s}")
            lines.append("")

        if self.reviewer_notes:
            lines.append("## Reviewer Notes")
            lines.append(self.reviewer_notes)
            lines.append("")

        return "\n".join(lines)

    def to_json_report(self) -> dict[str, Any]:
        """Export as a JSON-serializable dict for API responses."""
        return self.model_dump(exclude_none=True)

    def to_compact_report(self) -> str:
        """Single-line compact report for logging."""
        status = "PASS" if self.passed else "FAIL"
        return (
            f"[{status}] score={self.score:.0f} "
            f"issues={self.total_issues} "
            f"(H:{self.high_severity_count} M:{self.medium_severity_count} L:{self.low_severity_count})"
        )


# ═══════════════════════════════════════════════════════════════
# Repair Result
# ═══════════════════════════════════════════════════════════════

class RepairResult(BaseModel):
    """Result of a repair operation on a failing testcase."""

    repaired: bool = Field(description="Whether repair was successful")
    original_issues: list[ReviewIssue] = Field(default_factory=list)
    repaired_content: str = Field(default="", description="The repaired test content")
    repair_changes: list[str] = Field(
        default_factory=list,
        description="Description of each change made",
    )
    repair_notes: str = Field(default="", description="Repair process notes")
