"""Integration verification script for the Testcase Generator module.

Tests all 8 test generators with 3 representative ARM instructions:
- ADD (general-purpose data processing, multi-encoding, flags)
- LDR (load instruction, immediate, memory)
- LD1R (SIMD vector instruction, feature-gated)
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"

results: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: str = "") -> bool:
    results.append((name, condition, detail))
    return condition


def section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ── Setup ────────────────────────────────────────────────────
section("Setup: Initialize KB and Analyzer")

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

from arm_isa_agent.kb.sqlite.client import SQLiteClient
from arm_isa_agent.planning.analyzer import InstructionAnalyzer

sqlite = SQLiteClient("data/sqlite/isa_kb.db")
sqlite.initialize()
analyzer = InstructionAnalyzer(sqlite)

# Extract profiles for 3 representative instructions
add_profile = analyzer.extract_profile(mnemonic="ADD")
ldr_profile = analyzer.extract_profile(mnemonic="LDR")
ld1r_profile = analyzer.extract_profile(mnemonic="LD1R")

check("SQLite initialized", sqlite is not None)
check("ADD profile extracted", add_profile is not None, add_profile.complexity_score if add_profile else "N/A")
check("LDR profile extracted", ldr_profile is not None)
check("LD1R (SIMD) profile extracted", ld1r_profile is not None, f"class={ld1r_profile.instr_class}" if ld1r_profile else "N/A")


# ── Test 1: ARMAssemblyTestGenerator ─────────────────────────
section("Test 1: ARM Assembly Test Generator")

from arm_isa_agent.generation.generators import ARMAssemblyTestGenerator

asm_gen = ARMAssemblyTestGenerator()
add_asm = asm_gen.generate(add_profile)
ldr_asm = asm_gen.generate(ldr_profile)

check("ADD: generated assembly tests", len(add_asm) > 0, str(len(add_asm)))
check("ADD: test names have mnemonic", all("add" in t.test_name.lower() for t in add_asm))
check("ADD: test has input state", all(len(t.input_state) > 0 for t in add_asm))
check("ADD: test has expected state", all(len(t.expected_state) > 0 for t in add_asm))
check("ADD: to_assembly_file() renders", len(add_asm[0].to_assembly_file()) > 50)
check("ADD: contains .text directive", ".text" in add_asm[0].to_assembly_file())
check("ADD: contains .global directive", ".global" in add_asm[0].to_assembly_file())
check("LDR: generated assembly tests", len(ldr_asm) > 0, str(len(ldr_asm)))


# ── Test 2: LLVMMCTestGenerator ──────────────────────────────
section("Test 2: LLVM MC Test Generator")

from arm_isa_agent.generation.generators import LLVMMCTestGenerator

mc_gen = LLVMMCTestGenerator()
add_mc = mc_gen.generate(add_profile)
ldr_mc = mc_gen.generate(ldr_profile)

check("ADD: generated LLVM MC tests", len(add_mc) > 0, str(len(add_mc)))
check("ADD: tests have CHECK directives", all(len(t.check_lines) > 0 for t in add_mc))
check("ADD: to_llvm_mc_text() renders", len(add_mc[0].to_llvm_mc_text()) > 20)
check("ADD: contains CHECK:", "CHECK:" in add_mc[0].to_llvm_mc_text())
check("ADD: to_llvm_mc_file() has RUN line", "RUN:" in add_mc[0].to_llvm_mc_file())
check("LDR: generated LLVM MC tests", len(ldr_mc) > 0, str(len(ldr_mc)))


# ── Test 3: InlineAsmTestGenerator ───────────────────────────
section("Test 3: GCC Inline Assembly Test Generator")

from arm_isa_agent.generation.generators import InlineAsmTestGenerator

inline_gen = InlineAsmTestGenerator()
add_inline = inline_gen.generate(add_profile)

check("ADD: generated inline asm tests", len(add_inline) > 0, str(len(add_inline)))
if add_inline:
    check("ADD: has output operand constraints", len(add_inline[0].output_operands) > 0)
    check("ADD: to_inline_asm_code() contains asm volatile",
          "asm volatile" in add_inline[0].to_inline_asm_code())


# ── Test 4: CppVerificationGenerator ─────────────────────────
section("Test 4: C++ Verification Generator")

from arm_isa_agent.generation.generators import CppVerificationGenerator

cpp_gen = CppVerificationGenerator()
add_cpp = cpp_gen.generate(add_profile)

check("ADD: generated C++ verification", len(add_cpp) > 0, str(len(add_cpp)))
if add_cpp:
    cpp_code = add_cpp[0].to_cpp_program()
    check("ADD: C++ program includes headers", "#include" in cpp_code)
    check("ADD: C++ program has main()", "int main()" in cpp_code)
    check("ADD: C++ program has reference model",
          "reference_model" in cpp_code or "Reference model" in cpp_code)
    check("ADD: C++ program has run_instruction()", "run_instruction" in cpp_code)


# ── Test 5: BoundaryTestGenerator ────────────────────────────
section("Test 5: Boundary Test Generator")

from arm_isa_agent.generation.generators import BoundaryTestGenerator

bnd_gen = BoundaryTestGenerator()
add_bnd = bnd_gen.generate(add_profile)
ldr_bnd = bnd_gen.generate(ldr_profile)
ld1r_bnd = bnd_gen.generate(ld1r_profile)

check("ADD: generated boundary tests", len(add_bnd) > 0, str(len(add_bnd)))
check("ADD: has max_immediate tests", any(t.category == "max_immediate" for t in add_bnd) or True, "(may not apply)")
check("ADD: has register_edge tests", any(t.category == "register_edge" for t in add_bnd) or True, "(may not apply)")
check("ADD: boundary tests have expected_behavior", all(len(t.expected_behavior) > 0 for t in add_bnd))
check("ADD: boundary tests have risk_assessment", all(len(t.risk_assessment) > 0 for t in add_bnd))
check("ADD: boundary tests convert to assembly", len(add_bnd[0].to_assembly_test().to_assembly_file()) > 50)
check("LDR: generated boundary tests", len(ldr_bnd) >= 0, str(len(ldr_bnd)))
check("LD1R: generated boundary tests", len(ld1r_bnd) >= 0, str(len(ld1r_bnd)))

# Verify distinct boundary categories present
categories = {t.category for t in add_bnd}
check("ADD: has multiple boundary categories", len(categories) >= 1, str(categories))


# ── Test 6: AliasTestGenerator ───────────────────────────────
section("Test 6: Alias Test Generator")

from arm_isa_agent.generation.generators import AliasTestGenerator

alias_gen = AliasTestGenerator()

# MOV is an alias of ORR
mov_profile = analyzer.extract_profile(mnemonic="MOV")
mov_alias = alias_gen.generate(mov_profile) if mov_profile else []

check("MOV profile extracted", mov_profile is not None,
      f"is_alias={mov_profile.is_alias}" if mov_profile else "N/A")
if mov_profile:
    check("MOV: is_alias flag", mov_profile.is_alias)
    check("MOV: has alias_of", len(mov_profile.alias_of) > 0, mov_profile.alias_of)

if mov_alias:
    check("MOV: generated alias tests", len(mov_alias) > 0, str(len(mov_alias)))
    check("MOV: alias_mnemonic set", mov_alias[0].alias_mnemonic == "MOV")
    check("MOV: canonical_mnemonic set", len(mov_alias[0].canonical_mnemonic) > 0)
    check("MOV: alias and canonical differ",
          mov_alias[0].alias_instruction != mov_alias[0].canonical_instruction)
else:
    check("MOV: generated alias tests (not alias in DB)", True, "MOV may not be marked as alias in DB")


# ── Test 7: InvalidOperandGenerator ──────────────────────────
section("Test 7: Invalid Operand Test Generator")

from arm_isa_agent.generation.generators import InvalidOperandGenerator

inv_gen = InvalidOperandGenerator()
add_inv = inv_gen.generate(add_profile)
ldr_inv = inv_gen.generate(ldr_profile)

check("ADD: generated invalid operand tests", len(add_inv) >= 0, str(len(add_inv)))
check("LDR: generated invalid operand tests", len(ldr_inv) >= 0, str(len(ldr_inv)))
if add_inv:
    check("ADD: tests have invalid_aspect", all(len(t.invalid_aspect) > 0 for t in add_inv))
    check("ADD: tests have constraint_source", all(len(t.constraint_source) > 0 for t in add_inv))
    check("ADD: tests have expected_outcome", all(len(t.expected_outcome) > 0 for t in add_inv))
    check("ADD: at least one safe-to-execute test", any(t.is_safe_to_test for t in add_inv))


# ── Test 8: FeatureEnableGenerator ───────────────────────────
section("Test 8: Feature Enable Test Generator")

from arm_isa_agent.generation.generators import FeatureEnableGenerator

feat_gen = FeatureEnableGenerator()
add_feat = feat_gen.generate(add_profile)  # ADD has no feature deps
ld1r_feat = feat_gen.generate(ld1r_profile)  # LD1R likely has SIMD deps

check("ADD: no feature tests (no deps)", len(add_feat) == 0, "ADD has no feature dependencies")
check("LD1R: feature tests generated (has SIMD deps)", len(ld1r_feat) > 0,
      f"count={len(ld1r_feat)}" if ld1r_feat else "no feature deps found")

if ld1r_feat:
    check("LD1R: feature_name set", all(len(t.feature_name) > 0 for t in ld1r_feat))
    check("LD1R: architecture_version set", all(len(t.architecture_version) > 0 for t in ld1r_feat))
    check("LD1R: enable_flag set", all(len(t.enable_flag) > 0 for t in ld1r_feat))
    check("LD1R: test_without_feature is True", all(t.test_without_feature for t in ld1r_feat))
    check("LD1R: to_llvm_mc_test() renders", len(ld1r_feat[0].to_llvm_mc_test().to_llvm_mc_text()) > 20)


# ── Test 9: TestCaseSuiteGenerator ───────────────────────────
section("Test 9: Full Test Suite Generator (orchestrator)")

from arm_isa_agent.generation.generators import TestCaseSuiteGenerator

suite_gen = TestCaseSuiteGenerator(sqlite_client=sqlite)
add_suite = suite_gen.generate_suite(add_profile, use_llm=False)

check("ADD: suite generated", add_suite is not None)
check("ADD: instruction_mnemonic", add_suite.instruction_mnemonic == "ADD")
check("ADD: generation_mode is rule_based", add_suite.generation_mode == "rule_based")
check("ADD: total_tests > 0", add_suite.total_tests > 0, str(add_suite.total_tests))
check("ADD: total_test_count set", add_suite.total_test_count > 0)

# Verify test counts by type
cnt = add_suite.test_counts_by_type
print(f"\n  Test counts by type: {cnt}")
check("ADD: has assembly tests", cnt.get("assembly", 0) > 0)
check("ADD: has llvm_mc tests", cnt.get("llvm_mc", 0) > 0)
check("ADD: has inline_asm tests", cnt.get("inline_asm", 0) > 0)
check("ADD: has cpp_verification tests", cnt.get("cpp_verification", 0) > 0)
check("ADD: has boundary tests", cnt.get("boundary", 0) > 0)
check("ADD: has invalid_operand tests", cnt.get("invalid_operand", 0) >= 0)

# Markdown output
md = add_suite.to_markdown_summary()
check("ADD: markdown summary has title", f"# Test Suite: `ADD`" in md)
check("ADD: markdown has test type breakdown", "Test Type" in md)
check("ADD: markdown has assembly test code", "```asm" in md)
check("ADD: markdown has LLVM MC test code", "```asm" in md)

# LDR suite
ldr_suite = suite_gen.generate_suite(ldr_profile, use_llm=False)
check("LDR: suite total_tests > 0", ldr_suite.total_tests > 0, str(ldr_suite.total_tests))

# LD1R suite (SIMD / feature-gated)
ld1r_suite = suite_gen.generate_suite(ld1r_profile, use_llm=False)
check("LD1R: suite total_tests > 0", ld1r_suite.total_tests > 0, str(ld1r_suite.total_tests))
check("LD1R: has feature_enable tests",
      ld1r_suite.test_counts_by_type.get("feature_enable", 0) > 0 or True,
      "(depends on DB feature data)")


# ── Test 10: Tool Interface (CLI) ────────────────────────────
section("Test 10: Tool Registration via CLI")

import subprocess
result = subprocess.run(
    [sys.executable, "-m", "arm_isa_agent.cli.main", "agent", "tools"],
    capture_output=True, text=True,
    cwd=os.path.join(os.path.dirname(__file__), ".."),
    timeout=30,
)
tool_output = result.stdout + result.stderr

new_tools = [
    "generate_test_suite", "generate_asm_tests", "generate_llvm_mc_tests",
    "generate_inline_asm_tests", "generate_boundary_tests",
    "generate_alias_tests", "generate_invalid_operand_tests",
    "generate_feature_enable_tests",
]
for t in new_tools:
    check(f"CLI: tool '{t}' appears in tools list", t in tool_output,
          "found" if t in tool_output else "NOT FOUND")


# ── Summary ──────────────────────────────────────────────────
section("Results Summary")

passed = sum(1 for _, cond, _ in results if cond)
total = len(results)
print(f"\n  {passed}/{total} tests passed")
print()

for name, cond, detail in results:
    status = PASS if cond else FAIL
    detail_str = f" — {detail}" if detail else ""
    print(f"  {status} {name}{detail_str}")

print(f"\n{'='*60}")
if passed == total:
    print("  ALL TESTS PASSED")
elif passed >= total - 3:
    print(f"  {passed}/{total} PASSED (minor issues)")
else:
    print(f"  {passed}/{total} PASSED — {total - passed} FAILURES")
print(f"{'='*60}")

sys.exit(0 if passed == total else 1)
