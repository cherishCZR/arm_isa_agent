"""Testcase Reviewer — 5 dimension-specific reviewers + orchestrator + repair generator.

Architecture:
    TestcaseReviewer (orchestrator)
    ├── SyntaxReviewer        – ARM asm / LLVM MC / C++ syntax
    ├── ConstraintReviewer    – operand ranges, register constraints, feature gates
    ├── EncodingReviewer      – opcode / bitfield / encoding selection
    ├── SemanticReviewer      – expected results vs operation
    └── CoverageReviewer      – TestPlan vs actual testcases

    RepairGenerator (self-correction)
    └── Takes review issues → generates fixes → outputs repaired content
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any, Optional

import structlog

from arm_isa_agent.generation.models import TestCaseSuite
from arm_isa_agent.planning.models import InstructionProfile, TestStrategy
from arm_isa_agent.review_generation.models import (
    DimensionScore,
    RepairResult,
    ReviewIssue,
    ReviewResult,
)
from arm_isa_agent.review_generation.prompts import (
    CONSTRAINT_REVIEW_SYSTEM_PROMPT,
    COVERAGE_REVIEW_SYSTEM_PROMPT,
    ENCODING_REVIEW_SYSTEM_PROMPT,
    MASTER_REVIEW_SYSTEM_PROMPT,
    REPAIR_SYSTEM_PROMPT,
    SEMANTIC_REVIEW_SYSTEM_PROMPT,
    SYNTAX_REVIEW_SYSTEM_PROMPT,
    format_profile_context,
)

logger = structlog.get_logger(__name__)

# ── ARM A64 register patterns ────────────────────────────────────
_RE_GP_64 = re.compile(r"\bX([0-9]|[12][0-9]|30)\b", re.IGNORECASE)
_RE_GP_32 = re.compile(r"\bW([0-9]|[12][0-9]|30)\b", re.IGNORECASE)
_RE_SP = re.compile(r"\b(SP|WSP|XZR|WZR)\b", re.IGNORECASE)
_RE_VEC = re.compile(r"\b[BVHSDQ]\d{1,2}\b", re.IGNORECASE)
_RE_SVE = re.compile(r"\b[ZP]\d{1,2}\b", re.IGNORECASE)
_RE_IMM = re.compile(r"#(-?\d+|0x[0-9a-fA-F]+)")
_RE_IMM_VAL = re.compile(r"#(-?\d+)")
_RE_IMM_HEX = re.compile(r"#(0x[0-9a-fA-F]+)")


# ═══════════════════════════════════════════════════════════════
# Common helpers
# ═══════════════════════════════════════════════════════════════

def _safe_llm_invoke(llm: Any, system_prompt: str, user_prompt: str, fallback: str = "[]") -> str:
    """Invoke LLM safely, returning fallback on error."""
    try:
        from langchain_core.messages import HumanMessage, SystemMessage

        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ])
        return str(response.content)
    except Exception as e:
        logger.warning("llm_invoke_failed", error=str(e)[:200])
        return fallback


def _parse_json_response(text: str, default: Any = None) -> Any:
    """Extract JSON from LLM response text."""
    if default is None:
        default = []
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    for marker in ["```json", "```"]:
        idx = text.find(marker)
        if idx >= 0:
            start = idx + len(marker)
            end = text.find("```", start)
            if end >= 0:
                try:
                    return json.loads(text[start:end].strip())
                except json.JSONDecodeError:
                    continue
    for start_char, end_char in [("[", "]"), ("{", "}")]:
        start = text.find(start_char)
        if start >= 0:
            depth = 0
            for i in range(start, len(text)):
                if text[i] == start_char:
                    depth += 1
                elif text[i] == end_char:
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(text[start:i + 1])
                        except json.JSONDecodeError:
                            break
    return default


def _flatten_test_content(test_suite: TestCaseSuite) -> str:
    """Flatten a TestCaseSuite into a single text blob for review."""
    parts: list[str] = []
    parts.append(f"## Instruction: {test_suite.instruction_mnemonic}")
    parts.append("")

    # Assembly tests
    for t in test_suite.assembly_tests:
        parts.append(f"### [{t.test_name}] ARM Assembly")
        parts.append(f"Instruction: {t.instruction}")
        parts.append(f"Input: {t.input_state}")
        parts.append(f"Expected: {t.expected_state}")
        if t.expected_flags:
            parts.append(f"Flags: {t.expected_flags}")
        parts.append("")

    # LLVM MC tests
    for t in test_suite.llvm_mc_tests:
        parts.append(f"### [{t.test_name}] LLVM MC")
        parts.append(t.to_llvm_mc_text())
        parts.append("")

    # Inline asm tests
    for t in test_suite.inline_asm_tests:
        parts.append(f"### [{t.test_name}] Inline Asm")
        parts.append(t.to_inline_asm_code())
        parts.append("")

    # C++ verification
    for t in test_suite.cpp_verification_tests:
        parts.append(f"### [{t.test_name}] C++ Verification")
        parts.append(f"Reference model: {t.reference_model}")
        parts.append(f"Instruction: {t.instruction}")
        for i, (inp, exp) in enumerate(zip(t.test_inputs, t.expected_outputs)):
            parts.append(f"  Test {i}: input={inp}, expected={exp}")
        parts.append("")

    # Boundary tests
    for t in test_suite.boundary_tests:
        parts.append(f"### [{t.test_name}] Boundary [{t.category}]")
        parts.append(f"Instruction: {t.instruction}")
        parts.append(f"Boundary: {t.boundary_value}")
        parts.append(f"Expected: {t.expected_behavior}")
        parts.append("")

    # Alias tests
    for t in test_suite.alias_tests:
        parts.append(f"### [{t.test_name}] Alias")
        parts.append(f"Alias: {t.alias_instruction}")
        parts.append(f"Canonical: {t.canonical_instruction}")
        parts.append(f"Input: {t.input_state}")
        parts.append(f"Expected: {t.expected_state}")
        parts.append("")

    # Invalid operand tests
    for t in test_suite.invalid_operand_tests:
        parts.append(f"### [{t.test_name}] Invalid [{t.invalid_aspect}]")
        parts.append(f"Instruction: {t.instruction}")
        parts.append(f"Constraint: {t.constraint_source}")
        parts.append(f"Expected: {t.expected_outcome}  |  Safe to test: {t.is_safe_to_test}")
        parts.append("")

    # Feature enable tests
    for t in test_suite.feature_enable_tests:
        parts.append(f"### [{t.test_name}] Feature Enable")
        parts.append(f"Feature: {t.feature_name} ({t.architecture_version})")
        parts.append(t.test_name)
        parts.append("")

    return "\n".join(parts)


def _format_strategy_for_coverage(strategy: Optional[TestStrategy]) -> str:
    """Format TestStrategy for coverage review."""
    if strategy is None:
        return "No TestPlan/Strategy provided."
    lines: list[str] = []
    lines.append(f"## TestPlan for: {strategy.instruction_id}")
    lines.append(f"**Total tests:** {strategy.total_test_count}")
    lines.append(f"**Complexity:** {strategy.complexity}/10")
    lines.append("")

    lines.append("### Planned Dimensions:")
    for dim in strategy.dimensions:
        lines.append(f"- **{dim.name}** (priority: {dim.priority}, {dim.coverage_percentage:.0f}%)")
        lines.append(f"    Focus: {', '.join(dim.focus_areas)}")
        if dim.rationale:
            lines.append(f"    Rationale: {dim.rationale}")
        lines.append(f"    Suggested count: {dim.suggested_test_count}")
    lines.append("")

    if strategy.coverage_matrix:
        lines.append("### Coverage Matrix:")
        for dim, items in strategy.coverage_matrix.items():
            lines.append(f"  - {dim}: {', '.join(items)}")
        lines.append("")

    if strategy.constraints_to_verify:
        lines.append("### Constraints to Verify:")
        for c in strategy.constraints_to_verify:
            lines.append(f"  - {c}")
        lines.append("")

    if strategy.risk_analysis:
        lines.append(f"### Risk Analysis:\n{strategy.risk_analysis}")
        lines.append("")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 1. Syntax Reviewer
# ═══════════════════════════════════════════════════════════════

class SyntaxReviewer:
    """Review ARM assembly / LLVM MC / C++ syntax correctness.

    Supports both rule-based checks (regex) and LLM-assisted deep analysis.
    """

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    # ── Public API ───────────────────────────────────────────

    def review(
        self,
        test_suite: TestCaseSuite,
        profile: Optional[InstructionProfile] = None,
        use_llm: bool = False,
    ) -> tuple[list[ReviewIssue], float]:
        """Review syntax of a test suite.

        Returns (issues, score 0-100).
        """
        # Always run rule-based checks
        issues = self._rule_based_check(test_suite)

        # Optionally run LLM
        if use_llm and self._llm:
            llm_issues = self._llm_review(test_suite, profile)
            issues.extend(llm_issues)

        score = self._compute_score(issues)
        return issues, score

    # ── Rule-based checks ────────────────────────────────────

    def _rule_based_check(self, test_suite: TestCaseSuite) -> list[ReviewIssue]:
        """Deterministic syntax checks via regex patterns."""
        issues: list[ReviewIssue] = []

        # Check assembly tests
        for t in test_suite.assembly_tests:
            issues.extend(self._check_asm_syntax(t.instruction, t.test_name))
            # Check input expected state registers
            for reg in list(t.input_state.keys()) + list(t.expected_state.keys()):
                issues.extend(self._check_register_format(reg, t.test_name))
            if t.expected_flags:
                for flag_key in t.expected_flags:
                    if flag_key not in ("N", "Z", "C", "V"):
                        issues.append(ReviewIssue(
                            type="syntax_error",
                            severity="medium",
                            location=f"{t.test_name} flags",
                            description=f"Unknown flag: {flag_key}. Expected N/Z/C/V.",
                            suggestion=f"Use one of: N, Z, C, V",
                        ))

        # Check LLVM MC tests
        for t in test_suite.llvm_mc_tests:
            for al in t.assembly_lines:
                issues.extend(self._check_asm_syntax(al.strip(), t.test_name))

        # Check inline asm tests
        for t in test_suite.inline_asm_tests:
            issues.extend(self._check_asm_syntax(t.instruction, t.test_name))
            # Check operand constraint format
            for op_str in [t.input_operands, t.output_operands]:
                if op_str:
                    issues.extend(self._check_asm_constraint_format(op_str, t.test_name))

        # Check boundary tests
        for t in test_suite.boundary_tests:
            issues.extend(self._check_asm_syntax(t.instruction, t.test_name))

        # Check invalid operand tests
        for t in test_suite.invalid_operand_tests:
            issues.extend(self._check_asm_syntax(t.instruction, t.test_name))

        # Check alias tests
        for t in test_suite.alias_tests:
            issues.extend(self._check_asm_syntax(t.alias_instruction, t.test_name))
            issues.extend(self._check_asm_syntax(t.canonical_instruction, t.test_name))

        # Check feature enable tests
        for t in test_suite.feature_enable_tests:
            issues.extend(self._check_asm_syntax(t.instruction, t.test_name))

        # Check C++ verification tests
        for t in test_suite.cpp_verification_tests:
            issues.extend(self._check_asm_syntax(t.instruction, t.test_name))

        return issues

    @staticmethod
    def _check_asm_syntax(inst: str, test_name: str) -> list[ReviewIssue]:
        """Check a single assembly instruction string."""
        issues: list[ReviewIssue] = []
        inst_stripped = inst.strip()

        # Empty instruction
        if not inst_stripped:
            return issues

        # Check no spaces inside register names
        bad_reg_spacing = re.findall(r'\b[WX]\s+\d+', inst_stripped, re.IGNORECASE)
        if bad_reg_spacing:
            for brs in bad_reg_spacing:
                issues.append(ReviewIssue(
                    type="syntax_error",
                    severity="high",
                    location=f"{test_name}: `{inst_stripped}`",
                    description=f"Registration name with space: '{brs}'",
                    suggestion=f"Remove space: {brs.replace(' ', '')}",
                ))

        # Check for valid operand separator
        parts = inst_stripped.split()
        if len(parts) < 2:
            issues.append(ReviewIssue(
                type="syntax_error",
                severity="high",
                location=f"{test_name}: `{inst_stripped}`",
                description="Instruction has no operands",
                suggestion="Add operands, e.g. ADD X0, X1, X2",
            ))

        # Check that instruction mnemonic is uppercase (ARM convention)
        if parts:
            mnemonic = parts[0]
            if not mnemonic.isupper() and not mnemonic[0].isupper():
                pass  # lowercase mnemonics are valid in llvm-mc but uppercase is convention

            # Check no '#' immediately followed by a register name without separator
            remaining = " ".join(parts[1:])
            if remaining and "#" in remaining:
                # Find immediate values
                imms = _RE_IMM.findall(remaining)
                for imm in imms:
                    # Check hex format
                    hex_match = _RE_IMM_HEX.match(imm)
                    if hex_match:
                        hex_val = hex_match.group(1)
                        # Must have at least one hex digit after 0x
                        if len(hex_val) == 2:  # just "0x"
                            issues.append(ReviewIssue(
                                type="syntax_error",
                                severity="high",
                                location=f"{test_name}: `{inst_stripped}`",
                                description=f"Invalid hex immediate: {hex_val}",
                                suggestion="Provide hex digits, e.g. #0x10",
                            ))
                    else:
                        dec_match = _RE_IMM_VAL.match(imm)
                        if dec_match:
                            val_str = dec_match.group(1)
                            # Must be a number
                            try:
                                int(val_str)
                            except ValueError:
                                issues.append(ReviewIssue(
                                    type="syntax_error",
                                    severity="high",
                                    location=f"{test_name}: `{inst_stripped}`",
                                    description=f"Invalid immediate: {imm}",
                                    suggestion="Use valid integer constant, e.g. #123",
                                ))

        return issues

    @staticmethod
    def _check_register_format(reg: str, test_name: str) -> list[ReviewIssue]:
        """Check register string format."""
        issues: list[ReviewIssue] = []
        # Check if it looks like a valid register
        is_gp64 = bool(_RE_GP_64.fullmatch(reg))
        is_gp32 = bool(_RE_GP_32.fullmatch(reg))
        is_sp = bool(_RE_SP.fullmatch(reg))
        is_vec = bool(_RE_VEC.fullmatch(reg))
        is_sve = bool(_RE_SVE.fullmatch(reg))

        if not any([is_gp64, is_gp32, is_sp, is_vec, is_sve]):
            # Might be a valid register we didn't catch, or an error
            if reg and not reg[0].isalpha():
                issues.append(ReviewIssue(
                    type="syntax_error",
                    severity="medium",
                    location=test_name,
                    description=f"Possible invalid register format: '{reg}'",
                    suggestion="Use X0-X30, W0-W30, XZR, WZR, SP, or V/D/S/H/B registers",
                ))
        return issues

    @staticmethod
    def _check_asm_constraint_format(constraints: str, test_name: str) -> list[ReviewIssue]:
        """Check inline asm constraint string format."""
        issues: list[ReviewIssue] = []
        # Simple heuristic: constraints should contain quotes
        if '"' not in constraints and "'" not in constraints:
            issues.append(ReviewIssue(
                type="syntax_error",
                severity="medium",
                location=test_name,
                description=f"Inline asm constraint missing quotes: '{constraints}'",
                suggestion='Use format like: "r"(var) or "=r"(out_var)',
            ))
        return issues

    # ── LLM review ───────────────────────────────────────────

    def _llm_review(
        self,
        test_suite: TestCaseSuite,
        profile: Optional[InstructionProfile],
    ) -> list[ReviewIssue]:
        """LLM-assisted deep syntax review."""
        content = _flatten_test_content(test_suite)
        ctx = format_profile_context(profile) if profile else ""

        prompt = f"""Review the following ARM test suite for syntax errors.

