"""Testcase Generator tools — unified tool interface for the Agent to invoke generators."""

from __future__ import annotations

import json
from typing import Optional

import structlog

from arm_isa_agent.agent.tool_registry import get_llm, get_sqlite, register_tool
from arm_isa_agent.generation.generators import TestCaseSuiteGenerator
from arm_isa_agent.planning.analyzer import InstructionAnalyzer

logger = structlog.get_logger(__name__)


# ── generate_test_suite ──────────────────────────────────────────

@register_tool(
    "generate_test_suite",
    "Generate a comprehensive test suite for an ARM instruction across multiple formats. "
    "Outputs: ARM assembly tests, LLVM MC CHECK tests, GCC inline assembly tests, "
    "C++ verification programs, boundary value tests, alias tests, invalid operand tests, "
    "and feature enable tests. "
    "Use when the user asks to 'generate tests', 'create test cases', 'build a test suite'.",
)
def generate_test_suite(
    mnemonic: str,
    test_types: str = "all",
    use_llm: str = "false",
    output_format: str = "markdown",
) -> str:
    """Generate a complete test suite for an ARM instruction.

    Args:
        mnemonic: ARM instruction mnemonic, e.g. "ADD", "LDR", "STP".
        test_types: Comma-separated list of test types to generate, or "all".
                    Options: assembly, llvm_mc, inline_asm, cpp_verify, boundary,
                            alias, invalid_operand, feature_enable.
        use_llm: "true" to use LLM-assisted generation, "false" for rule-based (default).
        output_format: "markdown" for human-readable, "json" for structured output.

    Returns:
        Generated test suite in the requested format.
    """
    try:
        sqlite = get_sqlite()
        llm = get_llm() if use_llm.lower() in ("true", "1", "yes") else None

        # Build profile from SQLite
        analyzer = InstructionAnalyzer(sqlite)
        profile = analyzer.extract_profile(mnemonic=mnemonic)
        if profile is None:
            return json.dumps({
                "error": f"Instruction '{mnemonic}' not found in knowledge base",
                "suggestion": "Try a different mnemonic or check spelling",
            }, ensure_ascii=False)

        # Parse test types
        if test_types.lower() in ("all", ""):
            selected_types = None
        else:
            selected_types = [t.strip() for t in test_types.split(",") if t.strip()]

        # Generate suite
        generator = TestCaseSuiteGenerator(llm=llm, sqlite_client=sqlite)
        suite = generator.generate_suite(
            profile=profile,
            use_llm=use_llm.lower() in ("true", "1", "yes"),
            test_types=selected_types,
        )

        if output_format.lower() == "json":
            return suite.model_dump_json(indent=2)

        return suite.to_markdown_summary()

    except Exception as e:
        logger.error("generate_test_suite.error", error=str(e)[:300])
        return json.dumps({
            "error": f"Test suite generation failed: {str(e)[:300]}",
        }, ensure_ascii=False)


# ── generate_asm_tests ───────────────────────────────────────────

@register_tool(
    "generate_asm_tests",
    "Generate standalone ARM A64 assembly test files (.s) with register initialization "
    "and expected result verification. "
    "Use when the user wants assembly-level test cases.",
)
def generate_asm_tests(mnemonic: str, count: int = 3) -> str:
    """Generate ARM assembly test cases.

    Args:
        mnemonic: ARM instruction mnemonic.
        count: Number of test cases (default 3, max 5).

    Returns:
        Formatted assembly tests.
    """
    try:
        sqlite = get_sqlite()
        analyzer = InstructionAnalyzer(sqlite)
        profile = analyzer.extract_profile(mnemonic=mnemonic)
        if profile is None:
            return json.dumps({"error": f"Instruction '{mnemonic}' not found"}, ensure_ascii=False)

        from arm_isa_agent.generation.generators import ARMAssemblyTestGenerator

        gen = ARMAssemblyTestGenerator()
        tests = gen.generate(profile, count=min(count, 5))

        lines: list[str] = [f"# ARM Assembly Tests for `{mnemonic}`", ""]
        for t in tests:
            lines.append(t.to_assembly_file())
            lines.append("")
        return "\n".join(lines)

    except Exception as e:
        logger.error("generate_asm_tests.error", error=str(e)[:200])
        return json.dumps({"error": str(e)[:300]}, ensure_ascii=False)


