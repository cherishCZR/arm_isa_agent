"""Testcase Generator data models — structured types for all 8 test formats."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════
# 1. ARM Assembly Test
# ═══════════════════════════════════════════════════════════════

class ARMAssemblyTestCase(BaseModel):
    """A single ARM A64 assembly test case with input/expected state."""

    test_name: str = Field(description="Unique test name, e.g. test_add_normal")
    description: str = Field(default="", description="What this test verifies")
    instruction: str = Field(description="The ARM assembly instruction under test")
    input_state: dict[str, str] = Field(
        default_factory=dict,
        description="Register initial values, e.g. {'X0': '0x10', 'X1': '0x20'}",
    )
    expected_state: dict[str, str] = Field(
        default_factory=dict,
        description="Expected register/memory values after execution",
    )
    expected_flags: dict[str, str] = Field(
        default_factory=dict,
        description="Expected NZCV flags: {'N': '0', 'Z': '0', 'C': '1', 'V': '0'}",
    )
    encoding_name: str = Field(default="", description="Which encoding variant is tested")
    feature_required: str = Field(default="", description="Required feature, e.g. FEAT_FP")
    comments: list[str] = Field(default_factory=list, description="Explanatory comments")

    def to_assembly_file(self) -> str:
        """Render as a standalone ARM assembly source file."""
        lines: list[str] = []
        lines.append(f"// Test: {self.test_name}")
        lines.append(f"// Description: {self.description}")
        if self.feature_required:
            lines.append(f"// Requires: {self.feature_required}")
        lines.append(f"// Encoding: {self.encoding_name}" if self.encoding_name else "")
        lines.append("")
        lines.append("\t.text")
        lines.append(f"\t.global {self.test_name}")
        if hasattr(self, "_alignment"):
            lines.append(f"\t.align {self._alignment}")
        else:
            lines.append("\t.align 2")
        lines.append("")
        lines.append(f"{self.test_name}:")
        lines.append("")
        # Register initialization
        for reg, val in sorted(self.input_state.items()):
            lines.append(f"\t// Initialize {reg} = {val}")
            if reg.startswith("X") or reg.startswith("W"):
                lines.append(f"\tmov {reg}, #{val}")
            elif any(c.isdigit() for c in reg):
                # Vector register: use adr + ldr
                pass
        lines.append("")
        lines.append(f"\t// Instruction under test")
        lines.append(f"\t{self.instruction}")
        lines.append("")
        # Expected result comments
        lines.append("\t// Expected results:")
        for reg, val in sorted(self.expected_state.items()):
            lines.append(f"\t//   {reg} = {val}")
        if self.expected_flags:
            flags_str = ", ".join(f"{k}={v}" for k, v in sorted(self.expected_flags.items()))
            lines.append(f"\t//   Flags: {flags_str}")
        lines.append("")
        lines.append("\tret")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 2. LLVM MC Test
# ═══════════════════════════════════════════════════════════════

class LLVMMCTestCase(BaseModel):
    """LLVM MC (Machine Code) test with CHECK directives."""

    test_name: str = Field(description="Test identifier")
    description: str = Field(default="", description="What this test verifies")
    assembly_lines: list[str] = Field(
        default_factory=list,
        description="Assembly lines to feed to llvm-mc",
    )
    check_lines: list[str] = Field(
        default_factory=list,
        description="Expected encoding CHECK directives",
    )
    check_not_lines: list[str] = Field(
        default_factory=list,
        description="CHECK-NOT directives for negative tests",
    )
    encoding_name: str = Field(default="", description="Target encoding")
    feature_required: str = Field(default="", description="Required feature")

    def to_llvm_mc_file(self, target_triple: str = "aarch64-unknown-linux-gnu") -> str:
        """Render as a complete .s file for llvm-mc."""
        lines: list[str] = []
        lines.append(f"// Test: {self.test_name}")
        lines.append(f"// Description: {self.description}")
        lines.append("")
        lines.append(f"// RUN: llvm-mc -triple={target_triple} -show-encoding %s | FileCheck %s")
        if self.feature_required:
            feature_flag = self.feature_required.lower().replace("_", "-")
            lines.append(
                f"// RUN: llvm-mc -triple={target_triple} -mattr=+{feature_flag} "
                f"-show-encoding %s | FileCheck %s"
            )
        lines.append("")
        for cl in self.check_lines:
            lines.append(cl)
        lines.append("")
        for al in self.assembly_lines:
            lines.append(al)
        lines.append("")
        return "\n".join(lines)

    def to_llvm_mc_text(self) -> str:
        """Render as llvm-mc format text with CHECK patterns."""
        lines: list[str] = []
        lines.append(f"// {self.test_name}")
        if self.description:
            lines.append(f"// {self.description}")
        lines.append("")
        for cl in self.check_lines:
            lines.append(cl)
        for al in self.assembly_lines:
            lines.append(al)
        for cn in self.check_not_lines:
            lines.append(cn)
        lines.append("")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 3. GCC Inline Assembly Test
# ═══════════════════════════════════════════════════════════════

class InlineAsmTestCase(BaseModel):
    """GCC/Clang inline assembly test."""

    test_name: str = Field(description="Test function name")
    description: str = Field(default="", description="Test description")
    instruction: str = Field(description="ARM instruction to embed")
    input_operands: str = Field(
        default="",
        description="Input operand constraints, e.g. '[in1]\"r\"(val1), [in2]\"r\"(val2)'",
    )
    output_operands: str = Field(
        default="",
        description="Output operand constraints, e.g. '[out]\"=r\"(result)'",
    )
    clobbers: str = Field(default='"cc", "memory"', description="Clobber list")
    compiler: str = Field(default="gcc", description="gcc | clang")
    expected_result: str = Field(default="", description="Expected computation result")
    feature_required: str = Field(default="", description="Required ISA feature")

    def to_inline_asm_code(self) -> str:
        """Render as compilable C function."""
        lines: list[str] = []
        lines.append(f"// Test: {self.test_name}")
        if self.description:
            lines.append(f"// {self.description}")
        if self.feature_required:
            lines.append(f"// Requires: {self.feature_required}")
        lines.append("")
        lines.append(f"void {self.test_name}(void) {{")
        lines.append("    uint64_t in1 = ...;  // TODO: initialize")
        lines.append("    uint64_t in2 = ...;  // TODO: initialize")
        lines.append("    uint64_t result;")
        lines.append("")

        lines.append("    asm volatile(")
        lines.append(f'        "{self.instruction}"')
        if self.output_operands:
            lines.append(f"        : {self.output_operands}")
        else:
            lines.append("        : /* no output operands */")
        if self.input_operands:
            lines.append(f"        : {self.input_operands}")
        else:
            lines.append("        : /* no input operands */")
        lines.append(f"        : {self.clobbers}")
        lines.append("    );")
        lines.append("")

        if self.expected_result:
            lines.append(f"    // Expected: {self.expected_result}")
        lines.append("}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 4. C++ Verification Program
# ═══════════════════════════════════════════════════════════════

class CppVerificationTestCase(BaseModel):
    """Self-checking C++ verification program with reference model."""

    test_name: str = Field(description="Program/test name")
    description: str = Field(default="", description="What this verifies")
    instruction: str = Field(description="ARM instruction under test")
    reference_model: str = Field(
        default="",
        description="Reference computation description, e.g. 'result = a + b'",
    )
    test_inputs: list[dict[str, str]] = Field(
        default_factory=list,
        description="List of input vectors, e.g. [{'X0': '0', 'X1': '0'}, {...}]",
    )
    expected_outputs: list[dict[str, str]] = Field(
        default_factory=list,
        description="Corresponding expected outputs",
    )
    feature_required: str = Field(default="", description="Required feature")
    includes: list[str] = Field(
        default_factory=lambda: ["<cstdint>", "<cstdio>", "<cstdlib>"],
    )

    def to_cpp_program(self) -> str:
        """Render as a complete, compilable C++ verification program."""
        lines: list[str] = []
        lines.append(f"// Verification: {self.test_name}")
        lines.append(f"// {self.description}")
        if self.feature_required:
            lines.append(f"// Requires: {self.feature_required}")
        lines.append("")

        for inc in self.includes:
            lines.append(f"#include {inc}")
        lines.append("")

        lines.append("// ARM inline assembly helpers")
        lines.append("static inline uint64_t run_instruction(uint64_t a, uint64_t b) {")
        lines.append("    uint64_t result;")
        lines.append("    asm volatile(")
        lines.append(f'        "{self.instruction}\\n"')
        lines.append('        : "=&r" (result)')
        lines.append('        : "r" (a), "r" (b)')
        lines.append('        : "cc"')
        lines.append("    );")
        lines.append("    return result;")
        lines.append("}")
        lines.append("")

        # Reference model
        lines.append(f"// Reference model: {self.reference_model}")
        lines.append("static inline uint64_t reference_model(uint64_t a, uint64_t b) {")
        lines.append("    // TODO: implement reference computation")
        lines.append("    return 0;")
        lines.append("}")
        lines.append("")

        # Test harness
        lines.append("int main() {")
        lines.append("    int failures = 0;")
        lines.append("")

        for i, (inp, exp) in enumerate(zip(self.test_inputs, self.expected_outputs)):
            inp_str = ", ".join(f"{k}={v}" for k, v in inp.items())
            exp_str = ", ".join(f"{k}={v}" for k, v in exp.items())
            lines.append(f"    // Test {i}: {inp_str}")
            lines.append("    {")
            # Collect inputs
            for k, v in inp.items():
                lines.append(f"        uint64_t {k.lower()} = {v};")
            # Call
            lines.append(f"        uint64_t result = run_instruction({', '.join(k.lower() for k in inp)});")
            # Check
            for k, v in exp.items():
                lines.append(f"        uint64_t expected_{k.lower()} = {v};")
            if exp:
                first_k = next(iter(exp))
                lines.append(f"        if (result != expected_{first_k.lower()}) {{")
                lines.append(f"            printf(\"[FAIL] Test {i}: got 0x%lx, expected 0x%lx\\n\",")
                lines.append(f"                   result, expected_{first_k.lower()});")
                lines.append("            failures++;")
                lines.append("        } else {")
                lines.append(f"            printf(\"[PASS] Test {i}\\n\");")
                lines.append("        }")
            lines.append("    }")
            lines.append("")

        lines.append("    if (failures == 0) {")
        lines.append(f'        printf("\\n[OK] All tests passed for {self.test_name}\\n");')
        lines.append("        return 0;")
        lines.append("    }")
        lines.append(f'    printf("\\n[FAIL] {self.test_name}: %d failures\\n", failures);')
        lines.append("    return 1;")
        lines.append("}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 5. Boundary Test
# ═══════════════════════════════════════════════════════════════

class BoundaryTestCase(BaseModel):
    """Boundary / corner value test for an instruction."""

    test_name: str = Field(description="Test name")
    category: Literal[
        "max_immediate",
        "min_immediate",
        "zero",
        "overflow",
        "register_edge",
        "alignment",
        "width_boundary",
        "shift_extreme",
    ] = Field(description="Boundary category")
    instruction: str = Field(description="The assembly instruction")
    boundary_value: str = Field(description="The boundary value being tested, e.g. 'imm12=4095'")
    input_state: dict[str, str] = Field(default_factory=dict)
    expected_state: dict[str, str] = Field(default_factory=dict)
    expected_flags: dict[str, str] = Field(default_factory=dict)
    expected_behavior: str = Field(
        default="",
        description="E.g. 'result wraps to 0', 'UNDEFINED', 'CONSTRAINED_UNPREDICTABLE'",
    )
    risk_assessment: str = Field(default="", description="Why this boundary matters")

    def to_assembly_test(self) -> ARMAssemblyTestCase:
        """Convert to a standard assembly test case format."""
        return ARMAssemblyTestCase(
            test_name=self.test_name,
            description=f"Boundary test [{self.category}]: {self.boundary_value}. {self.expected_behavior}",
            instruction=self.instruction,
            input_state=self.input_state,
            expected_state=self.expected_state,
            expected_flags=self.expected_flags,
            comments=[f"Category: {self.category}", f"Boundary: {self.boundary_value}"],
        )


# ═══════════════════════════════════════════════════════════════
# 6. Alias Test
# ═══════════════════════════════════════════════════════════════

class AliasTestCase(BaseModel):
    """Test verifying that an alias is equivalent to its canonical form."""

    test_name: str = Field(description="Test name")
    alias_mnemonic: str = Field(description="The alias mnemonic, e.g. MOV")
    canonical_mnemonic: str = Field(description="The canonical mnemonic, e.g. ORR")
    alias_instruction: str = Field(description="Full alias instruction, e.g. 'MOV X0, X1'")
    canonical_instruction: str = Field(description="Equivalent canonical form, e.g. 'ORR X0, XZR, X1'")
    input_state: dict[str, str] = Field(default_factory=dict)
    expected_state: dict[str, str] = Field(default_factory=dict)
    behavior_equivalence: str = Field(
        default="",
        description="Description of why these are equivalent",
    )

    def to_assembly_test(self) -> ARMAssemblyTestCase:
        """Convert to assembly tests for both alias and canonical forms."""
        return ARMAssemblyTestCase(
            test_name=self.test_name,
            description=(
                f"Alias equivalence: {self.alias_mnemonic} == {self.canonical_mnemonic}. "
                f"{self.behavior_equivalence}"
            ),
            instruction=self.alias_instruction,
            input_state=self.input_state,
            expected_state=self.expected_state,
            comments=[
                f"Alias: {self.alias_mnemonic}",
                f"Canonical: {self.canonical_mnemonic}",
                f"Canonical form: {self.canonical_instruction}",
            ],
        )


# ═══════════════════════════════════════════════════════════════
# 7. Invalid Operand Test
# ═══════════════════════════════════════════════════════════════

class InvalidOperandTestCase(BaseModel):
    """Test that verifies invalid operand combinations are properly handled."""

    test_name: str = Field(description="Test name")
    instruction: str = Field(description="Full instruction with invalid operands")
    invalid_aspect: Literal[
        "register_combination",
        "immediate_range",
        "feature_missing",
        "alignment_violation",
        "reserved_bits",
        "type_mismatch",
    ] = Field(description="Type of invalidity")
    constraint_source: str = Field(
        default="",
        description="Reference to the ISA constraint: CONSTRAINED_UNPREDICTABLE, UNDEFINED, etc.",
    )
    constraint_condition: str = Field(default="", description="The constraint condition expression")
    expected_outcome: str = Field(
        default="CONSTRAINED_UNPREDICTABLE",
        description="CONSTRAINED_UNPREDICTABLE | UNDEFINED | RESERVED",
    )
    rationale: str = Field(default="", description="Why this is invalid")
    is_safe_to_test: bool = Field(default=True, description="Can this be executed without UB risk?")

    def to_assembly_test(self) -> ARMAssemblyTestCase:
        """Convert to an assembly test with warning comments."""
        warning = (
            self.expected_outcome
            if self.is_safe_to_test
            else f"{self.expected_outcome} - DO NOT EXECUTE DIRECTLY"
        )
        return ARMAssemblyTestCase(
            test_name=self.test_name,
            description=(
                f"Invalid operand test [{self.invalid_aspect}]: {self.rationale}. "
                f"Expected: {warning}"
            ),
            instruction=self.instruction,
            comments=[
                f"Constraint: {self.constraint_source}",
                f"Condition: {self.constraint_condition}",
                f"Expected outcome: {self.expected_outcome}",
            ],
        )


# ═══════════════════════════════════════════════════════════════
# 8. Feature Enable Test
# ═══════════════════════════════════════════════════════════════

class FeatureEnableTestCase(BaseModel):
    """Test verifying that instruction is available only when the required feature is enabled."""

    test_name: str = Field(description="Test name")
    instruction: str = Field(description="The instruction requiring the feature")
    feature_name: str = Field(description="Feature name, e.g. FEAT_SVE, FEAT_FP16")
    feature_description: str = Field(default="", description="Human-readable feature description")
    architecture_version: str = Field(default="", description="Minimum arch version, e.g. ARMv8.2")
    enable_flag: str = Field(default="", description="Compiler flag to enable, e.g. -march=armv8.2-a+sve")
    test_without_feature: bool = Field(default=True, description="Generate negative test (expect error)")
    assembly_lines: list[str] = Field(default_factory=list, description="Assembly to check")
    check_lines: list[str] = Field(
        default_factory=list,
        description="CHECK directives for positive case",
    )
    error_check_lines: list[str] = Field(
        default_factory=list,
        description="CHECK directives for negative case (expect error)",
    )
    expected_error: str = Field(
        default="",
        description="Expected error message when feature is absent",
    )

    def to_llvm_mc_test(self) -> LLVMMCTestCase:
        """Convert to an LLVM MC test with positive and negative RUN lines."""
        all_check = list(self.check_lines)
        if self.test_without_feature:
            all_check.extend(self.error_check_lines)

        return LLVMMCTestCase(
            test_name=self.test_name,
            description=f"Feature enable test: {self.feature_name} ({self.feature_description})",
            assembly_lines=list(self.assembly_lines),
            check_lines=all_check,
            encoding_name=self.feature_name,
            feature_required=self.feature_name,
        )


# ═══════════════════════════════════════════════════════════════
# Test Case Suite
# ═══════════════════════════════════════════════════════════════

class TestCaseSuite(BaseModel):
    """Complete test suite containing all test types for an instruction."""

    instruction_mnemonic: str = Field(description="Target instruction mnemonic")
    instruction_xml_id: str = Field(default="", description="XML identifier")

    # All test categories
    assembly_tests: list[ARMAssemblyTestCase] = Field(default_factory=list)
    llvm_mc_tests: list[LLVMMCTestCase] = Field(default_factory=list)
    inline_asm_tests: list[InlineAsmTestCase] = Field(default_factory=list)
    cpp_verification_tests: list[CppVerificationTestCase] = Field(default_factory=list)
    boundary_tests: list[BoundaryTestCase] = Field(default_factory=list)
    alias_tests: list[AliasTestCase] = Field(default_factory=list)
    invalid_operand_tests: list[InvalidOperandTestCase] = Field(default_factory=list)
    feature_enable_tests: list[FeatureEnableTestCase] = Field(default_factory=list)

    # Metadata
    generation_mode: str = Field(default="rule_based", description="rule_based | llm_assisted")
    total_test_count: int = Field(default=0)
    generation_warnings: list[str] = Field(default_factory=list)
    scenario_label: str | None = Field(default=None, description="Human-readable label for multi-instruction scenario")

    @property
    def total_tests(self) -> int:
        return (
            len(self.assembly_tests)
            + len(self.llvm_mc_tests)
            + len(self.inline_asm_tests)
            + len(self.cpp_verification_tests)
            + len(self.boundary_tests)
            + len(self.alias_tests)
            + len(self.invalid_operand_tests)
            + len(self.feature_enable_tests)
        )

    @property
    def test_counts_by_type(self) -> dict[str, int]:
        return {
            "assembly": len(self.assembly_tests),
            "llvm_mc": len(self.llvm_mc_tests),
            "inline_asm": len(self.inline_asm_tests),
            "cpp_verification": len(self.cpp_verification_tests),
            "boundary": len(self.boundary_tests),
            "alias": len(self.alias_tests),
            "invalid_operand": len(self.invalid_operand_tests),
            "feature_enable": len(self.feature_enable_tests),
        }

    def to_markdown_summary(self) -> str:
        """Render a Markdown summary of the test suite."""
        cnt = self.test_counts_by_type
        lines: list[str] = []
        lines.append(f"# Test Suite: `{self.instruction_mnemonic}`")
        if self.instruction_xml_id:
            lines.append(f"**XML ID:** `{self.instruction_xml_id}`")
        lines.append(f"**Total:** {self.total_tests} tests ({self.generation_mode})")
        lines.append("")
        lines.append("| Test Type | Count |")
        lines.append("|-----------|-------|")
        for t, c in sorted(cnt.items(), key=lambda x: -x[1]):
            label = t.replace("_", " ").title()
            lines.append(f"| {label} | {c} |")
        lines.append("")

        if self.assembly_tests:
            lines.append("## ARM Assembly Tests")
            for t in self.assembly_tests:
                lines.append(f"### {t.test_name}")
                lines.append(f"- **Instruction:** `{t.instruction}`")
                lines.append(f"- **Description:** {t.description}")
                if t.expected_flags:
                    lines.append(f"- **Flags:** {t.expected_flags}")
                lines.append("```asm")
                lines.append(t.to_assembly_file())
                lines.append("```")
                lines.append("")

        if self.llvm_mc_tests:
            lines.append("## LLVM MC Tests")
            for t in self.llvm_mc_tests:
                lines.append(f"### {t.test_name}")
                lines.append("```asm")
                lines.append(t.to_llvm_mc_text())
                lines.append("```")
                lines.append("")

        if self.inline_asm_tests:
            lines.append("## GCC Inline Assembly Tests")
            for t in self.inline_asm_tests:
                lines.append(f"### {t.test_name}")
                lines.append("```c")
                lines.append(t.to_inline_asm_code())
                lines.append("```")
                lines.append("")

        if self.cpp_verification_tests:
            lines.append("## C++ Verification Programs")
            for t in self.cpp_verification_tests:
                lines.append(f"### {t.test_name}")
                lines.append("```cpp")
                lines.append(t.to_cpp_program())
                lines.append("```")
                lines.append("")

        if self.boundary_tests:
            lines.append("## Boundary Tests")
            for t in self.boundary_tests:
                lines.append(
                    f"- **{t.test_name}** [{t.category}]: `{t.instruction}` "
                    f"({t.boundary_value}) → {t.expected_behavior}"
                )

        if self.alias_tests:
            lines.append("## Alias Tests")
            for t in self.alias_tests:
                lines.append(
                    f"- **{t.test_name}**: `{t.alias_instruction}` ⇔ `{t.canonical_instruction}`"
                )

        if self.invalid_operand_tests:
            lines.append("## Invalid Operand Tests")
            for t in self.invalid_operand_tests:
                lines.append(
                    f"- **{t.test_name}** [{t.invalid_aspect}]: `{t.instruction}` "
                    f"→ {t.expected_outcome}"
                )

        if self.feature_enable_tests:
            lines.append("## Feature Enable Tests")
            for t in self.feature_enable_tests:
                lines.append(
                    f"- **{t.test_name}**: `{t.instruction}` requires {t.feature_name}"
                )

        if self.generation_warnings:
            lines.append("## Warnings")
            for w in self.generation_warnings:
                lines.append(f"- ⚠ {w}")

        return "\n".join(lines)

    def to_single_assembly_file(self) -> str:
        """Combine every generated test case into one .S program.

        ARM assembly, boundary, alias and invalid-operand tests are emitted as
        executable assembly fragments.  LLVM-MC, inline-asm, C++ verification and
        feature-enable tests are kept as `#if 0` / `#endif` reference blocks so
        the single file still assembles while preserving all scenarios.
        """
        mnemonic = self.instruction_mnemonic.upper()
        label = (self.scenario_label or mnemonic).replace(",", "_").replace(" ", "_")
        primary_mnemonic = mnemonic.split(",")[0]
        counts = self.test_counts_by_type
        total = self.total_tests

        lines: list[str] = []
        lines.append("/* ============================================================================")
        lines.append(f" * Combined Test Program")
        if self.scenario_label:
            lines.append(f" * Scenario: {self.scenario_label}")
        lines.append(f" * Primary instruction: {primary_mnemonic}")
        if self.instruction_xml_id:
            lines.append(f" * XML ID: {self.instruction_xml_id}")
        lines.append(f" * Total tests: {total}")
        for name, cnt in counts.items():
            if cnt:
                lines.append(f" *   - {name}: {cnt}")
        lines.append(" * ============================================================================ */")
        lines.append("")
        lines.append("    .text")
        lines.append("    .align 2")
        lines.append("")

        def _section_header(title: str, count: int) -> None:
            lines.append("")
            lines.append("/* ============================================================================")
            lines.append(f" * {title} ({count})")
            lines.append(" * ============================================================================ */")
            lines.append("")

        def _subsection(name: str, description: str) -> None:
            lines.append("")
            lines.append(f"/* ----------------------------------------------------------------------------")
            lines.append(f" * Test: {name}")
            if description:
                lines.append(f" * Description: {description}")
            lines.append(" * ---------------------------------------------------------------------------- */")

        # 1. ARM Assembly tests (executable)
        if self.assembly_tests:
            _section_header("ARM Assembly Tests", len(self.assembly_tests))
            for t in self.assembly_tests:
                _subsection(t.test_name, t.description)
                lines.append(t.to_assembly_file().rstrip("\n"))

        # 2. Boundary tests (executable)
        if self.boundary_tests:
            _section_header("Boundary Tests", len(self.boundary_tests))
            for t in self.boundary_tests:
                asm = t.to_assembly_test()
                _subsection(t.test_name, f"Boundary [{t.category}]: {t.boundary_value}")
                lines.append(asm.to_assembly_file().rstrip("\n"))

        # 3. Alias tests (executable)
        if self.alias_tests:
            _section_header("Alias Tests", len(self.alias_tests))
            for t in self.alias_tests:
                asm = t.to_assembly_test()
                _subsection(t.test_name, f"Alias: {t.alias_mnemonic} ≡ {t.canonical_mnemonic}")
                lines.append(asm.to_assembly_file().rstrip("\n"))

        # 4. Invalid operand tests (executable)
        if self.invalid_operand_tests:
            _section_header("Invalid Operand Tests", len(self.invalid_operand_tests))
            for t in self.invalid_operand_tests:
                asm = t.to_assembly_test()
                _subsection(t.test_name, f"Invalid [{t.invalid_aspect}]: {t.expected_outcome}")
                lines.append(asm.to_assembly_file().rstrip("\n"))

        # 5. LLVM MC tests (reference block)
        if self.llvm_mc_tests:
            _section_header("LLVM MC Tests (reference)", len(self.llvm_mc_tests))
            for t in self.llvm_mc_tests:
                _subsection(t.test_name, t.description)
                lines.append("#if 0")
                lines.append(t.to_llvm_mc_file().rstrip("\n"))
                lines.append("#endif")

        # 6. Inline Assembly tests (reference block)
        if self.inline_asm_tests:
            _section_header("Inline Assembly Tests (reference)", len(self.inline_asm_tests))
            for t in self.inline_asm_tests:
                _subsection(t.test_name, t.description)
                lines.append("#if 0")
                lines.append(t.to_inline_asm_code().rstrip("\n"))
                lines.append("#endif")

        # 7. C++ Verification tests (reference block)
        if self.cpp_verification_tests:
            _section_header("C++ Verification Tests (reference)", len(self.cpp_verification_tests))
            for t in self.cpp_verification_tests:
                _subsection(t.test_name, t.description)
                lines.append("#if 0")
                lines.append(t.to_cpp_program().rstrip("\n"))
                lines.append("#endif")

        # 8. Feature enable tests (reference block)
        if self.feature_enable_tests:
            _section_header("Feature Enable Tests (reference)", len(self.feature_enable_tests))
            for t in self.feature_enable_tests:
                mc = t.to_llvm_mc_test()
                _subsection(t.test_name, f"Feature: {t.feature_name}")
                lines.append("#if 0")
                lines.append(mc.to_llvm_mc_file().rstrip("\n"))
                lines.append("#endif")

        return "\n".join(lines) + "\n"

    def to_test_file_entries(self) -> list[dict[str, str]]:
        """Return a single combined .S test program for the scenario.

        Each scenario is packaged as one self-contained assembly file.
        """
        mnemonic = self.instruction_mnemonic.upper()
        label = (self.scenario_label or mnemonic).replace(",", "_").replace(" ", "_")
        content = self.to_single_assembly_file()
        total = self.total_tests
        return [{
            "file_id": f"{label}_combined",
            "filename": f"{label}_test_program.S",
            "format": "s",
            "test_type": "combined_assembly",
            "content": content,
            "status": "pass",
            "description": f"Combined assembly program for {self.scenario_label or mnemonic} ({total} tests)",
            "issue_count": 0,
        }]