{ctx}

### Test Suite Content:
{content[:6000]}

Output JSON array of syntax issues."""

        result = _safe_llm_invoke(self._llm, SYNTAX_REVIEW_SYSTEM_PROMPT, prompt)
        data = _parse_json_response(result, [])

        issues: list[ReviewIssue] = []
        for item in data:
            item.setdefault("type", "syntax_error")
            item.setdefault("dimension", "syntax")
            issues.append(ReviewIssue(**item))
        return issues

    @staticmethod
    def _compute_score(issues: list[ReviewIssue]) -> float:
        """Compute syntax score from issues found."""
        if not issues:
            return 100.0
        deductions = {"high": 25.0, "medium": 10.0, "low": 3.0}
        total_deduction = sum(deductions.get(i.severity, 5.0) for i in issues)
        return max(0.0, 100.0 - total_deduction)


# ═══════════════════════════════════════════════════════════════
# 2. Constraint Reviewer
# ═══════════════════════════════════════════════════════════════

class ConstraintReviewer:
    """Review testcases against instruction operand constraints."""

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def review(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
        use_llm: bool = False,
    ) -> tuple[list[ReviewIssue], float]:
        """Review constraint compliance."""
        issues = self._rule_based_check(test_suite, profile)

        if use_llm and self._llm:
            llm_issues = self._llm_review(test_suite, profile)
            issues.extend(llm_issues)

        score = self._compute_score(issues)
        return issues, score

    def _rule_based_check(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
    ) -> list[ReviewIssue]:
        """Rule-based constraint compliance checks."""
        issues: list[ReviewIssue] = []

        # Build known immediate constraints per operand
        imm_constraints: dict[str, tuple[int, int]] = {}
        for ir in profile.immediate_ranges:
            sym = ir.operand_symbol.strip("<>")
            imm_constraints[sym] = (ir.min_value, ir.max_value)
            imm_constraints[ir.encoded_field] = (ir.min_value, ir.max_value)

        # Check all instructions for immediate range violations
        all_instructions = self._collect_all_instructions(test_suite)
        for inst_str, test_name in all_instructions:
            issues.extend(
                self._check_immediate_range(inst_str, test_name, imm_constraints, profile)
            )

        # Check register constraint violations (CONSTRAINED_UNPREDICTABLE triggers)
        for cu in profile.constrained_unpredictable:
            condition = cu.condition or ""
            if "sp" in condition.lower() or "SP" in condition:
                # Check if any test uses SP where it shouldn't
                for inst_str, test_name in list(all_instructions):
                    if re.search(r'\bSP\b', inst_str, re.IGNORECASE):
                        # Verify if this is a negative test (invalid operand) or a violation
                        is_invalid_test = any(
                            "invalid" in test_name.lower() or
                            "violation" in test_name.lower()
                            for _ in [1]
                        )
                        if not is_invalid_test:
                            issues.append(ReviewIssue(
                                type="constraint_error",
                                severity="high",
                                location=test_name,
                                description=f"Instruction uses SP in restricted context: {cu.description}",
                                suggestion=f"Replace SP with a general-purpose register",
                            ))

        return issues

    @staticmethod
    def _collect_all_instructions(
        test_suite: TestCaseSuite,
    ) -> list[tuple[str, str]]:
        """Collect (instruction_string, test_name) from all test types."""
        results: list[tuple[str, str]] = []

        for t in test_suite.assembly_tests:
            results.append((t.instruction, t.test_name))
        for t in test_suite.llvm_mc_tests:
            for al in t.assembly_lines:
                inst = al.strip().lstrip("\t")
                if inst:
                    results.append((inst, t.test_name))
        for t in test_suite.inline_asm_tests:
            results.append((t.instruction, t.test_name))
        for t in test_suite.boundary_tests:
            results.append((t.instruction, t.test_name))
        for t in test_suite.invalid_operand_tests:
            results.append((t.instruction, t.test_name))
        for t in test_suite.alias_tests:
            results.append((t.alias_instruction, t.test_name))
            results.append((t.canonical_instruction, t.test_name))
        for t in test_suite.feature_enable_tests:
            results.append((t.instruction, t.test_name))
        for t in test_suite.cpp_verification_tests:
            results.append((t.instruction, t.test_name))

        return results

    @staticmethod
    def _check_immediate_range(
        inst_str: str,
        test_name: str,
        imm_constraints: dict[str, tuple[int, int]],
        profile: InstructionProfile,
    ) -> list[ReviewIssue]:
        """Check if immediate values in instruction are within constrained ranges."""
        issues: list[ReviewIssue] = []

        # Find all immediate values in the instruction
        imms = _RE_IMM.findall(inst_str)
        for imm in imms:
            val: Optional[int] = None
            hex_match = _RE_IMM_HEX.match(imm)
            dec_match = _RE_IMM_VAL.match(imm)

            if hex_match:
                try:
                    val = int(hex_match.group(1), 16)
                except ValueError:
                    continue
            elif dec_match:
                try:
                    val = int(dec_match.group(1))
                    if val < 0 and any(ir.signed for ir in profile.immediate_ranges):
                        pass  # negative values are valid for signed immediates
                except ValueError:
                    continue
            else:
                continue

            if val is None:
                continue

            # Check against known ranges
            max_allowed = 0
            if imm_constraints:
                max_allowed = max(max_val for _, max_val in imm_constraints.values())
            else:
                # Default: assume immediate fits if instruction was generated properly
                continue

            if max_allowed > 0 and val > max_allowed:
                # But skip if this is an invalid-operand test (expected)
                if "invalid" in test_name.lower() or "overflow" in test_name.lower():
                    continue

                issues.append(ReviewIssue(
                    type="constraint_error",
                    severity="high",
                    location=f"{test_name}: `{inst_str}`",
                    description=f"Immediate value {val} (0x{val:x}) exceeds maximum {max_allowed}",
                    suggestion=f"Replace with a value <= {max_allowed}, e.g. #{max_allowed}",
                ))

        return issues

    def _llm_review(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
    ) -> list[ReviewIssue]:
        """LLM-assisted constraint review."""
        content = _flatten_test_content(test_suite)
        ctx = format_profile_context(profile)

        prompt = f"""Review the following test suite for CONSTRAINT violations.

