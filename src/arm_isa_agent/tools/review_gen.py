"""Review generation tools — testcase review + repair with self-correction loop.

Tools:
- review_testcase: Review a generated test suite against 5 dimensions.
- review_test_suite: Batch review multiple test suites.
- repair_testcase: Auto-repair failing testcases based on review feedback.
"""

from __future__ import annotations

import json
from typing import Any

import structlog

from arm_isa_agent.agent.tool_registry import get_llm, get_sqlite, register_tool
from arm_isa_agent.generation.models import TestCaseSuite
from arm_isa_agent.planning.analyzer import InstructionAnalyzer
from arm_isa_agent.review_generation.models import ReviewResult
from arm_isa_agent.review_generation.reviewer import RepairGenerator, TestcaseReviewer

logger = structlog.get_logger(__name__)


# ═══════════════════════════════════════════════════════════════
# Tool: review_testcase — review a generated test suite
# ═══════════════════════════════════════════════════════════════

@register_tool(
    "review_testcase",
    "Review a generated ARM test suite for quality across 5 dimensions: "
    "syntax, constraint, encoding, semantic, and coverage. "
    "Returns a detailed ReviewResult with pass/fail, scores, issues, and suggestions. "
    "Use after generate_test_suite to verify test quality before delivery.",
)
def review_testcase(
    mnemonic: str,
    test_suite_json: str = "",
    use_llm: bool = False,
) -> str:
    """Review a generated test suite.

    Args:
        mnemonic: The instruction mnemonic (e.g. "ADD", "LDR").
        test_suite_json: JSON string of the TestCaseSuite to review.
                         If empty, will re-build suite from DB.
        use_llm: If True, use LLM for deeper analysis (slower but more thorough).

    Returns:
        Markdown review report with scores, issues, and suggestions.
    """
    try:
        llm = get_llm() if use_llm else None
        sqlite = get_sqlite()

        # Build profile from DB
        analyzer = InstructionAnalyzer(sqlite)
        profile = analyzer.extract_profile(mnemonic=mnemonic)
        if not profile or not profile.mnemonic:
            return json.dumps({
                "error": f"Instruction '{mnemonic}' not found in database.",
            }, ensure_ascii=False)

        # Parse or build test suite
        suite: TestCaseSuite
        if test_suite_json:
            try:
                data = json.loads(test_suite_json)
                suite = TestCaseSuite(**data)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to parse test_suite_json: {e}",
                }, ensure_ascii=False)
        else:
            # Build a minimal suite from profile for review
            from arm_isa_agent.generation.generators import TestCaseSuiteGenerator
            gen = TestCaseSuiteGenerator(llm=None, sqlite_client=sqlite)
            suite = gen.generate_suite(profile, use_llm=False)

        # Run review
        reviewer = TestcaseReviewer(llm)
        result: ReviewResult = reviewer.review(
            test_suite=suite,
            profile=profile,
            strategy=None,
            use_llm=use_llm,
        )

        return result.to_markdown()

    except Exception as e:
        logger.error("review_testcase.error", error=str(e)[:300])
        return json.dumps({
            "error": f"Review failed: {str(e)[:500]}",
        }, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════
# Tool: repair_testcase — fix failing testcases
# ═══════════════════════════════════════════════════════════════

@register_tool(
    "repair_testcase",
    "Auto-repair a failing test suite based on review feedback. "
    "Takes ReviewResult issues and attempts to fix syntax, constraint, encoding, "
    "and semantic errors. Supports up to 3 repair attempts in the self-correction loop. "
    "Use after review_testcase when the result is FAIL.",
)
def repair_testcase(
    mnemonic: str,
    review_result_json: str,
    test_suite_json: str = "",
    attempt: int = 1,
) -> str:
    """Auto-repair a failing test suite.

    Args:
        mnemonic: The instruction mnemonic.
        review_result_json: JSON string of the ReviewResult with issues.
        test_suite_json: JSON string of the original TestCaseSuite (optional).
        attempt: Current repair attempt number (1-based).

    Returns:
        Markdown report of repair changes and repaired content.
    """
    try:
        llm = get_llm()
        sqlite = get_sqlite()

        # Parse review result
        try:
            review_data = json.loads(review_result_json)
            review_result = ReviewResult(**review_data)
        except Exception as e:
            return json.dumps({
                "error": f"Failed to parse review_result_json: {e}",
            }, ensure_ascii=False)

        # Build profile
        analyzer = InstructionAnalyzer(sqlite)
        profile = analyzer.extract_profile(mnemonic=mnemonic)
        if not profile or not profile.mnemonic:
            return json.dumps({
                "error": f"Instruction '{mnemonic}' not found.",
            }, ensure_ascii=False)

        # Parse or build test suite
        suite: TestCaseSuite
        if test_suite_json:
            try:
                data = json.loads(test_suite_json)
                suite = TestCaseSuite(**data)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to parse test_suite_json: {e}",
                }, ensure_ascii=False)
        else:
            from arm_isa_agent.generation.generators import TestCaseSuiteGenerator
            gen = TestCaseSuiteGenerator(llm=llm, sqlite_client=sqlite)
            suite = gen.generate_suite(profile, use_llm=False)

        # Run repair
        repair_gen = RepairGenerator(llm, max_repair_attempts=3)
        repair_result = repair_gen.repair(review_result, suite, profile)

        # Format output
        lines: list[str] = []
        lines.append(f"# Repair Report — `{mnemonic.upper()}` (Attempt {attempt}/3)")
        lines.append("")
        lines.append(f"**Status:** {'✅ Repaired' if repair_result.repaired else '❌ Repair Failed'}")
        lines.append(f"**Issues addressed:** {len(review_result.issues)}")
        lines.append("")

        if repair_result.repair_changes:
            lines.append("## Changes Made")
            for i, ch in enumerate(repair_result.repair_changes, 1):
                lines.append(f"{i}. {ch}")
            lines.append("")

        if repair_result.repair_notes:
            lines.append("## Repair Notes")
            lines.append(repair_result.repair_notes)
            lines.append("")

        if repair_result.repaired_content:
            lines.append("## Repaired Content")
            lines.append("```")
            lines.append(repair_result.repaired_content[:5000])
            if len(repair_result.repaired_content) > 5000:
                lines.append(f"\n... (truncated, {len(repair_result.repaired_content)} total chars)")
            lines.append("```")
            lines.append("")

        if not repair_result.repaired:
            lines.append("## Unresolved Issues")
            for issue in repair_result.original_issues[:5]:
                lines.append(f"- [{issue.severity}] [{issue.type}] {issue.description}")
            lines.append("")
            if attempt >= 3:
                lines.append("⚠ **Max repair attempts (3) reached.** Manual review required.")

        return "\n".join(lines)

    except Exception as e:
        logger.error("repair_testcase.error", error=str(e)[:300])
        return json.dumps({
            "error": f"Repair failed: {str(e)[:500]}",
        }, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════
# Tool: review_test_suite — batch review
# ═══════════════════════════════════════════════════════════════

@register_tool(
    "review_test_suite",
    "Batch review multiple test suites for quality. "
    "Takes a list of mnemonics and runs review_testcase on each. "
    "Returns a summary report with pass/fail rates and overall quality score.",
)
def review_test_suite(mnemonics_json: str, use_llm: bool = False) -> str:
    """Batch review multiple test suites.

    Args:
        mnemonics_json: JSON array of mnemonic strings, e.g. '["ADD", "LDR", "SUB"]'.
        use_llm: If True, use LLM for deeper analysis.

    Returns:
        Batch review summary report.
    """
    try:
        mnemonics = json.loads(mnemonics_json)
        if not isinstance(mnemonics, list):
            return json.dumps({"error": "mnemonics_json must be a JSON array"}, ensure_ascii=False)

        llm = get_llm() if use_llm else None
        sqlite = get_sqlite()
        analyzer = InstructionAnalyzer(sqlite)

        results: list[dict[str, Any]] = []
        passed_count = 0
        total_issues = 0

        for mnem in mnemonics:
            try:
                profile = analyzer.extract_profile(mnemonic=mnem)
                if not profile or not profile.mnemonic:
                    results.append({
                        "mnemonic": mnem,
                        "error": "Not found in database",
                    })
                    continue

                # Build suite
                from arm_isa_agent.generation.generators import TestCaseSuiteGenerator
                gen = TestCaseSuiteGenerator(llm=None, sqlite_client=sqlite)
                suite = gen.generate_suite(profile, use_llm=False)

                # Review
                reviewer = TestcaseReviewer(llm)
                review = reviewer.review(suite, profile, use_llm=use_llm)

                results.append({
                    "mnemonic": mnem,
                    "passed": review.passed,
                    "score": review.score,
                    "high_issues": review.high_severity_count,
                    "medium_issues": review.medium_severity_count,
                    "low_issues": review.low_severity_count,
                    "total_issues": review.total_issues,
                })

                if review.passed:
                    passed_count += 1
                total_issues += review.total_issues

            except Exception as e:
                results.append({
                    "mnemonic": mnem,
                    "error": str(e)[:200],
                })

        # Build summary
        total = len(mnemonics)
        lines: list[str] = []
        lines.append(f"# Batch Review Summary")
        lines.append(f"**Instructions:** {total}  |  **Passed:** {passed_count}/{total}  |  **Total Issues:** {total_issues}")
        lines.append("")

        lines.append("| Mnemonic | Status | Score | H | M | L |")
        lines.append("|----------|--------|-------|---|---|---|")
        for r in results:
            if "error" in r:
                lines.append(f"| {r['mnemonic']} | ❌ Error | - | - | - | - |")
            else:
                status = "✅ PASS" if r["passed"] else "❌ FAIL"
                lines.append(
                    f"| {r['mnemonic']} | {status} | {r['score']:.0f} "
                    f"| {r['high_issues']} | {r['medium_issues']} | {r['low_issues']} |"
                )
        lines.append("")

        return "\n".join(lines)

    except Exception as e:
        logger.error("review_test_suite.error", error=str(e)[:300])
        return json.dumps({"error": f"Batch review failed: {str(e)[:500]}"}, ensure_ascii=False)