# ── generate_llvm_mc_tests ───────────────────────────────────────

@register_tool(
    "generate_llvm_mc_tests",
    "Generate LLVM MC test cases with CHECK directives for ARM instructions. "
    "Use when the user needs llvm-mc compatible tests.",
)
def generate_llvm_mc_tests(mnemonic: str) -> str:
    """Generate LLVM MC CHECK tests.

    Args:
        mnemonic: ARM instruction mnemonic.

    Returns:
        LLVM MC test file content.
    """
    try:
        sqlite = get_sqlite()
        analyzer = InstructionAnalyzer(sqlite)
        profile = analyzer.extract_profile(mnemonic=mnemonic)
        if profile is None:
            return json.dumps({"error": f"Instruction '{mnemonic}' not found"}, ensure_ascii=False)

        from arm_isa_agent.generation.generators import LLVMMCTestGenerator

        gen = LLVMMCTestGenerator()
        tests = gen.generate(profile)

        lines: list[str] = [f"# LLVM MC Tests for `{mnemonic}`", ""]
        for t in tests:
            lines.append(t.to_llvm_mc_text())
            lines.append("")
        return "\n".join(lines)

    except Exception as e:
        logger.error("generate_llvm_mc_tests.error", error=str(e)[:200])
        return json.dumps({"error": str(e)[:300]}, ensure_ascii=False)


# ── generate_inline_asm_tests ────────────────────────────────────

@register_tool(
    "generate_inline_asm_tests",
    "Generate GCC/Clang inline assembly test functions in C for ARM instructions. "
    "Use when the user needs C/C++ embedded assembly tests.",
)
def generate_inline_asm_tests(mnemonic: str, compiler: str = "gcc") -> str:
    """Generate C inline assembly test functions.

    Args:
        mnemonic: ARM instruction mnemonic.
        compiler: "gcc" or "clang" (default: "gcc").

    Returns:
        C code with inline assembly test functions.
    """
    try:
        sqlite = get_sqlite()
        analyzer = InstructionAnalyzer(sqlite)
        profile = analyzer.extract_profile(mnemonic=mnemonic)
        if profile is None:
            return json.dumps({"error": f"Instruction '{mnemonic}' not found"}, ensure_ascii=False)

        from arm_isa_agent.generation.generators import InlineAsmTestGenerator

        gen = InlineAsmTestGenerator()
        tests = gen.generate(profile)

        lines: list[str] = [
            f"// GCC/Clang Inline Assembly Tests for `{mnemonic}`",
            "// Compiler: " + compiler.upper(),
            "",
            '#include <stdint.h>',
            '#include <stdio.h>',
            '#include <stdlib.h>',
            "",
        ]
        for t in tests:
            lines.append(t.to_inline_asm_code())
            lines.append("")
        return "\n".join(lines)

    except Exception as e:
        logger.error("generate_inline_asm_tests.error", error=str(e)[:200])
        return json.dumps({"error": str(e)[:300]}, ensure_ascii=False)


# ── generate_boundary_tests ──────────────────────────────────────