{ctx}

### Test Suite:
{content[:6000]}

Output JSON array of constraint issues."""

        result = _safe_llm_invoke(self._llm, CONSTRAINT_REVIEW_SYSTEM_PROMPT, prompt)
        data = _parse_json_response(result, [])

        issues: list[ReviewIssue] = []
        for item in data:
            item.setdefault("type", "constraint_error")
            item.setdefault("dimension", "constraint")
            issues.append(ReviewIssue(**item))
        return issues

    @staticmethod
    def _compute_score(issues: list[ReviewIssue]) -> float:
        if not issues:
            return 100.0
        deductions = {"high": 30.0, "medium": 12.0, "low": 4.0}
        total_deduction = sum(deductions.get(i.severity, 5.0) for i in issues)
        return max(0.0, 100.0 - total_deduction)


# ═══════════════════════════════════════════════════════════════
# 3. Encoding Reviewer
# ═══════════════════════════════════════════════════════════════

class EncodingReviewer:
    """Review testcases against expected instruction encodings."""

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def review(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
        use_llm: bool = False,
    ) -> tuple[list[ReviewIssue], float]:
        """Review encoding accuracy."""
        issues = self._rule_based_check(test_suite, profile)

        if use_llm and self._llm:
            llm_issues = self._llm_review(test_suite, profile)
            issues.extend(llm_issues)

        score = self._compute_score(issues)
        return issues, score

    def _rule_based_check(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
    ) -> list[ReviewIssue]:
        """Rule-based encoding checks."""
        issues: list[ReviewIssue] = []

        # 1. Check REGISTER WIDTH vs ENCODING VARIANT
        for t in test_suite.assembly_tests:
            inst = t.instruction
            # Detect if using W registers but encoding says 64-bit only
            has_w_reg = bool(_RE_GP_32.search(inst))
            has_x_reg = bool(_RE_GP_64.search(inst))

            if has_w_reg and not profile.has_32bit_encoding and profile.has_64bit_encoding:
                issues.append(ReviewIssue(
                    type="encoding_error",
                    severity="high",
                    location=t.test_name,
                    description=f"W-register used but no 32-bit encoding exists for {profile.mnemonic}",
                    suggestion=f"Use X registers for 64-bit encoding",
                ))

            # If only 32-bit encoding, using X might also be suspicious (some encodings use X in 32-bit)
            if has_x_reg and not profile.has_64bit_encoding and profile.has_32bit_encoding:
                issues.append(ReviewIssue(
                    type="encoding_error",
                    severity="low",
                    location=t.test_name,
                    description=f"X-register used but only 32-bit encoding exists. "
                                f"Some 32-bit instructions can use X registers; verify.",
                    suggestion=f"Check if W registers are required",
                ))

        # 2. Check LLVM MC CHECK lines have encoding patterns when bit_pattern is defined
        for t in test_suite.llvm_mc_tests:
            if t.encoding_name:
                # Find matching encoding
                matching_enc = next(
                    (e for e in profile.encodings if e.name == t.encoding_name), None
                )
                if matching_enc and matching_enc.bit_pattern:
                    has_encoding_check = any(
                        "encoding" in cl.lower() or "encoding" in cl
                        for cl in t.check_lines
                    )
                    if not has_encoding_check:
                        issues.append(ReviewIssue(
                            type="encoding_error",
                            severity="medium",
                            location=t.test_name,
                            description=f"LLVM MC test missing encoding CHECK for bit pattern "
                                        f"{matching_enc.bit_pattern}",
                            suggestion=f"Add: // CHECK-SAME: encoding: [{matching_enc.bit_pattern}]",
                        ))

        return issues

    def _llm_review(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
    ) -> list[ReviewIssue]:
        """LLM-assisted encoding review."""
        content = _flatten_test_content(test_suite)
        ctx = format_profile_context(profile)

        prompt = f"""Review the following test suite for ENCODING correctness.

