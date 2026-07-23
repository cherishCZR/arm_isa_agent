"""Verification module — Compiler Verification Agent for ARM ISA testcase generation, review & repair.

Provides:
- VerificationReport: Structured report with coverage, score, issues.
- CoverageBreakdown: Per-dimension coverage percentages.
- VerificationOrchestrator: One-shot pipeline orchestrator.
- run_verification: Convenience function for single-instruction verification.
"""

from arm_isa_agent.verification.models import (
    CoverageBreakdown,
    StageResult,
    VerificationReport,
)

__all__ = [
    "VerificationReport",
    "CoverageBreakdown",
    "StageResult",
    "VerificationOrchestrator",
    "run_verification",
]


def __getattr__(name: str):
    if name in {"VerificationOrchestrator", "run_verification"}:
        from arm_isa_agent.verification.orchestrator import VerificationOrchestrator, run_verification

        return {
            "VerificationOrchestrator": VerificationOrchestrator,
            "run_verification": run_verification,
        }[name]
    raise AttributeError(name)