@register_tool(
    "generate_boundary_tests",
    "Generate boundary value test cases for an ARM instruction. "
    "Covers: max/min immediate, zero, overflow, register edges, width boundaries. "
    "Use when the user needs corner case testing.",
)
def generate_boundary_tests(mnemonic: str) -> str:
    """Generate boundary value test cases.

    Args:
        mnemonic: ARM instruction mnemonic.

    Returns:
        Boundary test cases with assembly and expected behavior.
    """
    try:
        sqlite = get_sqlite()
        analyzer = InstructionAnalyzer(sqlite)
        profile = analyzer.extract_profile(mnemonic=mnemonic)
        if profile is None:
            return json.dumps({"error": f"Instruction '{mnemonic}' not found"}, ensure_ascii=False)

        from arm_isa_agent.generation.generators import BoundaryTestGenerator

        gen = BoundaryTestGenerator()
        tests = gen.generate(profile)

        lines: list[str] = [
            f"# Boundary Tests for `{mnemonic}`",
            f"Total: {len(tests)} boundary test cases",
            "",
            "| # | Category | Instruction | Boundary | Expected |",
            "|---|----------|-------------|----------|----------|",
        ]
        for i, t in enumerate(tests, 1):
            lines.append(
                f"| {i} | {t.category} | `{t.instruction}` | "
                f"{t.boundary_value} | {t.expected_behavior[:60]} |"
            )
        lines.append("")
        lines.append("## Detailed Test Cases")
        lines.append("")
        for t in tests:
            lines.append(f"### {t.test_name}")
            lines.append(f"- **Category:** {t.category}")
            lines.append(f"- **Instruction:** `{t.instruction}`")
            lines.append(f"- **Boundary:** {t.boundary_value}")
            lines.append(f"- **Expected:** {t.expected_behavior}")
            if t.risk_assessment:
                lines.append(f"- **Risk:** {t.risk_assessment}")
            if t.input_state:
                inputs = ", ".join(f"{k}={v}" for k, v in t.input_state.items())
                lines.append(f"- **Inputs:** {inputs}")
            if t.expected_state:
                exp = ", ".join(f"{k}={v}" for k, v in t.expected_state.items())
                lines.append(f"- **Expected Output:** {exp}")
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        logger.error("generate_boundary_tests.error", error=str(e)[:200])
        return json.dumps({"error": str(e)[:300]}, ensure_ascii=False)


# ── generate_alias_tests ─────────────────────────────────────────

@register_tool(
    "generate_alias_tests",
    "Generate alias equivalence tests for ARM instructions. "
    "Verifies that alias mnemonics produce identical encoding to their canonical forms. "
    "Use when testing MOV, CMP, NEG, TST, MVN and other ARM aliases.",
)
def generate_alias_tests(mnemonic: str) -> str:
    """Generate alias vs canonical equivalence tests.

    Args:
        mnemonic: ARM instruction mnemonic (either the alias or the canonical).

    Returns:
        Alias equivalence test cases.
    """
    try:
        sqlite = get_sqlite()
        analyzer = InstructionAnalyzer(sqlite)
        profile = analyzer.extract_profile(mnemonic=mnemonic)
        if profile is None:
            return json.dumps({"error": f"Instruction '{mnemonic}' not found"}, ensure_ascii=False)

        from arm_isa_agent.generation.generators import AliasTestGenerator

        gen = AliasTestGenerator()
        tests = gen.generate(profile)

        if not tests:
            return f"No alias tests generated for `{mnemonic}`. This instruction is not a known alias."

        lines: list[str] = [f"# Alias Tests for `{mnemonic}`", ""]
        for t in tests:
            lines.append(f"## {t.test_name}")
            lines.append(f"- **Alias:** `{t.alias_mnemonic}` → `{t.canonical_mnemonic}`")
            lines.append(f"- **Alias form:** `{t.alias_instruction}`")
            lines.append(f"- **Canonical form:** `{t.canonical_instruction}`")
            if t.input_state:
                inputs = ", ".join(f"{k}={v}" for k, v in t.input_state.items())
                lines.append(f"- **Inputs:** {inputs}")
            if t.expected_state:
                exp = ", ".join(f"{k}={v}" for k, v in t.expected_state.items())
                lines.append(f"- **Expected:** {exp}")
            lines.append(f"- **Rationale:** {t.behavior_equivalence}")
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        logger.error("generate_alias_tests.error", error=str(e)[:200])
        return json.dumps({"error": str(e)[:300]}, ensure_ascii=False)


# ── generate_invalid_operand_tests ───────────────────────────────