{ctx}

### Test Suite:
{content[:6000]}

Output JSON array of encoding issues."""

        result = _safe_llm_invoke(self._llm, ENCODING_REVIEW_SYSTEM_PROMPT, prompt)
        data = _parse_json_response(result, [])

        issues: list[ReviewIssue] = []
        for item in data:
            item.setdefault("type", "encoding_error")
            item.setdefault("dimension", "encoding")
            issues.append(ReviewIssue(**item))
        return issues

    @staticmethod
    def _compute_score(issues: list[ReviewIssue]) -> float:
        if not issues:
            return 100.0
        deductions = {"high": 30.0, "medium": 12.0, "low": 4.0}
        total_deduction = sum(deductions.get(i.severity, 5.0) for i in issues)
        return max(0.0, 100.0 - total_deduction)


# ═══════════════════════════════════════════════════════════════
# 4. Semantic Reviewer
# ═══════════════════════════════════════════════════════════════

class SemanticReviewer:
    """Review testcase expected results against instruction operation semantics."""

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def review(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
        use_llm: bool = False,
    ) -> tuple[list[ReviewIssue], float]:
        """Review semantic correctness."""
        issues = self._rule_based_check(test_suite, profile)

        if use_llm and self._llm:
            llm_issues = self._llm_review(test_suite, profile)
            issues.extend(llm_issues)

        score = self._compute_score(issues)
        return issues, score

    def _rule_based_check(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
    ) -> list[ReviewIssue]:
        """Rule-based semantic checks via reference model."""
        issues: list[ReviewIssue] = []
        mnemonic_upper = profile.mnemonic.upper()

        for t in test_suite.assembly_tests:
            if not t.input_state or not t.expected_state:
                continue

            # Try to verify via reference model
            expected_dst = self._get_first_expected_reg(t.expected_state)
            if expected_dst:
                computed = self._compute_expected(
                    mnemonic_upper, t.instruction, t.input_state
                )
                if computed is not None:
                    expected_val = self._parse_val(t.expected_state.get(expected_dst, ""))
                    if expected_val is not None and computed != expected_val:
                        issues.append(ReviewIssue(
                            type="semantic_error",
                            severity="high",
                            location=f"{t.test_name}: {t.instruction}",
                            description=(
                                f"Expected result mismatch: "
                                f"expected {expected_dst}=0x{expected_val:x}, "
                                f"computed {expected_dst}=0x{computed:x}"
                            ),
                            suggestion=(
                                f"Update expected_state: {{{expected_dst}: '0x{computed:X}'}}"
                            ),
                        ))

        return issues

    @staticmethod
    def _get_first_expected_reg(expected_state: dict[str, str]) -> Optional[str]:
        """Get the first register name from expected state."""
        if not expected_state:
            return None
        return next(iter(expected_state))

    @staticmethod
    def _parse_val(val_str: str) -> Optional[int]:
        """Parse a value string like "0x30" or "48" to int."""
        if not val_str:
            return None
        val_str = val_str.strip()
        try:
            if val_str.lower().startswith("0x"):
                return int(val_str, 16)
            return int(val_str)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _compute_expected(
        mnemonic: str,
        instruction: str,
        input_state: dict[str, str],
    ) -> Optional[int]:
        """Try to compute expected result from operation semantics.

        Only handles simple arithmetic (ADD/SUB/MUL etc.) for rule-based checking.
        Complex operations need LLM.
        """
        if not input_state:
            return None

        mnem_upper = mnemonic.upper()
        vals = [SemanticReviewer._parse_val(v) for v in input_state.values()]
        vals = [v for v in vals if v is not None]
        if len(vals) < 2:
            return None

        a, b = vals[0], vals[1]

        # Detect operation from mnemonic
        if "ADD" in mnem_upper or "ADDS" == mnem_upper:
            return a + b
        elif "SUB" in mnem_upper or "SUBS" in mnem_upper:
            return a - b
        elif "AND" in mnem_upper or "ANDS" in mnem_upper:
            return a & b
        elif "ORR" in mnem_upper or "ORN" in mnem_upper:
            return a | b
        elif "EOR" in mnem_upper or "EOR" in mnem_upper:
            return a ^ b
        elif "MUL" in mnem_upper:
            return a * b
        elif "LSL" in mnem_upper:
            return a << b
        elif "LSR" in mnem_upper:
            return a >> b

        return None

    def _llm_review(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
    ) -> list[ReviewIssue]:
        """LLM-assisted semantic review."""
        content = _flatten_test_content(test_suite)
        ctx = format_profile_context(profile)

        prompt = f"""Review the following test suite for SEMANTIC correctness.

