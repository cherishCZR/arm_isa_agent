"""VerificationOrchestrator — Full Compiler Verification Pipeline.

Pipeline:
    Retrieval → Constraint Analysis → Test Planning → Test Generation → Review + Repair Loop → Report

Usage:
    orchestrator = VerificationOrchestrator(sqlite_client, llm)
    report = orchestrator.verify("ADD")
    print(report.to_markdown())

SSE Streaming:
    async for event_str in orchestrator.verify_stream("ADD"):
        # event_str is a complete SSE message (event + data lines)
        yield event_str
"""

from __future__ import annotations

import asyncio
import json
import time
from typing import Any, AsyncGenerator, Optional

import structlog

from arm_isa_agent.assembly.scenario import ScenarioProgramGenerator, ScenarioRequest, make_assembly_symbol
from arm_isa_agent.assembly.single_suite import SingleInstructionSuiteGenerator
from arm_isa_agent.compile.verifier import CompileVerifier
from arm_isa_agent.generation.generators import TestCaseSuiteGenerator
from arm_isa_agent.generation.models import TestCaseSuite
from arm_isa_agent.planning.analyzer import InstructionAnalyzer
from arm_isa_agent.planning.models import InstructionProfile, PlanOutput, TestStrategy
from arm_isa_agent.planning.planner import InstructionPlanner
from arm_isa_agent.review_generation.models import RepairResult, ReviewResult
from arm_isa_agent.review_generation.reviewer import RepairGenerator, TestcaseReviewer
from arm_isa_agent.verification.models import (
    CoverageBreakdown,
    INTERNAL_TO_FRONTEND_STAGE,
    PipelineStage,
    SSEBatchComplete,
    SSEBatchStart,
    SSEInstructionComplete,
    SSEInstructionStart,
    SSEResult,
    SSEStageComplete,
    SSEStageProgress,
    SSEStageStart,
    StageDetail,
    StageResult,
    TestFileEntry,
    VerificationReport,
)

logger = structlog.get_logger(__name__)

# Safety limits
MAX_REPAIR_ATTEMPTS = 3