@register_tool(
    "generate_invalid_operand_tests",
    "Generate tests for invalid/illegal operand combinations. "
    "Based on CONSTRAINED_UNPREDICTABLE and encoding constraints. "
    "Use when verifying assembler error handling and constraint checking.",
)
def generate_invalid_operand_tests(mnemonic: str) -> str:
    """Generate invalid operand test cases.

    Args:
        mnemonic: ARM instruction mnemonic.

    Returns:
        Invalid operand test cases with constraint references.
    """
    try:
        sqlite = get_sqlite()
        analyzer = InstructionAnalyzer(sqlite)
        profile = analyzer.extract_profile(mnemonic=mnemonic)
        if profile is None:
            return json.dumps({"error": f"Instruction '{mnemonic}' not found"}, ensure_ascii=False)

        from arm_isa_agent.generation.generators import InvalidOperandGenerator

        gen = InvalidOperandGenerator()
        tests = gen.generate(profile)

        if not tests:
            return f"No invalid operand tests generated for `{mnemonic}`."

        lines: list[str] = [
            f"# Invalid Operand Tests for `{mnemonic}`",
            "",
            "| # | Instruction | Invalid Aspect | Expected | Safe? |",
            "|---|-------------|----------------|----------|-------|",
        ]
        for i, t in enumerate(tests, 1):
            safe = "yes" if t.is_safe_to_test else "NO"
            lines.append(
                f"| {i} | `{t.instruction}` | {t.invalid_aspect} | "
                f"{t.expected_outcome} | {safe} |"
            )
        lines.append("")

        for t in tests:
            lines.append(f"## {t.test_name}")
            lines.append(f"- **Instruction:** `{t.instruction}`")
            lines.append(f"- **Type:** {t.invalid_aspect}")
            lines.append(f"- **Constraint:** {t.constraint_source}")
            if t.constraint_condition:
                lines.append(f"- **Condition:** `{t.constraint_condition}`")
            lines.append(f"- **Expected Outcome:** {t.expected_outcome}")
            lines.append(f"- **Safe to Execute:** {'Yes' if t.is_safe_to_test else '**No (DO NOT EXECUTE)**'}")
            lines.append(f"- **Rationale:** {t.rationale}")
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        logger.error("generate_invalid_operand_tests.error", error=str(e)[:200])
        return json.dumps({"error": str(e)[:300]}, ensure_ascii=False)


# ── generate_feature_enable_tests ────────────────────────────────

@register_tool(
    "generate_feature_enable_tests",
    "Generate feature dependency tests for ARM instructions. "
    "Verifies instructions are only available when the required architecture feature is enabled. "
    "Use when the instruction has FEAT_* dependencies.",
)
def generate_feature_enable_tests(mnemonic: str) -> str:
    """Generate feature dependency tests.

    Args:
        mnemonic: ARM instruction mnemonic.

    Returns:
        Feature enable test cases with positive and negative tests.
    """
    try:
        sqlite = get_sqlite()
        analyzer = InstructionAnalyzer(sqlite)
        profile = analyzer.extract_profile(mnemonic=mnemonic)
        if profile is None:
            return json.dumps({"error": f"Instruction '{mnemonic}' not found"}, ensure_ascii=False)

        from arm_isa_agent.generation.generators import FeatureEnableGenerator

        gen = FeatureEnableGenerator()
        tests = gen.generate(profile)

        if not tests:
            return f"No feature enable tests generated for `{mnemonic}`. This instruction has no feature dependencies."

        lines: list[str] = [
            f"# Feature Enable Tests for `{mnemonic}`",
            "",
            "| # | Feature | Architecture | Enable Flag | Error |",
            "|---|---------|--------------|-------------|-------|",
        ]
        for i, t in enumerate(tests, 1):
            lines.append(
                f"| {i} | {t.feature_name} | {t.architecture_version} | "
                f"`{t.enable_flag}` | {t.expected_error[:40]}... |"
            )
        lines.append("")

        for t in tests:
            lines.append(f"## {t.test_name}")
            lines.append(f"- **Feature:** {t.feature_name} ({t.feature_description})")
            lines.append(f"- **Architecture:** {t.architecture_version}")
            lines.append(f"- **Enable Flag:** `{t.enable_flag}`")
            lines.append(f"- **Instruction:** `{t.instruction}`")
            lines.append("")
            lines.append("### Assembly")
            for al in t.assembly_lines:
                lines.append(f"    {al}")
            lines.append("")
            if t.check_lines:
                lines.append("### CHECK (positive)")
                for cl in t.check_lines:
                    lines.append(f"    {cl}")
                lines.append("")
            if t.error_check_lines:
                lines.append("### CHECK (negative - without feature)")
                for ec in t.error_check_lines:
                    lines.append(f"    {ec}")
                lines.append("")

        return "\n".join(lines)

    except Exception as e:
        logger.error("generate_feature_enable_tests.error", error=str(e)[:200])
        return json.dumps({"error": str(e)[:300]}, ensure_ascii=False)