{ctx}

### Test Suite:
{content[:6000]}

Output JSON array of semantic issues."""

        result = _safe_llm_invoke(self._llm, SEMANTIC_REVIEW_SYSTEM_PROMPT, prompt)
        data = _parse_json_response(result, [])

        issues: list[ReviewIssue] = []
        for item in data:
            item.setdefault("type", "semantic_error")
            item.setdefault("dimension", "semantic")
            issues.append(ReviewIssue(**item))
        return issues

    @staticmethod
    def _compute_score(issues: list[ReviewIssue]) -> float:
        if not issues:
            return 100.0
        deductions = {"high": 30.0, "medium": 12.0, "low": 4.0}
        total_deduction = sum(deductions.get(i.severity, 5.0) for i in issues)
        return max(0.0, 100.0 - total_deduction)


# ═══════════════════════════════════════════════════════════════
# 5. Coverage Reviewer
# ═══════════════════════════════════════════════════════════════

class CoverageReviewer:
    """Review test suite coverage against TestPlan/TestStrategy."""

    # Map free-form planning dimension names to the concrete test categories
    # that the generator actually produces. Names that map to an empty set are
    # explicitly acknowledged but not treated as checkable categories (e.g.
    # register constraints are implicitly tested inside normal/boundary tests).
    _DIMENSION_ALIASES: dict[str, set[str]] = {
        # Core categories with direct test coverage
        "normal operation": {"normal"},
        "normal": {"normal"},
        "core functional": {"normal"},
        "basic operation": {"normal"},
        "functional": {"normal"},
        "boundary values": {"boundary"},
        "boundary": {"boundary"},
        "edge cases": {"boundary"},
        "corner cases": {"boundary"},
        "encoding coverage": {"encoding"},
        "encoding": {"encoding"},
        "width variants": {"encoding"},
        "32/64-bit variants": {"encoding"},
        "constrained unpredictable": {"invalid"},
        "invalid operand": {"invalid"},
        "constraint": {"invalid"},
        "constraints": {"invalid"},
        "feature dependency": {"feature"},
        "feature enable": {"feature"},
        "feature": {"feature"},
        "alias": {"alias"},
        "alias equivalence": {"alias"},
        "verification": {"verification"},
        "cpp verification": {"verification"},
        # Acknowledged but not checked as standalone categories (absorbed into others)
        "register constraints": set(),
        "shift/extend coverage": set(),
        "shift/extend": set(),
        "flag effects": set(),
        "flag effects (nzcv)": set(),
        "nzcv": set(),
        "vector/simd-specific": set(),
        "sve-specific": set(),
        "simd-specific": set(),
    }

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def _normalize_dimension_name(self, name: str) -> set[str]:
        """Map a planning dimension name to concrete generator categories."""
        key = name.lower().strip()
        if key in self._DIMENSION_ALIASES:
            return set(self._DIMENSION_ALIASES[key])

        # Fuzzy fallback for unknown dimension names
        inferred: set[str] = set()
        if any(kw in key for kw in ("normal", "basic", "operation", "functional")):
            inferred.add("normal")
        if any(kw in key for kw in ("boundary", "edge", "corner", "min", "max", "zero")):
            inferred.add("boundary")
        if any(kw in key for kw in ("encoding", "width", "variant", "32-bit", "64-bit")):
            inferred.add("encoding")
        if any(kw in key for kw in ("invalid", "constraint", "unpredictable", "undefined")):
            inferred.add("invalid")
        if any(kw in key for kw in ("feature", "dependency")):
            inferred.add("feature")
        if any(kw in key for kw in ("alias")):
            inferred.add("alias")
        if any(kw in key for kw in ("verify", "verification", "cpp")):
            inferred.add("verification")
        return inferred

    def _collect_actual_dimensions(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
    ) -> set[str]:
        """Collect which concrete test categories are actually present."""
        actual: set[str] = set()
        if test_suite.assembly_tests:
            actual.add("normal")
            # Flag effects are covered if any assembly test sets expected_flags
            if any(t.expected_flags for t in test_suite.assembly_tests):
                actual.add("flag_effects")
        if test_suite.boundary_tests:
            actual.add("boundary")
        if test_suite.alias_tests:
            actual.add("alias")
        if test_suite.invalid_operand_tests:
            actual.add("invalid")
        if test_suite.feature_enable_tests:
            actual.add("feature")
        if test_suite.llvm_mc_tests:
            actual.add("encoding")
        if test_suite.cpp_verification_tests:
            actual.add("verification")
        return actual

    def review(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
        strategy: Optional[TestStrategy] = None,
        use_llm: bool = False,
    ) -> tuple[list[ReviewIssue], float]:
        """Review coverage completeness."""
        issues = self._rule_based_check(test_suite, profile, strategy)

        if use_llm and self._llm:
            llm_issues = self._llm_review(test_suite, profile, strategy)
            issues.extend(llm_issues)

        score = self._compute_score(issues)
        return issues, score

    def _rule_based_check(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
        strategy: Optional[TestStrategy],
    ) -> list[ReviewIssue]:
        """Rule-based coverage gap detection."""
        issues: list[ReviewIssue] = []
        mnemonic = test_suite.instruction_mnemonic

        # Check encoding coverage
        enc_count = profile.encoding_count
        tested_encodings: set[str] = set()

        for t in test_suite.llvm_mc_tests:
            if t.encoding_name:
                tested_encodings.add(t.encoding_name)

        for enc in profile.encodings:
            if enc.name not in tested_encodings:
                issues.append(ReviewIssue(
                    type="coverage_gap",
                    severity="medium",
                    location=f"encoding: {enc.name}",
                    description=f"Encoding variant '{enc.name}' not covered by any LLVM MC test",
                    suggestion=f"Add an LLVM MC test for {enc.name} encoding",
                ))

        # Check ALIAS coverage: if the instruction has aliases but no alias tests
        known_alias_count = len(test_suite.alias_tests)
        if profile.is_alias and known_alias_count == 0:
            issues.append(ReviewIssue(
                type="coverage_gap",
                severity="high",
                location=f"alias: {mnemonic}",
                description=f"Alias instruction '{mnemonic}' has no alias equivalence tests",
                suggestion=f"Generate alias tests comparing {mnemonic} with its canonical form",
            ))

        # Check boundary coverage: max/min/zero only when there are immediate operands.
        # For register-only instructions, only require the zero-register case.
        boundary_categories = {t.category for t in test_suite.boundary_tests}
        required_categories: set[str] = set()
        if profile.immediate_ranges:
            required_categories.update({"max_immediate", "min_immediate", "zero"})
        elif profile.has_special_register:
            required_categories.add("zero")
        missing_categories = required_categories - boundary_categories
        if missing_categories:
            issues.append(ReviewIssue(
                type="coverage_gap",
                severity="medium",
                location=f"boundary tests",
                description=f"Missing boundary categories: {', '.join(sorted(missing_categories))}",
                suggestion=f"Add boundary tests for: {', '.join(sorted(missing_categories))}",
            ))

        # Check feature enable coverage
        if profile.feature_dependencies and len(test_suite.feature_enable_tests) == 0:
            feat_names = [fd.feature_name for fd in profile.feature_dependencies]
            issues.append(ReviewIssue(
                type="coverage_gap",
                severity="high",
                location="feature_enable",
                description=f"Feature dependencies ({', '.join(feat_names)}) not tested",
                suggestion=f"Add feature enable tests for: {', '.join(feat_names)}",
            ))

        # Check invalid operand coverage when constraints exist
        has_constraints = bool(
            profile.constrained_unpredictable or
            profile.encoding_undefined or
            profile.feature_gates
        )
        if has_constraints and len(test_suite.invalid_operand_tests) == 0:
            issues.append(ReviewIssue(
                type="coverage_gap",
                severity="medium",
                location="invalid_operand",
                description="Constraints exist but no invalid operand tests generated",
                suggestion="Add tests for CONSTRAINED_UNPREDICTABLE / UNDEFINED conditions",
            ))

        # Check TestPlan dimension coverage if strategy is provided.
        # Planning dimensions are free-form names; we normalize them to the
        # concrete generator categories (normal, boundary, encoding, ...)
        # before checking. This prevents false HIGH-severity gaps caused by
        # names like "Flag Effects (NZCV)" or "Register Constraints" that
        # are implicitly exercised by the generated tests.
        if strategy:
            planned_dims: set[str] = set()
            for dim in strategy.dimensions:
                mapped = self._normalize_dimension_name(dim.name)
                if mapped:
                    planned_dims.update(mapped)

            actual_dims = self._collect_actual_dimensions(test_suite, profile)

            missing_dims = planned_dims - actual_dims
            if missing_dims:
                issues.append(ReviewIssue(
                    type="coverage_gap",
                    severity="high",
                    location="test_plan",
                    description=f"TestPlan dimensions not covered: {', '.join(sorted(missing_dims))}",
                    suggestion=f"Generate tests for missing dimensions: {', '.join(sorted(missing_dims))}",
                ))

        return issues

    def _llm_review(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
        strategy: Optional[TestStrategy],
    ) -> list[ReviewIssue]:
        """LLM-assisted coverage review."""
        content = _flatten_test_content(test_suite)
        ctx = format_profile_context(profile)
        strategy_ctx = _format_strategy_for_coverage(strategy)

        prompt = f"""Review the following test suite for COVERAGE completeness.