class VerificationOrchestrator:
    """One-shot compiler verification pipeline for ARM instructions.

    Runs the full pipeline:
        1. Instruction Retrieval (profile loading)
        2. Constraint Analysis
        3. Test Planning
        4. Test Generation (8 test formats)
        5. Test Review (5 dimensions)
        6. Repair Loop (max 3 iterations)
        7. Verification Report generation

    Usage:
        orchestrator = VerificationOrchestrator(sqlite_client, llm)
        report = orchestrator.verify("ADD")
    """

    def __init__(
        self,
        sqlite_client: Any = None,
        llm: Any = None,
        use_llm_planning: bool = False,
        use_llm_review: bool = False,
    ) -> None:
        self._sqlite = sqlite_client
        self._llm = llm
        self._use_llm_planning = use_llm_planning
        self._use_llm_review = use_llm_review

        # Lazy init
        self._analyzer: Optional[InstructionAnalyzer] = None
        self._planner: Optional[InstructionPlanner] = None
        self._generator: Optional[TestCaseSuiteGenerator] = None
        self._reviewer: Optional[TestcaseReviewer] = None
        self._repairer: Optional[RepairGenerator] = None

    # ── Lazy component initialization ──────────────────────────

    @property
    def analyzer(self) -> InstructionAnalyzer:
        if self._analyzer is None:
            self._analyzer = InstructionAnalyzer(self._sqlite)
        return self._analyzer

    @property
    def planner(self) -> InstructionPlanner:
        if self._planner is None:
            self._planner = InstructionPlanner(self._sqlite, self._llm)
        return self._planner

    @property
    def generator(self) -> TestCaseSuiteGenerator:
        if self._generator is None:
            self._generator = TestCaseSuiteGenerator(llm=self._llm, sqlite_client=self._sqlite)
        return self._generator

    @property
    def reviewer(self) -> TestcaseReviewer:
        if self._reviewer is None:
            self._reviewer = TestcaseReviewer(self._llm)
        return self._reviewer

    @property
    def repairer(self) -> RepairGenerator:
        if self._repairer is None:
            self._repairer = RepairGenerator(self._llm, max_repair_attempts=MAX_REPAIR_ATTEMPTS)
        return self._repairer

    # ── Main pipeline ──────────────────────────────────────────

    def verify(
        self,
        instruction: str,
        use_llm: bool = False,
        instruction_count: int = 100,
        target_instruction_count: int = 1,
    ) -> VerificationReport:
        """Run the full compiler verification pipeline for a single instruction.

        Args:
            instruction: ARM instruction mnemonic, e.g. "ADD", "LDR", "STP".
            use_llm: If True, use LLM for test generation (default: rule-based).
            instruction_count: Target number of instruction instances per test program.

        Returns:
            VerificationReport with coverage, score, issues, and stage timing.
        """
        return self._verify_single_instruction_program(
            instruction,
            use_llm=use_llm,
            program_instruction_count=instruction_count,
            target_instruction_count=target_instruction_count,
        )

    def _verify_legacy_suite(
        self,
        instruction: str,
        use_llm: bool = False,
        instruction_count: int = 100,
    ) -> VerificationReport:
        """Legacy 8-format suite verification path.

        Kept for reference artifacts and future optional outputs. The default
        single-instruction path now uses the same XML-driven assembly program
        generator as scenario batch verification.
        """
        t_start = time.perf_counter()
        stage_results: list[StageResult] = []
        profile: Optional[InstructionProfile] = None
        strategy: Optional[TestStrategy] = None
        suite: Optional[TestCaseSuite] = None
        review_result: Optional[ReviewResult] = None
        repair_count = 0
        repair_successful = False

        logger.info("verification.start", instruction=instruction)

        # ═══════════════════════════════════════════════════════
        # Stage 1: Instruction Retrieval
        # ═══════════════════════════════════════════════════════
        t_s1 = time.perf_counter()
        try:
            profile = self.analyzer.extract_profile(mnemonic=instruction)
            if profile is None:
                return self._error_report(
                    instruction, "Instruction not found in knowledge base", stage_results
                )
            stage_results.append(StageResult(
                stage="retrieval",
                status="ok",
                duration_ms=(time.perf_counter() - t_s1) * 1000,
                output_summary=(
                    f"Loaded profile: {profile.mnemonic}, class={profile.instr_class}, "
                    f"encodings={profile.encoding_count}, operands={profile.operand_count}, "
                    f"complexity={profile.complexity_score}/10"
                ),
            ))
            logger.info("verification.retrieval_done", mnemonic=profile.mnemonic)
        except Exception as e:
            stage_results.append(StageResult(
                stage="retrieval", status="error",
                duration_ms=(time.perf_counter() - t_s1) * 1000,
                error=str(e)[:300],
            ))
            return self._error_report(instruction, f"Retrieval failed: {str(e)[:200]}", stage_results)

        # ═══════════════════════════════════════════════════════
        # Stage 2: Constraint Analysis
        # ═══════════════════════════════════════════════════════
        t_s2 = time.perf_counter()
        try:
            constraint_count = len(profile.constrained_unpredictable)
            feature_count = len(profile.feature_dependencies)
            encoding_undef_count = len(profile.encoding_undefined)

            constraint_details: list[str] = []
            if constraint_count > 0:
                constraint_details.append(f"{constraint_count} UNPREDICTABLE constraints")
            if feature_count > 0:
                constraint_details.append(
                    f"{feature_count} feature deps ({', '.join(fd.feature_name for fd in profile.feature_dependencies[:3])})"
                )
            if encoding_undef_count > 0:
                constraint_details.append(f"{encoding_undef_count} encoding undefined")
            if profile.has_shift_extend:
                constraint_details.append("shift/extend variants")
            if profile.affects_flags:
                constraint_details.append("affects NZCV flags")

            summary = "; ".join(constraint_details) if constraint_details else "No special constraints"
            stage_results.append(StageResult(
                stage="constraint_analysis",
                status="ok",
                duration_ms=(time.perf_counter() - t_s2) * 1000,
                output_summary=summary,
            ))
            logger.info("verification.constraint_analysis_done", details=summary)
        except Exception as e:
            stage_results.append(StageResult(
                stage="constraint_analysis", status="warning",
                duration_ms=(time.perf_counter() - t_s2) * 1000,
                error=str(e)[:200],
            ))

        # ═══════════════════════════════════════════════════════
        # Stage 3: Test Planning
        # ═══════════════════════════════════════════════════════
        t_s3 = time.perf_counter()
        plan_output: Optional[PlanOutput] = None
        try:
            plan_result = self.planner.plan(
                mnemonic=instruction,
                user_goal=f"Comprehensive verification of {instruction}",
                use_llm=self._use_llm_planning,
            )
            if plan_result.get("status") == "ok":
                strategy = plan_result.get("strategy")
                if isinstance(strategy, TestStrategy):
                    plan_output = PlanOutput(
                        instruction=profile,
                        strategy=strategy,
                        reasoning=plan_result.get("reasoning", ""),
                        test_plan_summary=plan_result.get("plan_markdown", ""),
                    )

            dim_names = [d.name for d in (strategy.dimensions if strategy else [])]
            stage_results.append(StageResult(
                stage="test_planning",
                status="ok" if strategy else "warning",
                duration_ms=(time.perf_counter() - t_s3) * 1000,
                output_summary=(
                    f"Plan: {strategy.total_test_count} tests, "
                    f"{len(dim_names)} dimensions: {', '.join(dim_names[:5])}"
                    if strategy else "No strategy generated — using defaults"
                ),
            ))
            logger.info("verification.planning_done", dims=len(dim_names) if strategy else 0)
        except Exception as e:
            stage_results.append(StageResult(
                stage="test_planning", status="warning",
                duration_ms=(time.perf_counter() - t_s3) * 1000,
                error=str(e)[:200],
                output_summary="Using default test strategy",
            ))

        # ═══════════════════════════════════════════════════════
        # Stage 4: Test Generation
        # ═══════════════════════════════════════════════════════
        t_s4 = time.perf_counter()
        try:
            suite = self.generator.generate_suite(
                profile=profile,
                use_llm=use_llm,
                instruction_count=instruction_count,
            )
            stage_results.append(StageResult(
                stage="test_generation",
                status="ok",
                duration_ms=(time.perf_counter() - t_s4) * 1000,
                output_summary=f"Generated {suite.total_tests} test cases across {len([c for c in suite.test_counts_by_type.values() if c > 0])} formats",
            ))
            logger.info("verification.generation_done", total_tests=suite.total_tests)
        except Exception as e:
            stage_results.append(StageResult(
                stage="test_generation", status="error",
                duration_ms=(time.perf_counter() - t_s4) * 1000,
                error=str(e)[:300],
            ))
            return self._error_report(instruction, f"Test generation failed: {str(e)[:200]}", stage_results)

        # ═══════════════════════════════════════════════════════
        # Stage 5: Test Review
        # ═══════════════════════════════════════════════════════
        t_s5 = time.perf_counter()
        try:
            review_result = self.reviewer.review(
                test_suite=suite,
                profile=profile,
                strategy=strategy,
                use_llm=self._use_llm_review,
            )
            stage_results.append(StageResult(
                stage="test_review",
                status="ok" if review_result.passed else "warning",
                duration_ms=(time.perf_counter() - t_s5) * 1000,
                output_summary=(
                    f"{'PASS' if review_result.passed else 'FAIL'} | "
                    f"Score: {review_result.score:.0f}/100 | "
                    f"Issues: {review_result.total_issues} "
                    f"(H:{review_result.high_severity_count} "
                    f"M:{review_result.medium_severity_count} "
                    f"L:{review_result.low_severity_count})"
                ),
            ))
            logger.info(
                "verification.review_done",
                passed=review_result.passed,
                score=review_result.score,
                issues=review_result.total_issues,
            )
        except Exception as e:
            stage_results.append(StageResult(
                stage="test_review", status="error",
                duration_ms=(time.perf_counter() - t_s5) * 1000,
                error=str(e)[:300],
            ))
            return self._error_report(instruction, f"Test review failed: {str(e)[:200]}", stage_results)

        # ═══════════════════════════════════════════════════════
        # Stage 6: Repair Loop (max 3 attempts)
        # ═══════════════════════════════════════════════════════
        t_s6 = time.perf_counter()
        last_review = review_result

        while not last_review.passed and repair_count < MAX_REPAIR_ATTEMPTS:
            # Check if there are fixable issues
            fixable_types = {"syntax_error", "constraint_error", "encoding_error", "semantic_error"}
            has_fixable = any(
                i.type in fixable_types and i.severity in ("high", "medium")
                for i in last_review.issues
            )
            if not has_fixable:
                logger.info("verification.repair_skip", reason="no fixable issues")
                break

            repair_count += 1
            logger.info("verification.repair_attempt", attempt=repair_count)

            try:
                repair_result: RepairResult = self.repairer.repair(
                    review_result=last_review,
                    test_suite=suite,
                    profile=profile,
                )

                if repair_result.repaired:
                    # Re-generate suite with repairs
                    suite = self.generator.generate_suite(
                        profile=profile,
                        use_llm=True,  # Use LLM for repaired generation
                    )

                    # Re-review
                    last_review = self.reviewer.review(
                        test_suite=suite,
                        profile=profile,
                        strategy=strategy,
                        use_llm=self._use_llm_review,
                    )

                    if last_review.passed:
                        repair_successful = True
                        logger.info("verification.repair_success", attempt=repair_count)
                else:
                    logger.warning("verification.repair_not_possible", attempt=repair_count)
                    break

            except Exception as e:
                logger.error("verification.repair_error", attempt=repair_count, error=str(e)[:200])
                break

        stage_results.append(StageResult(
            stage="repair",
            status="ok" if repair_successful else ("skipped" if repair_count == 0 else "warning"),
            duration_ms=(time.perf_counter() - t_s6) * 1000,
            output_summary=(
                f"Repaired successfully after {repair_count} attempt(s)"
                if repair_successful else
                f"Repair attempted {repair_count} time(s), not fully resolved"
                if repair_count > 0 else
                "No repair needed"
            ),
        ))

        # ── Build final report ────────────────────────────────
        review_score = last_review.score if last_review else 0.0
        review_passed = last_review.passed if last_review else False

        # Determine overall status
        if review_passed and repair_count == 0:
            overall_status = "PASS"
        elif review_passed and repair_count > 0:
            overall_status = "REPAIRED"
        elif not review_passed:
            overall_status = "FAIL"
        else:
            overall_status = "ERROR"

        # Compute coverage
        coverage = self._compute_coverage(suite, profile, strategy)

        # Build issues list
        issues_list: list[dict[str, Any]] = []
        if last_review:
            for issue in last_review.issues:
                issues_list.append({
                    "type": issue.type,
                    "severity": issue.severity,
                    "description": issue.description,
                    "location": issue.location,
                    "suggestion": issue.suggestion,
                    "dimension": issue.dimension,
                })

        # Profile summary
        profile_summary: dict[str, Any] = {
            "mnemonic": profile.mnemonic,
            "title": profile.title,
            "instr_class": profile.instr_class,
            "encoding_count": profile.encoding_count,
            "operand_count": profile.operand_count,
            "complexity": profile.complexity_score,
            "feature_deps": [f.feature_name for f in profile.feature_dependencies],
            "is_alias": profile.is_alias,
            "affects_flags": profile.affects_flags,
        }

        # Test suite preview
        suite_preview = suite.to_markdown_summary() if suite else ""

        # Build stage_details for frontend (from stage_results)
        stage_details: list[StageDetail] = []
        for sr in stage_results:
            fe_stage = self._frontend_stage(sr.stage)
            stage_details.append(StageDetail(
                stage=fe_stage,
                status=sr.status,  # type: ignore[arg-type]
                duration_ms=sr.duration_ms,
                summary=sr.output_summary,
                error=sr.error,
            ))

        # Build test_files from suite
        test_files_raw = suite.to_test_file_entries() if suite else []
        issue_locations = {i.get("location", "") for i in issues_list}
        for tf in test_files_raw:
            if tf["file_id"] in issue_locations:
                tf["status"] = "fail"
                tf["issue_count"] = sum(1 for i in issues_list if i.get("location") == tf["file_id"])
        passing = sum(1 for tf in test_files_raw if tf["status"] == "pass")
        failing = sum(1 for tf in test_files_raw if tf["status"] == "fail")

        # Convert to TestFileEntry objects
        test_file_entries = [TestFileEntry(**tf) for tf in test_files_raw]
        compile_summary = CompileVerifier().verify_files(test_files_raw)
        failed_files = [
            r.filename for r in compile_summary.results
            if r.status == "FAIL"
        ]
        verification_level = (
            "compiled" if compile_summary.status == "PASS"
            else "statically_reviewed" if review_passed
            else "generated"
        )
        generated_status = "PASS" if suite and suite.total_tests > 0 else "FAIL"
        static_review_status = "PASS" if review_passed else "FAIL"
        compile_status = (
            "PASS" if compile_summary.status == "PASS"
            else "FAIL" if compile_summary.status == "FAIL"
            else "SKIPPED"
        )
        if compile_summary.status == "PASS":
            overall_status = "COMPILED"
        elif compile_summary.status == "FAIL":
            overall_status = "FAILED"
        elif review_passed:
            overall_status = "REVIEWED"

        total_ms = (time.perf_counter() - t_start) * 1000

        report = VerificationReport(
            instruction=instruction,
            status=overall_status,
            generated_tests=suite.total_tests if suite else 0,
            passing_test_count=passing,
            failing_test_count=failing,
            coverage=coverage,
            review_score=review_score,
            review_passed=review_passed,
            issues=issues_list,
            suggestions=last_review.suggestions if last_review else [],
            repair_attempts=repair_count,
            repair_successful=repair_successful,
            stage_results=stage_results,
            stage_details=stage_details,
            test_files=test_file_entries,
            verification_level=verification_level,  # type: ignore[arg-type]
            generated_status=generated_status,  # type: ignore[arg-type]
            static_review_status=static_review_status,  # type: ignore[arg-type]
            compile_status=compile_status,  # type: ignore[arg-type]
            compile_results=compile_summary.results,
            compile_summary=compile_summary,
            failed_files=failed_files,
            toolchain=(compile_summary.results[0].toolchain if compile_summary.results else ""),
            total_duration_ms=total_ms,
            instruction_profile_summary=profile_summary,
            test_plan_summary=plan_output.test_plan_summary if plan_output else "",
            plan_reasoning=plan_output.reasoning if plan_output else "",
            test_suite_preview=suite_preview[:2000],
            test_suite_full=suite_preview,
        )

        logger.info(
            "verification.complete",
            instruction=instruction,
            status=overall_status,
            score=review_score,
            tests=report.generated_tests,
            duration_ms=total_ms,
        )

        return report

    # ── Helpers ───────────────────────────────────────────────

    def _compute_coverage(
        self,
        suite: TestCaseSuite,
        profile: InstructionProfile,
        strategy: Optional[TestStrategy],
    ) -> CoverageBreakdown:
        """Estimate coverage percentages based on generated tests vs plan dimensions."""
        try:
            normal_tests = len(suite.assembly_tests)
            llvm_tests = len(suite.llvm_mc_tests)
            inline_tests = len(suite.inline_asm_tests)
            boundary_tests = len(suite.boundary_tests)
            alias_tests = len(suite.alias_tests)
            invalid_tests = len(suite.invalid_operand_tests)
            feature_tests = len(suite.feature_enable_tests)

            # Normal coverage: based on assembly + llvm_mc + inline_asm counts
            normal_cov = min(100,
                (normal_tests > 0) * 40 + (llvm_tests > 0) * 30 + (inline_tests > 0) * 30)

            # Boundary: if we have boundary tests and immediate ranges
            boundary_cov = 100 if boundary_tests >= 3 else (
                66 if boundary_tests >= 1 else 0
            )
            if not profile.immediate_ranges:
                boundary_cov = 0 if boundary_tests == 0 else 80

            # Alias: if instruction is an alias or has aliases
            if profile.is_alias:
                alias_cov = 100 if alias_tests >= 1 else 50
            else:
                alias_cov = 0  # N/A for non-alias instructions

            # Invalid operand
            invalid_cov = 100 if invalid_tests >= 2 else (50 if invalid_tests >= 1 else 0)
            if not profile.constrained_unpredictable and not profile.encoding_undefined:
                invalid_cov = 100 if invalid_tests >= 1 else 0

            # Feature
            feature_cov = 100 if feature_tests >= 1 else 0
            if not profile.feature_dependencies:
                feature_cov = 100  # N/A → full mark

            # Encoding
            encoding_cov = min(100, profile.encoding_count * 20 * (1 if normal_tests > 0 else 0.5))

            # Adjust from strategy dimensions if available
            if strategy:
                for dim in strategy.dimensions:
                    if dim.name == "Boundary" and dim.coverage_percentage > 0:
                        boundary_cov = max(boundary_cov, dim.coverage_percentage)
                    elif dim.name == "Encoding" and dim.coverage_percentage > 0:
                        encoding_cov = max(encoding_cov, dim.coverage_percentage)

            return CoverageBreakdown(
                normal=min(100.0, normal_cov),
                boundary=min(100.0, boundary_cov),
                encoding=min(100.0, encoding_cov),
                alias=min(100.0, alias_cov),
                invalid=min(100.0, invalid_cov),
                feature=min(100.0, feature_cov),
            )
        except Exception:
            return CoverageBreakdown()

    def _verify_single_instruction_program(
        self,
        instruction: str,
        use_llm: bool = False,
        program_instruction_count: int = 100,
        target_instruction_count: int = 1,
    ) -> VerificationReport:
        """Verify one instruction using XML scenario suites or LLM assembly generation."""
        if not use_llm:
            return self._verify_single_rule_suite(
                instruction,
                program_instruction_count=program_instruction_count,
                target_instruction_count=target_instruction_count,
            )
        t_start = time.perf_counter()
        raw = instruction.strip()
        if not raw:
            return self._error_report(instruction, "Instruction is empty", [])

        safe_id = make_assembly_symbol(raw, prefix="single_instruction")

        stage_results: list[StageResult] = []
        profile_summary: dict[str, Any] = {"query": raw}

        t_retrieval = time.perf_counter()
        try:
            generator = ScenarioProgramGenerator(self._sqlite, seed=1, llm=self._llm)
            program = generator.generate_and_verify(
                ScenarioRequest(
                    scenario_id=safe_id,
                    raw=raw,
                    queries=[] if use_llm else [raw],
                    program_instruction_count=program_instruction_count,
                    target_instruction_count=target_instruction_count,
                    generation_mode="llm" if use_llm else "rule_based",
                )
            )
        except Exception as exc:
            logger.exception("verification.single_program_failed", instruction=raw)
            stage_results.append(StageResult(
                stage="llm" if use_llm else "retrieval",
                status="error",
                duration_ms=(time.perf_counter() - t_retrieval) * 1000,
                output_summary="Failed to resolve or generate instruction program",
                error=str(exc),
            ))
            return self._error_report(raw, str(exc), stage_results)

        selected = program.resolved[0] if program.resolved else {}
        profile_summary.update({
            "mnemonic": selected.get("mnemonic", raw.split()[0].upper()),
            "xml_id": selected.get("xml_id", ""),
            "instr_class": selected.get("instr_class", ""),
            "feature_deps": selected.get("features", []),
            "resolved_query": selected.get("query", raw),
            "assembly": selected.get("assembly", ""),
        })

        stage_results.append(StageResult(
            stage="retrieval",
            status="ok" if program.resolved else "error",
            duration_ms=(time.perf_counter() - t_retrieval) * 1000,
            output_summary=(
                f"Resolved {raw} to {profile_summary.get('xml_id')}"
                if program.resolved else f"Could not resolve {raw}"
            ),
        ))
        stage_results.append(StageResult(
            stage="test_planning",
            status="ok",
            duration_ms=0.0,
            output_summary=(f"Program budget: {program_instruction_count}; target instances: {target_instruction_count}"),
        ))
        if use_llm:
            stage_results.append(StageResult(
                stage="llm",
                status="ok" if program.generated_status == "PASS" else "error",
                duration_ms=0.0,
                output_summary="; ".join(program.generation_trace) or "LLM generation did not complete",
            ))
        llm_failed = use_llm and program.generated_status != "PASS"
        stage_results.append(StageResult(
            stage="test_generation",
            status="skipped" if llm_failed else "ok" if program.generated_status == "PASS" else "error",
            duration_ms=0.0,
            output_summary=("Skipped because LLM generation failed" if llm_failed else f"Generated {program.test_file['filename'] if program.test_file else 'no file'}"),
        ))
        stage_results.append(StageResult(
            stage="test_review",
            status="skipped" if llm_failed else "ok" if program.static_review_status in {"PASS", "WARNING"} else "error",
            duration_ms=0.0,
            output_summary=("Skipped because LLM generation failed" if llm_failed else f"Static review {program.static_review_status.lower()}"),
        ))
        compile_stage_status = (
            "skipped" if llm_failed
            else "ok" if program.compile_status == "PASS"
            else "error" if program.compile_status == "FAIL"
            else "skipped"
        )
        stage_results.append(StageResult(
            stage="compile",
            status=compile_stage_status,
            duration_ms=0.0,
            output_summary=("Skipped because LLM generation failed" if llm_failed else f"Compile-only validation {program.compile_status.lower()}"),
        ))

        issues = list(program.issues)
        test_files_raw = [program.test_file] if program.test_file else []
        test_file_entries = [TestFileEntry(**tf) for tf in test_files_raw]
        compile_summary = program.compile_summary
        failed_files = [r.filename for r in compile_summary.results if r.status == "FAIL"]
        total_ms = (time.perf_counter() - t_start) * 1000

        coverage = CoverageBreakdown(
            normal=100.0 if program.generated_status == "PASS" else 0.0,
            encoding=100.0 if program.resolved else 0.0,
            feature=100.0,
        )
        stage_details = [
            StageDetail(
                stage=self._frontend_stage(sr.stage),
                status=sr.status,  # type: ignore[arg-type]
                duration_ms=sr.duration_ms,
                summary=sr.output_summary,
                error=sr.error,
            )
            for sr in stage_results
        ]
        result_event = program.to_result_event(total_ms)
        status = result_event["status"]
        verification_level = result_event["verification_level"]
        generated_status = result_event["generated_status"]
        static_review_status = result_event["static_review_status"]
        compile_status = result_event["compile_status"]

        return VerificationReport(
            instruction=raw,
            status=status,  # type: ignore[arg-type]
            verification_level=verification_level,  # type: ignore[arg-type]
            generated_status=generated_status,  # type: ignore[arg-type]
            static_review_status=static_review_status,  # type: ignore[arg-type]
            compile_status=compile_status,  # type: ignore[arg-type]
            generated_tests=program.program_instruction_count,
            passing_test_count=sum(1 for tf in test_files_raw if tf.get("status") == "pass"),
            failing_test_count=sum(1 for tf in test_files_raw if tf.get("status") == "fail"),
            coverage=coverage,
            review_score=result_event["review_score"],
            review_passed=program.static_review_status in {"PASS", "WARNING"},
            issues=issues,
            suggestions=[],
            repair_attempts=0,
            repair_successful=False,
            stage_results=stage_results,
            stage_details=stage_details,
            test_files=test_file_entries,
            compile_results=compile_summary.results,
            compile_summary=compile_summary,
            failed_files=failed_files,
            toolchain=(compile_summary.results[0].toolchain if compile_summary.results else ""),
            generation_mode=program.generation_mode,
            generation_trace=program.generation_trace,
            budget=result_event["budget"],
            required_features=program.required_features,
            canonical_targets=result_event["canonical_targets"],
            total_duration_ms=total_ms,
            instruction_profile_summary=profile_summary,
            test_plan_summary="Generate one standalone AArch64 assembly program and compile it against an exact instruction budget.",
            plan_reasoning=f"Generation mode: {program.generation_mode}; total instruction budget: {program.program_instruction_count}; target count: {program.target_instruction_count}.",
            test_suite_preview=(program.test_file or {}).get("content", "")[:2000],
            test_suite_full=(program.test_file or {}).get("content", ""),
        )

    def _verify_single_rule_suite(
        self,
        instruction: str,
        program_instruction_count: int,
        target_instruction_count: int,
    ) -> VerificationReport:
        """Generate a multi-file XML-derived suite for single-instruction rule mode."""
        started = time.perf_counter()
        raw = instruction.strip()
        if not raw:
            return self._error_report(instruction, "Instruction is empty", [])

        generator = SingleInstructionSuiteGenerator(self._sqlite, seed=1)
        suite = generator.generate_and_verify(raw, program_instruction_count, target_instruction_count)
        profile = suite.profile
        files = suite.test_files
        compile_summary = suite.compile_summary
        static_passed = bool(files) and not any(entry["status"] == "fail" and entry["issue_count"] for entry in files if entry["file_id"] not in {result.file_id for result in compile_summary.results if result.status == "FAIL"})
        generated_status = "PASS" if files else "FAIL"
        compile_status = compile_summary.status if files else "SKIPPED"
        static_status = "PASS" if static_passed else "FAIL" if files else "SKIPPED"
        status = "COMPILED" if compile_status == "PASS" and static_status == "PASS" else "FAILED"
        total_ms = (time.perf_counter() - started) * 1000
        failed_files = [result.filename for result in compile_summary.results if result.status == "FAIL"]
        categories = {entry["test_type"] for entry in files}
        features = [item.feature_name for item in profile.feature_dependencies] if profile else []

        stage_results = [
            StageResult(
                stage="retrieval",
                status="ok" if profile else "error",
                duration_ms=0.0,
                output_summary=f"Resolved {raw} to {profile.xml_id}" if profile else f"Could not resolve {raw}",
            ),
            StageResult(
                stage="test_planning",
                status="ok" if profile else "skipped",
                duration_ms=0.0,
                output_summary=f"Planned {len(suite.scenario_plan)} XML-applicable scenarios; each file budget {program_instruction_count}, target instances {target_instruction_count}",
            ),
            StageResult(
                stage="test_generation",
                status="ok" if generated_status == "PASS" else "error",
                duration_ms=0.0,
                output_summary=f"Generated {len(files)} scenario program file(s)",
            ),
            StageResult(
                stage="test_review",
                status="ok" if static_status == "PASS" else "error" if static_status == "FAIL" else "skipped",
                duration_ms=0.0,
                output_summary=f"Static review {static_status.lower()} for {len(files)} scenario file(s)",
            ),
            StageResult(
                stage="compile",
                status="ok" if compile_status == "PASS" else "error" if compile_status == "FAIL" else "skipped",
                duration_ms=sum(result.duration_ms for result in compile_summary.results),
                output_summary=f"Compile-only validation {compile_status.lower()}: {compile_summary.passed}/{compile_summary.total} files passed",
            ),
        ]
        stage_details = [
            StageDetail(
                stage=self._frontend_stage(stage.stage),
                status=stage.status,  # type: ignore[arg-type]
                duration_ms=stage.duration_ms,
                summary=stage.output_summary,
            )
            for stage in stage_results
        ]
        coverage = CoverageBreakdown(
            normal=100.0 if "normal_assembly" in categories else 0.0,
            boundary=100.0 if {"immediate_boundary", "shift_extend_boundary"} & categories else 0.0,
            encoding=100.0 if profile else 0.0,
            alias=100.0 if "register_aliasing" in categories else 0.0,
            feature=100.0 if not features or "extension_register_variation" in categories else 0.0,
        )
        budget = {
            "program_instruction_count": program_instruction_count,
            "target_instruction_count": target_instruction_count,
            "actual_instruction_count": program_instruction_count,
            "target_counts": {profile.xml_id: target_instruction_count} if profile else {},
            "per_scenario": True,
        }
        profile_summary = {
            "query": raw,
            "mnemonic": profile.mnemonic if profile else raw.split()[0].upper(),
            "xml_id": profile.xml_id if profile else "",
            "instr_class": profile.instr_class if profile else "",
            "feature_deps": features,
        }
        return VerificationReport(
            instruction=raw,
            status=status,  # type: ignore[arg-type]
            verification_level="compiled" if status == "COMPILED" else "generated",
            generated_status=generated_status,  # type: ignore[arg-type]
            static_review_status=static_status,  # type: ignore[arg-type]
            compile_status=compile_status,  # type: ignore[arg-type]
            generated_tests=len(files),
            passing_test_count=sum(entry["status"] == "pass" for entry in files),
            failing_test_count=sum(entry["status"] == "fail" for entry in files),
            coverage=coverage,
            review_score=(100.0 * compile_summary.passed / len(files)) if files else 0.0,
            review_passed=static_status == "PASS",
            issues=suite.issues,
            stage_results=stage_results,
            stage_details=stage_details,
            test_files=[TestFileEntry(**entry) for entry in files],
            compile_results=compile_summary.results,
            compile_summary=compile_summary,
            failed_files=failed_files,
            toolchain=compile_summary.results[0].toolchain if compile_summary.results else "",
            generation_mode="rule_based_suite",
            generation_trace=suite.trace,
            budget=budget,
            required_features=features,
            canonical_targets=[{"key": profile.xml_id, "query": raw, "aliases": [raw]}] if profile else [],
            scenario_plan=suite.scenario_plan,
            total_duration_ms=total_ms,
            instruction_profile_summary=profile_summary,
            test_plan_summary="XML-derived compile-only scenario suite; each scenario independently uses the requested instruction and target budgets.",
            plan_reasoning="; ".join(suite.trace),
            test_suite_preview=files[0]["content"][:2000] if files else "",
            test_suite_full="\n\n".join(entry["content"] for entry in files),
        )

    def _error_report(
        self,
        instruction: str,
        error_msg: str,
        stage_results: list[StageResult],
    ) -> VerificationReport:
        """Build an error VerificationReport when pipeline fails early."""
        return VerificationReport(
            instruction=instruction,
            status="ERROR",
            generated_tests=0,
            issues=[{"type": "orchestration_error", "severity": "high", "description": error_msg}],
            stage_results=stage_results,
            total_duration_ms=sum(sr.duration_ms for sr in stage_results),
        )

    # ── SSE / Streaming ────────────────────────────────────────

    @staticmethod
    def _sse(event: str, data: dict[str, Any] | BaseModel) -> str:
        """Format a single SSE message string.

        Args:
            event: SSE event name (stage_start, stage_progress, stage_complete, result, done, etc.)
            data: Dict or Pydantic model to serialize as JSON.

        Returns:
            Complete SSE message with event and data lines.
        """
        from pydantic import BaseModel as _BaseModel
        if isinstance(data, _BaseModel):
            payload = data.model_dump(exclude_none=True)
        else:
            payload = data
        return f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"

    @staticmethod
    def _frontend_stage(internal_stage: str) -> PipelineStage:
        """Map internal stage name to frontend-facing stage name."""
        return INTERNAL_TO_FRONTEND_STAGE.get(internal_stage, "planner")

    def _build_stage_detail(
        self,
        internal_stage: str,
        status: str,
        duration_ms: float,
        summary: str,
        reasoning: str = "",
        findings: list[str] | None = None,
        snapshot: dict[str, Any] | None = None,
        error: str = "",
    ) -> StageDetail:
        """Build a frontend-facing StageDetail from internal stage data."""
        fe_stage = self._frontend_stage(internal_stage)
        fe_status = status  # "ok"|"warning"|"error"|"skipped" maps directly
        return StageDetail(
            stage=fe_stage,
            status=fe_status,  # type: ignore[arg-type]
            duration_ms=duration_ms,
            summary=summary,
            reasoning=reasoning,
            key_findings=findings or [],
            data_snapshot=snapshot or {},
            error=error,
        )

    async def verify_stream(
        self,
        instruction: str,
        use_llm: bool = False,
        instruction_count: int = 100,
        target_instruction_count: int = 1,
    ) -> AsyncGenerator[str, None]:
        """Run verification with SSE event streaming.

        Yields SSE-formatted string messages for real-time frontend progress.
        Each yield is a complete SSE event: "event: xxx\\ndata: {...}\\n\\n"

        Args:
            instruction: ARM instruction mnemonic, e.g. "ADD".

        Yields:
            SSE event strings in sequence: stage_start → stage_progress → stage_complete → ... → result → done
        """
        t_start = time.perf_counter()
        stage_results: list[StageResult] = []
        stage_details: list[StageDetail] = []
        profile: Optional[InstructionProfile] = None
        strategy: Optional[TestStrategy] = None
        suite: Optional[TestCaseSuite] = None
        review_result: Optional[ReviewResult] = None
        repair_count = 0
        repair_successful = False
        plan_output: Optional[PlanOutput] = None

        instruction = instruction.strip() if use_llm else instruction.strip().upper()

        # ── Helper: emit stage_complete ──
        def _emit_stage_complete(
            internal: str, status_str: str, dur: float, summary_text: str,
            reasoning: str = "", findings: list[str] | None = None,
            snapshot: dict[str, Any] | None = None, error_text: str = "",
        ) -> str:
            fe_stage = self._frontend_stage(internal)
            findings = findings or []
            snapshot = snapshot or {}
            event_data = SSEStageComplete(
                stage=fe_stage,
                status=status_str,  # type: ignore[arg-type]
                duration_ms=dur,
                summary=summary_text,
                findings=findings,
                snapshot=snapshot,
            )
            detail = self._build_stage_detail(
                internal_stage=internal, status=status_str,
                duration_ms=dur, summary=summary_text,
                reasoning=reasoning, findings=findings,
                snapshot=snapshot, error=error_text,
            )
            stage_details.append(detail)
            return self._sse("stage_complete", event_data)

        logger.info("verification.stream.start", instruction=instruction)

        llm_stage_started = False
        if use_llm:
            llm_stage_started = True
            yield self._sse("stage_start", SSEStageStart(
                stage="llm",
                message="Calling LLM to extract targets and generate structured assembly...",
                instruction=instruction,
            ))
            yield self._sse("stage_progress", SSEStageProgress(
                stage="llm",
                detail="Waiting for structured target extraction and assembly response...",
                instruction=instruction,
            ))
        report = await asyncio.to_thread(
            self._verify_single_instruction_program,
            instruction,
            use_llm,
            instruction_count,
            target_instruction_count,
        )
        stage_map = [
            ("retrieval", "Resolving instruction variant..."),
            ("test_planning", "Planning compile-only assembly program..."),
            *(([("llm", "Calling LLM for structured assembly generation...")] if use_llm else [])),
            ("test_generation", "Generating assembly program..."),
            ("test_review", "Running static review..."),
            ("compile", "Compiling generated assembly..."),
        ]
        for internal, message in stage_map:
            frontend_stage = self._frontend_stage(internal)
            detail = next((sd for sd in report.stage_details if sd.stage == frontend_stage), None)
            if detail is None:
                status = "skipped"
                summary = "Not executed because an earlier pipeline stage failed"
                if internal == "llm" and use_llm and report.status == "ERROR":
                    status = "error"
                    summary = "LLM generation failed before a program could be produced"
            else:
                status = detail.status
                summary = detail.summary
            if not (internal == "llm" and llm_stage_started):
                yield self._sse("stage_start", SSEStageStart(
                    stage=frontend_stage,
                    message=message,
                    instruction=instruction,
                ))
                yield self._sse("stage_progress", SSEStageProgress(
                    stage=frontend_stage,
                    detail=message,
                    instruction=instruction,
                ))
            yield self._sse("stage_complete", SSEStageComplete(
                stage=frontend_stage,
                status=status,
                duration_ms=(detail.duration_ms if detail else 0.0),
                summary=summary,
                findings=[],
                snapshot={},
                instruction=instruction,
            ))

        coverage_dict = {
            "normal": report.coverage.normal,
            "boundary": report.coverage.boundary,
            "encoding": report.coverage.encoding,
            "alias": report.coverage.alias,
            "invalid": report.coverage.invalid,
            "feature": report.coverage.feature,
            "overall": report.coverage.overall,
        }
        result_event = SSEResult(
            instruction=report.instruction,
            status=report.status,
            review_score=report.review_score,
            total_tests=report.generated_tests,
            passing_tests=report.passing_test_count,
            failing_tests=report.failing_test_count,
            total_duration_ms=report.total_duration_ms,
            stage_details=[sd.model_dump() for sd in report.stage_details],
            test_files=[tf.model_dump() for tf in report.test_files],
            coverage=coverage_dict,
            issues=report.issues,
            verification_level=report.verification_level,
            generated_status=report.generated_status,
            static_review_status=report.static_review_status,
            compile_status=report.compile_status,
            compile_results=[r.model_dump() for r in report.compile_results],
            generation_mode=report.generation_mode,
            generation_trace=report.generation_trace,
            budget=report.budget,
            required_features=report.required_features,
            canonical_targets=report.canonical_targets,
        )
        yield self._sse("result", result_event)
        yield self._sse("done", {})
        logger.info(
            "verification.stream.complete",
            instruction=instruction,
            status=report.status,
            score=report.review_score,
            tests=report.generated_tests,
            duration_ms=report.total_duration_ms,
        )
        return

        # ═══════════════════════════════════════════════════════
        # Stage 1: Instruction Retrieval
        # ═══════════════════════════════════════════════════════
        t_s1 = time.perf_counter()
        try:
            profile = self.analyzer.extract_profile(mnemonic=instruction)
            if profile is None:
                yield self._sse("done", {"error": f"Instruction '{instruction}' not found in knowledge base"})
                return

            snapshot_s1 = {
                "encoding_count": profile.encoding_count,
                "operand_count": profile.operand_count,
                "feature_deps": len(profile.feature_dependencies),
                "complexity": profile.complexity_score,
            }
            summary_s1 = (
                f"Found ARM ARM XML entry for {instruction}: "
                f"class={profile.instr_class}, encodings={profile.encoding_count}, "
                f"operands={profile.operand_count}, complexity={profile.complexity_score}/10"
            )

            # Emit retrieval stage (this is actually "retrieval" in frontend)
            yield self._sse("stage_start", SSEStageStart(
                stage="retrieval",
                message=f"Retrieving instruction profile for {instruction} from knowledge base...",
            ))
            dur_s1 = (time.perf_counter() - t_s1) * 1000
            stage_results.append(StageResult(
                stage="retrieval", status="ok", duration_ms=dur_s1,
                output_summary=summary_s1,
            ))
            yield _emit_stage_complete(
                internal="retrieval", status_str="ok", dur=dur_s1,
                summary_text=f"Found ARM ARM XML entry for {instruction}",
                findings=[
                    f"指令类: {profile.instr_class or 'unknown'}",
                    f"复杂度: {profile.complexity_score}/10",
                    f"编码变体: {profile.encoding_count} 个",
                    f"操作数: {profile.operand_count} 个",
                    f"特征依赖: {len(profile.feature_dependencies)} 个",
                ],
                snapshot=snapshot_s1,
            )
            logger.info("verification.stream.retrieval_done", mnemonic=profile.mnemonic)
        except Exception as e:
            dur_s1 = (time.perf_counter() - t_s1) * 1000
            stage_results.append(StageResult(
                stage="retrieval", status="error", duration_ms=dur_s1, error=str(e)[:300],
            ))
            yield _emit_stage_complete(
                internal="retrieval", status_str="error", dur=dur_s1,
                summary_text=f"Retrieval failed: {str(e)[:100]}",
                error_text=str(e)[:300],
            )
            yield self._sse("done", {"error": f"Retrieval failed: {str(e)[:200]}"})
            return

        # ═══════════════════════════════════════════════════════
        # Stage 2+3: Constraint Analysis + Test Planning → Planner
        # ═══════════════════════════════════════════════════════
        yield self._sse("stage_start", SSEStageStart(
            stage="planner",
            message=f"Analyzing {instruction} constraints and planning test strategy...",
        ))

        t_p = time.perf_counter()

        # --- Constraint Analysis (internal) ---
        t_s2 = time.perf_counter()
        try:
            constraint_count = len(profile.constrained_unpredictable)
            feature_count = len(profile.feature_dependencies)
            encoding_undef_count = len(profile.encoding_undefined)

            constraint_details: list[str] = []
            if constraint_count > 0:
                constraint_details.append(f"{constraint_count} UNPREDICTABLE constraints")
            if feature_count > 0:
                constraint_details.append(
                    f"{feature_count} feature deps ({', '.join(fd.feature_name for fd in profile.feature_dependencies[:3])})"
                )
            if encoding_undef_count > 0:
                constraint_details.append(f"{encoding_undef_count} encoding undefined")
            if profile.has_shift_extend:
                constraint_details.append("shift/extend variants")
            if profile.affects_flags:
                constraint_details.append("affects NZCV flags")

            constraint_summary = "; ".join(constraint_details) if constraint_details else "No special constraints"
            dur_s2 = (time.perf_counter() - t_s2) * 1000
            stage_results.append(StageResult(
                stage="constraint_analysis", status="ok", duration_ms=dur_s2,
                output_summary=constraint_summary,
            ))
            yield self._sse("stage_progress", SSEStageProgress(
                stage="planner",
                detail=f"Found {constraint_count} constraints, {feature_count} feature deps",
            ))
        except Exception as e:
            dur_s2 = (time.perf_counter() - t_s2) * 1000
            constraint_summary = ""
            stage_results.append(StageResult(
                stage="constraint_analysis", status="warning", duration_ms=dur_s2, error=str(e)[:200],
            ))

        # --- Test Planning (internal) ---
        t_s3 = time.perf_counter()
        plan_reasoning = ""
        try:
            plan_result = self.planner.plan(
                mnemonic=instruction,
                user_goal=f"Comprehensive verification of {instruction}",
                use_llm=self._use_llm_planning,
            )
            if plan_result.get("status") == "ok":
                strategy = plan_result.get("strategy")
                if isinstance(strategy, TestStrategy):
                    plan_output = PlanOutput(
                        instruction=profile,
                        strategy=strategy,
                        reasoning=plan_result.get("reasoning", ""),
                        test_plan_summary=plan_result.get("plan_markdown", ""),
                    )
                    plan_reasoning = plan_output.reasoning

            dim_names = [d.name for d in (strategy.dimensions if strategy else [])]
            plan_summary = (
                f"Plan: {strategy.total_test_count} tests, "
                f"{len(dim_names)} dimensions: {', '.join(dim_names[:5])}"
                if strategy else "Using default test strategy"
            )
            dur_s3 = (time.perf_counter() - t_s3) * 1000
            stage_results.append(StageResult(
                stage="test_planning",
                status="ok" if strategy else "warning",
                duration_ms=dur_s3,
                output_summary=plan_summary,
            ))
            yield self._sse("stage_progress", SSEStageProgress(
                stage="planner",
                detail=f"Strategy: {strategy.total_test_count if strategy else 'default'} tests, {len(dim_names)} dimensions",
            ))
        except Exception as e:
            dur_s3 = (time.perf_counter() - t_s3) * 1000
            plan_summary = "Using default test strategy"
            stage_results.append(StageResult(
                stage="test_planning", status="warning", duration_ms=dur_s3, error=str(e)[:200],
            ))

        # Emit combined Planner stage_complete
        dur_planner = dur_s2 + dur_s3
        planner_findings: list[str] = []
        if constraint_details:
            planner_findings = constraint_details
        elif profile:
            planner_findings = [
                f"编码变体: {profile.encoding_count} 个",
                f"操作数: {profile.operand_count} 个",
                f"特征依赖: {len(profile.feature_dependencies)} 个",
            ]
        yield _emit_stage_complete(
            internal="constraint_analysis",  # will map to "planner"
            status_str="ok",
            dur=dur_planner,
            summary_text=(
                f"Found {constraint_count} constraints: {constraint_summary[:80]}"
                if constraint_summary else f"Analyzed {instruction} — no special constraints"
            ),
            reasoning=plan_reasoning,
            findings=planner_findings,
            snapshot={
                "encoding_count": profile.encoding_count,
                "operand_count": profile.operand_count,
                "feature_deps": len(profile.feature_dependencies),
                "complexity": profile.complexity_score,
                "total_test_count": strategy.total_test_count if strategy else 0,
                "dimension_count": len(dim_names) if strategy else 0,
            },
        )

        logger.info("verification.stream.planner_done", dims=len(dim_names) if strategy else 0)

        # ═══════════════════════════════════════════════════════
        # Stage 4: Test Generation → Generator
        # ═══════════════════════════════════════════════════════
        yield self._sse("stage_start", SSEStageStart(
            stage="generator",
            message="Creating boundary cases...",
        ))

        t_s4 = time.perf_counter()
        try:
            yield self._sse("stage_progress", SSEStageProgress(
                stage="generator",
                detail="Generating assembly tests...",
            ))
            suite = self.generator.generate_suite(
                profile=profile,
                use_llm=use_llm,
                instruction_count=instruction_count,
            )
            format_counts = {
                k: v for k, v in suite.test_counts_by_type.items() if v > 0
            }
            dur_s4 = (time.perf_counter() - t_s4) * 1000
            stage_results.append(StageResult(
                stage="test_generation", status="ok", duration_ms=dur_s4,
                output_summary=f"Generated {suite.total_tests} test cases across {len(format_counts)} formats",
            ))
            gen_findings = [f"{k}: {v}" for k, v in sorted(format_counts.items())]
            yield _emit_stage_complete(
                internal="test_generation", status_str="ok", dur=dur_s4,
                summary_text=f"Generated {suite.total_tests} test cases across {len(format_counts)} formats",
                findings=gen_findings,
                snapshot={"total_tests": suite.total_tests, "format_counts": format_counts},
            )
            logger.info("verification.stream.generation_done", total_tests=suite.total_tests)
        except Exception as e:
            dur_s4 = (time.perf_counter() - t_s4) * 1000
            stage_results.append(StageResult(
                stage="test_generation", status="error", duration_ms=dur_s4, error=str(e)[:300],
            ))
            yield _emit_stage_complete(
                internal="test_generation", status_str="error", dur=dur_s4,
                summary_text=f"Test generation failed: {str(e)[:100]}",
                error_text=str(e)[:300],
            )
            yield self._sse("done", {"error": f"Test generation failed: {str(e)[:200]}"})
            return

        # ═══════════════════════════════════════════════════════
        # Stage 5: Test Review → Reviewer
        # ═══════════════════════════════════════════════════════
        yield self._sse("stage_start", SSEStageStart(
            stage="reviewer",
            message="Reviewing test cases across 5 dimensions...",
        ))

        t_s5 = time.perf_counter()
        try:
            yield self._sse("stage_progress", SSEStageProgress(
                stage="reviewer",
                detail="Checking syntax, constraints, encoding, semantics, and coverage...",
            ))
            review_result = self.reviewer.review(
                test_suite=suite,
                profile=profile,
                strategy=strategy,
                use_llm=self._use_llm_review,
            )
            dur_s5 = (time.perf_counter() - t_s5) * 1000
            review_summary = (
                f"{'PASS' if review_result.passed else 'FAIL'} | "
                f"Score: {review_result.score:.0f}/100 | "
                f"Issues: {review_result.total_issues} "
                f"(H:{review_result.high_severity_count} "
                f"M:{review_result.medium_severity_count} "
                f"L:{review_result.low_severity_count})"
            )
            stage_results.append(StageResult(
                stage="test_review",
                status="ok" if review_result.passed else "warning",
                duration_ms=dur_s5,
                output_summary=review_summary,
            ))

            dim_status: list[str] = []
            for ds in review_result.dimension_scores:
                icon = "✅" if ds.score >= 80 else ("⚠️" if ds.score >= 60 else "❌")
                dim_status.append(f"{ds.dimension}: {icon}")
            if not dim_status:
                dim_status = ["Syntax: ✅", "Constraint: ✅", "Encoding: ✅", "Semantic: ✅", "Coverage: ✅"]

            yield _emit_stage_complete(
                internal="test_review", status_str="ok" if review_result.passed else "warning",
                dur=dur_s5,
                summary_text=review_summary,
                findings=dim_status,
                snapshot={
                    "score": review_result.score,
                    "passed": review_result.passed,
                    "high": review_result.high_severity_count,
                    "medium": review_result.medium_severity_count,
                    "low": review_result.low_severity_count,
                },
            )
            logger.info("verification.stream.review_done", passed=review_result.passed, score=review_result.score)
        except Exception as e:
            dur_s5 = (time.perf_counter() - t_s5) * 1000
            stage_results.append(StageResult(
                stage="test_review", status="error", duration_ms=dur_s5, error=str(e)[:300],
            ))
            yield _emit_stage_complete(
                internal="test_review", status_str="error", dur=dur_s5,
                summary_text=f"Test review failed: {str(e)[:100]}",
                error_text=str(e)[:300],
            )
            yield self._sse("done", {"error": f"Test review failed: {str(e)[:200]}"})
            return

        # ═══════════════════════════════════════════════════════
        # Stage 6: Repair Loop → Repair
        # ═══════════════════════════════════════════════════════
        t_s6 = time.perf_counter()
        last_review = review_result
        repair_needed = not last_review.passed and repair_count < MAX_REPAIR_ATTEMPTS

        if repair_needed:
            yield self._sse("stage_start", SSEStageStart(
                stage="repair",
                message="Attempting to fix detected issues...",
            ))

        while not last_review.passed and repair_count < MAX_REPAIR_ATTEMPTS:
            fixable_types = {"syntax_error", "constraint_error", "encoding_error", "semantic_error"}
            has_fixable = any(
                i.type in fixable_types and i.severity in ("high", "medium")
                for i in last_review.issues
            )
            if not has_fixable:
                logger.info("verification.multi.repair_skip", reason="no fixable issues")
                break

            repair_count += 1
            yield self._sse("stage_progress", SSEStageProgress(
                stage="repair",
                detail=f"Repair attempt {repair_count}/{MAX_REPAIR_ATTEMPTS}...",
            ))
            logger.info("verification.multi.repair_attempt", attempt=repair_count)

            try:
                repair_result: RepairResult = self.repairer.repair(
                    review_result=last_review,
                    test_suite=suite,
                    profile=profile,
                )
                if repair_result.repaired:
                    suite = self.generator.generate_suite(
                        profile=profile,
                        use_llm=True,
                    )
                    last_review = self.reviewer.review(
                        test_suite=suite,
                        profile=profile,
                        strategy=strategy,
                        use_llm=self._use_llm_review,
                    )
                    if last_review.passed:
                        repair_successful = True
                        yield self._sse("stage_progress", SSEStageProgress(
                            stage="repair",
                            detail="Fixed testcase — review passed after repair!",
                        ))
                        logger.info("verification.multi.repair_success", attempt=repair_count)
                else:
                    logger.warning("verification.multi.repair_not_possible", attempt=repair_count)
                    break
            except Exception as e:
                logger.error("verification.multi.repair_error", attempt=repair_count, error=str(e)[:200])
                break

        dur_s6 = (time.perf_counter() - t_s6) * 1000
        repair_status = "ok" if repair_successful else ("skipped" if repair_count == 0 else "warning")
        repair_summary = (
            f"Repaired successfully after {repair_count} attempt(s)"
            if repair_successful else
            f"Repair attempted {repair_count} time(s), not fully resolved"
            if repair_count > 0 else
            "No repair needed"
        )
        stage_results.append(StageResult(
            stage="repair", status=repair_status,
            duration_ms=dur_s6, output_summary=repair_summary,
        ))
        yield _emit_stage_complete(
            internal="repair", status_str=repair_status, dur=dur_s6,
            summary_text=repair_summary,
            findings=[repair_summary],
            snapshot={"attempts": repair_count, "successful": repair_successful},
        )

        # ── Build final result ───────────────────────────────
        review_score = last_review.score if last_review else 0.0
        review_passed = last_review.passed if last_review else False

        if review_passed and repair_count == 0:
            overall_status = "PASS"
        elif review_passed and repair_count > 0:
            overall_status = "REPAIRED"
        elif not review_passed:
            overall_status = "FAIL"
        else:
            overall_status = "ERROR"

        coverage = self._compute_coverage(suite, profile, strategy)

        # Build issues
        issues_list: list[dict[str, Any]] = []
        if last_review:
            for issue in last_review.issues:
                issues_list.append({
                    "type": issue.type,
                    "severity": issue.severity,
                    "description": issue.description,
                    "location": issue.location,
                    "suggestion": issue.suggestion,
                    "dimension": issue.dimension,
                })

        # Build test_files from suite
        test_files_raw = suite.to_test_file_entries() if suite else []
        # Mark failing tests based on review issues
        issue_locations = {i.get("location", "") for i in issues_list}
        for tf in test_files_raw:
            if tf["file_id"] in issue_locations:
                tf["status"] = "fail"
                tf["issue_count"] = sum(1 for i in issues_list if i.get("location") == tf["file_id"])

        passing = sum(1 for tf in test_files_raw if tf["status"] == "pass")
        failing = sum(1 for tf in test_files_raw if tf["status"] == "fail")
        compile_summary = CompileVerifier().verify_files(test_files_raw)
        verification_level = (
            "compiled" if compile_summary.status == "PASS"
            else "statically_reviewed" if review_passed
            else "generated"
        )
        generated_status = "PASS" if suite and suite.total_tests > 0 else "FAIL"
        static_review_status = "PASS" if review_passed else "FAIL"
        compile_status = (
            "PASS" if compile_summary.status == "PASS"
            else "FAIL" if compile_summary.status == "FAIL"
            else "SKIPPED"
        )
        if compile_summary.status == "PASS":
            overall_status = "COMPILED"
        elif compile_summary.status == "FAIL":
            overall_status = "FAILED"
        elif review_passed:
            overall_status = "REVIEWED"

        total_ms = (time.perf_counter() - t_start) * 1000

        # Coverage dict
        coverage_dict = {
            "normal": coverage.normal,
            "boundary": coverage.boundary,
            "encoding": coverage.encoding,
            "alias": coverage.alias,
            "invalid": coverage.invalid,
            "feature": coverage.feature,
            "overall": coverage.overall,
        }

        # Emit result
        result_event = SSEResult(
            instruction=instruction,
            status=overall_status,
            review_score=review_score,
            total_tests=suite.total_tests if suite else 0,
            passing_tests=passing,
            failing_tests=failing,
            total_duration_ms=total_ms,
            stage_details=[sd.model_dump() for sd in stage_details],
            test_files=test_files_raw,
            coverage=coverage_dict,
            issues=issues_list,
            verification_level=verification_level,  # type: ignore[arg-type]
            generated_status=generated_status,  # type: ignore[arg-type]
            static_review_status=static_review_status,  # type: ignore[arg-type]
            compile_status=compile_status,  # type: ignore[arg-type]
            compile_results=[r.model_dump() for r in compile_summary.results],
        )
        yield self._sse("result", result_event)
        yield self._sse("done", {})

        logger.info(
            "verification.stream.complete",
            instruction=instruction,
            status=overall_status,
            score=review_score,
            tests=suite.total_tests if suite else 0,
            duration_ms=total_ms,
        )

    async def verify_batch_stream(
        self,
        instructions: list[str],
        use_llm: bool = False,
        instruction_count: int = 100,
    ) -> AsyncGenerator[str, None]:
        """Run batch verification with SSE event streaming.

        Args:
            instructions: List of ARM instruction mnemonics.
            use_llm: If True, use LLM-assisted generation.
            instruction_count: Target instruction instances per program.

        Yields:
            SSE event strings for batch progress.
        """
        cleaned = [i.strip().upper() for i in instructions if i.strip()]
        if not cleaned:
            yield self._sse("done", {"error": "No valid instructions provided"})
            return

        yield self._sse("batch_start", SSEBatchStart(total=len(cleaned), instructions=cleaned))

        pass_count = 0
        fail_count = 0
        reports: list[dict[str, Any]] = []
        batch_start_time = time.perf_counter()

        for idx, instr in enumerate(cleaned):
            yield self._sse("instruction_start", SSEInstructionStart(
                index=idx, instruction=instr, total=len(cleaned),
            ))

            # Run individual verify_stream with use_llm & instruction_count
            t_ins = time.perf_counter()
            captured_status = "PASS"
            captured_score = 0.0
            captured_test_files: list[dict[str, Any]] = []
            captured_issues: list[dict[str, Any]] = []

            async for event_str in self.verify_stream(instr, use_llm=use_llm, instruction_count=instruction_count):
                # Capture the result event for populating instruction_complete
                if "event: result" in event_str:
                    try:
                        data_line = event_str.split("data: ")[1]
                        result_data = json.loads(data_line)
                        captured_status = result_data.get("status", "PASS")
                        captured_score = result_data.get("review_score", 0.0)
                        captured_test_files = result_data.get("test_files", [])
                        captured_issues = result_data.get("issues", [])
                    except Exception:
                        pass
                yield event_str

            ins_dur = (time.perf_counter() - t_ins) * 1000
            if captured_status in ("PASS", "REPAIRED"):
                pass_count += 1
            else:
                fail_count += 1

            yield self._sse("instruction_complete", SSEInstructionComplete(
                index=idx,
                instruction=instr,
                status=captured_status,
                review_score=captured_score,
                duration_ms=ins_dur,
                test_files=captured_test_files,
                issues=captured_issues,
            ))

        batch_dur = (time.perf_counter() - batch_start_time) * 1000
        yield self._sse("batch_complete", SSEBatchComplete(
            total=len(cleaned),
            passed=pass_count,
            failed=fail_count,
            total_duration_ms=batch_dur,
            reports=reports,
        ))
        yield self._sse("done", {})

    async def verify_scenario_program_stream(
        self,
        scenarios: list[list[str]],
        use_llm: bool = False,
        instruction_count: int = 100,
        target_instruction_count: int = 1,
    ) -> AsyncGenerator[str, None]:
        """Run scenario batch verification as one assembly program per row."""
        requests: list[ScenarioRequest] = []
        for scenario in scenarios:
            queries = [m.strip() for m in scenario if m and m.strip()]
            if not queries:
                continue
            requests.append(ScenarioRequest(
                scenario_id=f"scenario_{len(requests) + 1:03d}",
                raw="\n".join(queries) if use_llm else ",".join(queries),
                queries=[] if use_llm else queries,
                program_instruction_count=instruction_count,
                target_instruction_count=target_instruction_count,
                generation_mode="llm" if use_llm else "rule_based",
            ))

        if not requests:
            yield self._sse("done", {"error": "No valid scenarios provided"})
            return

        labels = [r.raw for r in requests]
        yield self._sse("batch_start", SSEBatchStart(total=len(requests), instructions=labels))

        pass_count = 0
        fail_count = 0
        reports: list[dict[str, Any]] = []
        batch_start_time = time.perf_counter()

        for idx, request in enumerate(requests):
            yield self._sse("instruction_start", SSEInstructionStart(
                index=idx,
                instruction=request.raw,
                total=len(requests),
            ))
            started = time.perf_counter()
            result_data: dict[str, Any]
            try:
                progress_queue: asyncio.Queue[tuple[str, str, str, dict[str, Any]]] = asyncio.Queue()
                loop = asyncio.get_running_loop()

                def publish_progress(stage: str, event: str, message: str, snapshot: dict[str, Any]) -> None:
                    loop.call_soon_threadsafe(progress_queue.put_nowait, (stage, event, message, snapshot))

                generator = ScenarioProgramGenerator(
                    self._sqlite,
                    seed=instruction_count + idx,
                    llm=self._llm,
                    progress_callback=publish_progress,
                )
                generation_task = asyncio.create_task(asyncio.to_thread(generator.generate_and_verify, request))

                while not generation_task.done():
                    try:
                        stage, event, message, snapshot = await asyncio.wait_for(progress_queue.get(), timeout=0.1)
                    except asyncio.TimeoutError:
                        continue
                    if event == "start":
                        yield self._sse("stage_start", SSEStageStart(stage=stage, message=message, instruction=request.raw))
                    elif event == "progress":
                        yield self._sse("stage_progress", SSEStageProgress(stage=stage, detail=message, instruction=request.raw))
                    else:
                        status = str(snapshot.get("status", "ok"))
                        yield self._sse("stage_complete", SSEStageComplete(
                            stage=stage,
                            status=status,
                            duration_ms=0.0,
                            summary=message,
                            snapshot=snapshot,
                            instruction=request.raw,
                        ))

                program = await generation_task
                # Drain callback events that raced with task completion so the UI
                # always receives the final static-review/compiler state first.
                while not progress_queue.empty():
                    stage, event, message, snapshot = progress_queue.get_nowait()
                    if event == "start":
                        yield self._sse("stage_start", SSEStageStart(stage=stage, message=message, instruction=request.raw))
                    elif event == "progress":
                        yield self._sse("stage_progress", SSEStageProgress(stage=stage, detail=message, instruction=request.raw))
                    else:
                        yield self._sse("stage_complete", SSEStageComplete(
                            stage=stage,
                            status=str(snapshot.get("status", "ok")),
                            duration_ms=0.0,
                            summary=message,
                            snapshot=snapshot,
                            instruction=request.raw,
                        ))
                duration_ms = (time.perf_counter() - started) * 1000
                result_data = program.to_result_event(duration_ms)
                reports.append(result_data)
                yield self._sse("result", result_data)

                if result_data.get("status") in {"COMPILED", "REVIEWED", "GENERATED"}:
                    pass_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                logger.error("scenario_program.stream.error", scenario=request.raw, error=str(e)[:300])
                fail_count += 1
                result_data = {
                    "instruction": request.raw,
                    "status": "ERROR",
                    "review_score": 0.0,
                    "total_tests": 0,
                    "passing_tests": 0,
                    "failing_tests": 1,
                    "total_duration_ms": (time.perf_counter() - started) * 1000,
                    "stage_details": [],
                    "test_files": [],
                    "coverage": {},
                    "issues": [{
                        "type": "runtime_error",
                        "severity": "high",
                        "description": str(e)[:500],
                        "location": request.raw,
                        "dimension": "orchestrator",
                    }],
                    "verification_level": "generated",
                    "generated_status": "FAIL",
                    "static_review_status": "SKIPPED",
                    "compile_status": "SKIPPED",
                    "compile_results": [],
                }
                reports.append(result_data)
                yield self._sse("result", result_data)

            yield self._sse("instruction_complete", SSEInstructionComplete(
                index=idx,
                instruction=request.raw,
                status=str(result_data.get("status", "ERROR")),
                review_score=float(result_data.get("review_score", 0.0)),
                duration_ms=float(result_data.get("total_duration_ms", 0.0)),
                test_files=list(result_data.get("test_files", [])),
            ))

        batch_dur = (time.perf_counter() - batch_start_time) * 1000
        yield self._sse("batch_complete", SSEBatchComplete(
            total=len(requests),
            passed=pass_count,
            failed=fail_count,
            total_duration_ms=batch_dur,
            reports=reports,
        ))
        yield self._sse("done", {})

    async def verify_scenario_stream(
        self,
        scenarios: list[list[str]],
        use_llm: bool = False,
        instruction_count: int = 100,
    ) -> AsyncGenerator[str, None]:
        """Run scenario-based batch verification — each scenario is a *list* of
        instructions that get combined into a single test program.

        Args:
            scenarios: List of scenarios; each scenario is a list of instruction
                       mnemonics to combine into one test program.
            use_llm: If True, use LLM-assisted generation.
            instruction_count: Target total instruction instances per combined program.

        Yields:
            SSE event strings for batch progress.
        """
        per_scenario_count = max(1, instruction_count)
        validated: list[list[str]] = [
            [m.strip().upper() for m in scenario if m.strip()]
            for scenario in scenarios
        ]
        validated = [s for s in validated if s]
        total_scenarios = len(validated)

        if total_scenarios == 0:
            yield self._sse("done", {"error": "No valid scenarios provided"})
            return

        # Emit batch_start with combined label
        scenario_labels = [",".join(s) for s in validated]
        yield self._sse("batch_start", SSEBatchStart(
            total=total_scenarios, instructions=scenario_labels,
        ))

        pass_count = 0
        fail_count = 0
        reports: list[dict[str, Any]] = []
        batch_start_time = time.perf_counter()

        for idx, instr_list in enumerate(validated):
            label = ",".join(instr_list)
            yield self._sse("instruction_start", SSEInstructionStart(
                index=idx, instruction=label, total=total_scenarios,
            ))

            t_ins = time.perf_counter()

            # Track result variables for instruction_complete
            overall_status = "FAIL"
            review_score = 0.0
            issues_list: list[dict[str, Any]] = []
            test_files_raw: list[dict[str, Any]] = []

            # ── Combined multi-instruction flow ──
            try:
                # Stage 1: Load profiles for all instructions
                profiles = []
                for mnemonic in instr_list:
                    yield self._sse("stage_progress", SSEStageProgress(
                        stage=self._frontend_stage("analyzer"),
                        detail=f"Loading profile: {mnemonic}",
                    ))
                    profile = await asyncio.to_thread(
                        self.analyzer.extract_profile, mnemonic,
                    )
                    if not profile:
                        yield self._sse("stage_progress", SSEStageProgress(
                            stage=self._frontend_stage("analyzer"),
                            detail=f"Profile not found: {mnemonic}, skipping",
                        ))
                        continue
                    profiles.append(profile)

                if not profiles:
                    yield self._sse("instruction_complete", SSEInstructionComplete(
                        index=idx, instruction=label,
                        status="FAIL", review_score=0.0,
                        duration_ms=(time.perf_counter() - t_ins) * 1000,
                        test_files=[],
                    ))
                    fail_count += 1
                    continue

                # Stage 2: Plan (use first profile's mnemonic as primary)
                try:
                    await asyncio.to_thread(
                        self.planner.plan,
                        mnemonic=profiles[0].mnemonic,
                        user_goal=f"Comprehensive multi-instruction verification of {label}",
                        use_llm=self._use_llm_planning,
                    )
                except Exception as e:
                    logger.warning("scenario.plan_failed", label=label, error=str(e))

                yield self._sse("stage_progress", SSEStageProgress(
                    stage=self._frontend_stage("planning"),
                    detail=f"Planned test strategy for {len(profiles)} instruction(s)",
                ))

                # Stage 3: Generate combined suite
                yield self._sse("stage_progress", SSEStageProgress(
                    stage="generator",
                    detail=f"Generating combined tests for {label}...",
                ))
                suite = self.generator.generate_multi_instruction(
                    profiles=profiles,
                    use_llm=use_llm,
                    instruction_count=per_scenario_count,
                )
                if suite:
                    suite.scenario_label = label
                    test_files_raw = suite.to_test_file_entries()
                else:
                    test_files_raw = []

                # Stage 4: Review (LLM only when enabled and available)
                review_passed = True
                review_score = 100.0
                issues_list: list[dict[str, Any]] = []
                if self._use_llm_review and self._llm:
                    try:
                        review_result = await asyncio.to_thread(
                            self.reviewer.review,
                            test_suite=suite,
                            profile=profiles[0],
                            strategy=None,
                            use_llm=True,
                        )
                        review_passed = review_result.passed
                        review_score = review_result.score
                        issues_list = [i.to_json_api() if hasattr(i, 'to_json_api') else i
                                      for i in (review_result.issues or [])]
                        # Mark failing test files based on review
                        issue_locs = {i.get("location", "") for i in issues_list}
                        for tf in test_files_raw:
                            if tf.get("file_id", "") in issue_locs:
                                tf["status"] = "fail"
                    except Exception as e:
                        logger.warning("scenario.review_failed", label=label, error=str(e))

                # Stage 5: Emit result event
                overall_status = "PASS" if review_passed else "FAIL"
                passing = sum(1 for tf in test_files_raw if tf.get("status") == "pass")
                failing = sum(1 for tf in test_files_raw if tf.get("status") == "fail")

                result_event = SSEResult(
                    instruction=label,
                    status=overall_status,
                    review_score=review_score,
                    total_tests=suite.total_tests if suite else 0,
                    passing_tests=passing,
                    failing_tests=failing,
                    total_duration_ms=(time.perf_counter() - t_ins) * 1000,
                    stage_details=[],
                    test_files=test_files_raw,
                    coverage={},
                    issues=issues_list,
                )
                yield self._sse("result", result_event)

                if review_passed:
                    pass_count += 1
                else:
                    fail_count += 1

            except Exception as e:
                logger.error("scenario.stream.error", label=label, error=str(e))
                overall_status = "ERROR"
                review_score = 0.0
                issues_list = [{"severity": "error", "type": "runtime_error", "dimension": "-", "description": str(e), "suggestion": "Check backend logs for full traceback", "location": ""}]
                test_files_raw = []
                yield self._sse("result", SSEResult(
                    instruction=label,
                    status="ERROR",
                    review_score=0.0,
                    total_tests=0,
                    passing_tests=0,
                    failing_tests=0,
                    total_duration_ms=0,
                    stage_details=[],
                    test_files=[],
                    coverage={},
                    issues=issues_list,
                ))
                fail_count += 1

            ins_dur = (time.perf_counter() - t_ins) * 1000
            yield self._sse("instruction_complete", SSEInstructionComplete(
                index=idx,
                instruction=label,
                status=overall_status,
                review_score=review_score,
                duration_ms=ins_dur,
                test_files=test_files_raw,
            ))

        batch_dur = (time.perf_counter() - batch_start_time) * 1000
        yield self._sse("batch_complete", SSEBatchComplete(
            total=total_scenarios,
            passed=pass_count,
            failed=fail_count,
            total_duration_ms=batch_dur,
            reports=reports,
        ))
        yield self._sse("done", {})


# ── Convenience function ──────────────────────────────────────────

def run_verification(
    instruction: str,
    sqlite_client: Any = None,
    llm: Any = None,
    use_llm: bool = False,
    instruction_count: int = 100,
    target_instruction_count: int = 1,
) -> VerificationReport:
    """One-shot verification for a single ARM instruction.

    Args:
        instruction: ARM mnemonic (e.g. "ADD", "LDR").
        sqlite_client: Initialized SQLiteClient.
        llm: LangChain ChatOpenAI instance.
        use_llm: Enable LLM-assisted planning and review (slower but higher quality).
        instruction_count: Target instruction instances per test program.
        target_instruction_count: Target instruction occurrences in each test program.

    Returns:
        VerificationReport with full pipeline results.
    """
    orchestrator = VerificationOrchestrator(
        sqlite_client=sqlite_client,
        llm=llm,
        use_llm_planning=use_llm,
        use_llm_review=use_llm,
    )
    return orchestrator.verify(
        instruction,
        use_llm=use_llm,
        instruction_count=instruction_count,
        target_instruction_count=target_instruction_count,
    )