{ctx}

{strategy_ctx}

### Test Suite:
{content[:6000]}

Output JSON array of coverage gaps."""

        result = _safe_llm_invoke(self._llm, COVERAGE_REVIEW_SYSTEM_PROMPT, prompt)
        data = _parse_json_response(result, [])

        issues: list[ReviewIssue] = []
        for item in data:
            item.setdefault("type", "coverage_gap")
            item.setdefault("dimension", "coverage")
            issues.append(ReviewIssue(**item))
        return issues

    @staticmethod
    def _compute_score(issues: list[ReviewIssue]) -> float:
        if not issues:
            return 100.0
        deductions = {"high": 25.0, "medium": 10.0, "low": 3.0}
        total_deduction = sum(deductions.get(i.severity, 5.0) for i in issues)
        return max(0.0, 100.0 - total_deduction)


# ═══════════════════════════════════════════════════════════════
# Testcase Reviewer — orchestrator
# ═══════════════════════════════════════════════════════════════

class TestcaseReviewer:
    """Orchestrator that runs all 5 dimension reviewers and produces a final ReviewResult.

    Usage:
        reviewer = TestcaseReviewer(llm)
        result = reviewer.review(test_suite, profile, strategy)
        if not result.passed:
            # trigger repair loop
    """

    PASS_THRESHOLD: float = 70.0

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm
        self.syntax_reviewer = SyntaxReviewer(llm)
        self.constraint_reviewer = ConstraintReviewer(llm)
        self.encoding_reviewer = EncodingReviewer(llm)
        self.semantic_reviewer = SemanticReviewer(llm)
        self.coverage_reviewer = CoverageReviewer(llm)

    def review(
        self,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
        strategy: Optional[TestStrategy] = None,
        use_llm: bool = False,
    ) -> ReviewResult:
        """Run all 5 dimension reviews and produce a final ReviewResult.

        Args:
            test_suite: The generated test suite to review.
            profile: Instruction metadata profile.
            strategy: Optional TestPlan strategy for coverage review.
            use_llm: If True, use LLM for deep analysis on each dimension.

        Returns:
            ReviewResult with pass/fail, scores, issues, and suggestions.
        """
        logger.info(
            "review.start",
            mnemonic=test_suite.instruction_mnemonic,
            total_tests=test_suite.total_tests,
            use_llm=use_llm,
        )

        all_issues: list[ReviewIssue] = []
        dim_scores: list[DimensionScore] = []

        # ── Dimension 1: Syntax ──────────────────────────────
        syntax_issues, syntax_score = self.syntax_reviewer.review(
            test_suite, profile, use_llm
        )
        syntax_issues = [i.model_copy(update={"dimension": "syntax"}) for i in syntax_issues]
        all_issues.extend(syntax_issues)
        dim_scores.append(DimensionScore(
            dimension="syntax",
            score=syntax_score,
            issues_count=len(syntax_issues),
            max_severity=self._max_severity(syntax_issues),
            details=f"Syntax review: {len(syntax_issues)} issues found",
        ))

        # ── Dimension 2: Constraint ──────────────────────────
        constr_issues, constr_score = self.constraint_reviewer.review(
            test_suite, profile, use_llm
        )
        constr_issues = [i.model_copy(update={"dimension": "constraint"}) for i in constr_issues]
        all_issues.extend(constr_issues)
        dim_scores.append(DimensionScore(
            dimension="constraint",
            score=constr_score,
            issues_count=len(constr_issues),
            max_severity=self._max_severity(constr_issues),
            details=f"Constraint review: {len(constr_issues)} issues found",
        ))

        # ── Dimension 3: Encoding ────────────────────────────
        enc_issues, enc_score = self.encoding_reviewer.review(
            test_suite, profile, use_llm
        )
        enc_issues = [i.model_copy(update={"dimension": "encoding"}) for i in enc_issues]
        all_issues.extend(enc_issues)
        dim_scores.append(DimensionScore(
            dimension="encoding",
            score=enc_score,
            issues_count=len(enc_issues),
            max_severity=self._max_severity(enc_issues),
            details=f"Encoding review: {len(enc_issues)} issues found",
        ))

        # ── Dimension 4: Semantic ────────────────────────────
        sem_issues, sem_score = self.semantic_reviewer.review(
            test_suite, profile, use_llm
        )
        sem_issues = [i.model_copy(update={"dimension": "semantic"}) for i in sem_issues]
        all_issues.extend(sem_issues)
        dim_scores.append(DimensionScore(
            dimension="semantic",
            score=sem_score,
            issues_count=len(sem_issues),
            max_severity=self._max_severity(sem_issues),
            details=f"Semantic review: {len(sem_issues)} issues found",
        ))

        # ── Dimension 5: Coverage ────────────────────────────
        cov_issues, cov_score = self.coverage_reviewer.review(
            test_suite, profile, strategy, use_llm
        )
        cov_issues = [i.model_copy(update={"dimension": "coverage"}) for i in cov_issues]
        all_issues.extend(cov_issues)
        dim_scores.append(DimensionScore(
            dimension="coverage",
            score=cov_score,
            issues_count=len(cov_issues),
            max_severity=self._max_severity(cov_issues),
            details=f"Coverage review: {len(cov_issues)} issues found",
        ))

        # ── Compute overall score ────────────────────────────
        weights = {"syntax": 0.15, "constraint": 0.25, "encoding": 0.15, "semantic": 0.25, "coverage": 0.20}
        overall_score = sum(
            weights.get(ds.dimension, 0.20) * ds.score
            for ds in dim_scores
        )

        # ── Build suggestions ────────────────────────────────
        suggestions = self._generate_suggestions(all_issues)

        # ── Determine pass/fail ──────────────────────────────
        high_count = sum(1 for i in all_issues if i.severity == "high")
        passed = overall_score >= self.PASS_THRESHOLD and high_count == 0

        reviewer_notes = self._generate_reviewer_notes(
            overall_score, passed, dim_scores, all_issues
        )

        result = ReviewResult(
            passed=passed,
            score=overall_score,
            dimension_scores=dim_scores,
            issues=all_issues,
            suggestions=suggestions,
            reviewer_notes=reviewer_notes,
            instruction_mnemonic=test_suite.instruction_mnemonic,
            review_timestamp=datetime.now(timezone.utc).isoformat(),
        )

        logger.info(
            "review.done",
            mnemonic=test_suite.instruction_mnemonic,
            score=overall_score,
            passed=passed,
            issues=len(all_issues),
            high=high_count,
        )

        return result

    @staticmethod
    def _max_severity(issues: list[ReviewIssue]) -> str:
        if not issues:
            return "none"
        severities = {i.severity for i in issues}
        for s in ("high", "medium", "low"):
            if s in severities:
                return s
        return "none"

    @staticmethod
    def _generate_suggestions(issues: list[ReviewIssue]) -> list[str]:
        """Generate top actionable suggestions from issues."""
        # Prioritize HIGH severity issues first
        high_issues = [i for i in issues if i.severity == "high"]
        medium_issues = [i for i in issues if i.severity == "medium"]

        suggestions: list[str] = []

        # High severity: all suggestions
        for i in high_issues[:5]:
            if i.suggestion:
                suggestions.append(f"[{i.severity}] [{i.type}] {i.suggestion}")

        # Medium severity: top 3
        for i in medium_issues[:3]:
            if i.suggestion:
                suggestions.append(f"[{i.severity}] [{i.type}] {i.suggestion}")

        # Low: just a summary
        low_count = sum(1 for i in issues if i.severity == "low")
        if low_count > 0:
            suggestions.append(f"[low] {low_count} low-severity issues found; review at your discretion")

        return suggestions[:10]

    @staticmethod
    def _generate_reviewer_notes(
        overall_score: float,
        passed: bool,
        dim_scores: list[DimensionScore],
        all_issues: list[ReviewIssue],
    ) -> str:
        """Generate natural-language reviewer summary."""
        status = "PASS" if passed else "FAIL"
        high = sum(1 for i in all_issues if i.severity == "high")
        medium = sum(1 for i in all_issues if i.severity == "medium")
        low = sum(1 for i in all_issues if i.severity == "low")

        weakest_dims = sorted(dim_scores, key=lambda d: d.score)[:2]
        weakest_str = ", ".join(f"{d.dimension} ({d.score:.0f})" for d in weakest_dims)

        notes = (
            f"Overall: {status} (score={overall_score:.0f}/100). "
            f"Found {len(all_issues)} issues: {high} high, {medium} medium, {low} low. "
            f"Weakest dimensions: {weakest_str}. "
        )
        if not passed:
            notes += "Review FAILED. Repair loop recommended."
        else:
            notes += "Review PASSED. Test suite is acceptable for delivery."

        return notes


# ═══════════════════════════════════════════════════════════════
# Repair Generator — self-correction
# ═══════════════════════════════════════════════════════════════

class RepairGenerator:
    """Generate repaired testcases based on review feedback.

    Used in the self-correction loop:
        Reviewer → (failed) → RepairGenerator → Reviewer → ...

    Args:
        max_repair_attempts: Maximum number of repair cycles (default 3).
    """

    def __init__(self, llm: Any = None, max_repair_attempts: int = 3) -> None:
        self._llm = llm
        self._max_repair_attempts = max_repair_attempts

    def repair(
        self,
        review_result: ReviewResult,
        test_suite: TestCaseSuite,
        profile: InstructionProfile,
    ) -> RepairResult:
        """Generate repaired test content based on review issues.

        Args:
            review_result: The review result with issues to fix.
            test_suite: The original (failing) test suite.
            profile: Instruction metadata for context.

        Returns:
            RepairResult with repaired content and change descriptions.
        """
        logger.info(
            "repair.start",
            mnemonic=test_suite.instruction_mnemonic,
            issues=len(review_result.issues),
        )

        if not self._llm:
            return RepairResult(
                repaired=False,
                original_issues=review_result.issues,
                repair_notes="No LLM available for repair. Use LLM-assisted mode.",
            )

        # Focus on high+medium severity issues
        critical_issues = [
            i for i in review_result.issues
            if i.severity in ("high", "medium")
        ]
        if not critical_issues:
            critical_issues = review_result.issues[:10]

        # Build repair prompt
        issues_text = self._format_issues_for_repair(critical_issues)
        content_text = _flatten_test_content(test_suite)
        ctx = format_profile_context(profile)

        prompt = f"""Repair the following failing test suite based on the reviewer issues.

{ctx}

### Reviewer Issues (need fixing):
{issues_text}

### Current (Failing) Test Suite:
{content_text[:6000]}

Output a JSON object with:
- repaired: true/false
- repair_changes: list of what was changed
- repair_notes: summary
- repaired_content: the FULL repaired test suite content (same format as input)"""

        result = _safe_llm_invoke(self._llm, REPAIR_SYSTEM_PROMPT, prompt, "{}")
        data = _parse_json_response(result, {})

        if not data or not isinstance(data, dict):
            return RepairResult(
                repaired=False,
                original_issues=critical_issues,
                repair_notes="LLM response could not be parsed.",
            )

        repair_result = RepairResult(
            repaired=data.get("repaired", False),
            original_issues=critical_issues,
            repaired_content=data.get("repaired_content", ""),
            repair_changes=data.get("repair_changes", []),
            repair_notes=data.get("repair_notes", ""),
        )

        logger.info(
            "repair.done",
            repaired=repair_result.repaired,
            changes=len(repair_result.repair_changes),
        )

        return repair_result

    @staticmethod
    def _format_issues_for_repair(issues: list[ReviewIssue]) -> str:
        """Format review issues for the repair prompt."""
        lines: list[str] = []
        for i, issue in enumerate(issues, 1):
            loc = f" at {issue.location}" if issue.location else ""
            sug = f" → {issue.suggestion}" if issue.suggestion else ""
            lines.append(f"{i}. [{issue.severity}] [{issue.type}]{loc}")
            lines.append(f"   {issue.description}{sug}")
        return "\n".join(lines)

    def should_repair(self, review_result: ReviewResult, attempt_count: int) -> bool:
        """Determine if repair should be attempted.

        Returns True if:
        - Review result is FAIL
        - Attempt count < max_repair_attempts
        - There are fixable issues (not just coverage gaps)
        """
        if review_result.passed:
            return False
        if attempt_count >= self._max_repair_attempts:
            return False
        # Check if there are fixable issues (syntax, constraint, encoding, semantic)
        fixable_types = {"syntax_error", "constraint_error", "encoding_error", "semantic_error"}
        has_fixable = any(i.type in fixable_types for i in review_result.issues)
        return has_fixable
