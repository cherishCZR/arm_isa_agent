"""Testcase Generator prompt templates — LLM-assisted test generation prompts."""

from __future__ import annotations

from arm_isa_agent.planning.models import InstructionProfile


# ═══════════════════════════════════════════════════════════════
# Profile context builder
# ═══════════════════════════════════════════════════════════════

def format_profile_context(profile: InstructionProfile) -> str:
    """Build a rich text summary of the instruction profile for LLM consumption."""
    parts: list[str] = []

    parts.append(f"## Instruction: {profile.mnemonic}")
    parts.append(f"- **XML ID:** `{profile.xml_id}`")
    parts.append(f"- **Class:** {profile.instr_class}")
    if profile.brief:
        parts.append(f"- **Brief:** {profile.brief}")
    if profile.title:
        parts.append(f"- **Title:** {profile.title}")
    if profile.is_alias:
        parts.append(f"- **Alias of:** `{profile.alias_of}`")
    parts.append(f"- **Complexity Score:** {profile.complexity_score}/10")
    parts.append("")

    # Encodings
    parts.append(f"### Encodings ({profile.encoding_count})")
    for enc in profile.encodings:
        parts.append(f"- **{enc.name}** ({enc.label})")
        if enc.assembly_template:
            parts.append(f"  - Template: `{enc.assembly_template}`")
        if enc.bitdiffs:
            parts.append(f"  - Condition: `{enc.bitdiffs}`")
        if enc.bit_pattern:
            parts.append(f"  - Bits: `{enc.bit_pattern}`")
        if enc.has_shift_extend:
            parts.append(f"  - Has shift/extend: yes")
    parts.append("")

    # Operands
    parts.append(f"### Operands ({profile.operand_count})")
    for op in profile.operands:
        extra = []
        if op.register_class:
            extra.append(f"reg_class={op.register_class}")
        if op.register_width:
            extra.append(f"width={op.register_width}bit")
        if op.encoded_in:
            extra.append(f"encoded_in={op.encoded_in}")
        extra_str = f" ({', '.join(extra)})" if extra else ""
        parts.append(f"- **{op.symbol}** [{op.operand_type}]{extra_str}: {op.description}")
    parts.append("")

    # Register analysis
    parts.append("### Register Analysis")
    parts.append(f"- General-purpose registers: {profile.gp_register_count}")
    parts.append(f"- SIMD/FP registers: {profile.simd_register_count}")
    parts.append(f"- SVE registers: {profile.sv_register_count}")
    parts.append(f"- Special registers (SP/XZR/PC): {'yes' if profile.has_special_register else 'no'}")
    parts.append(f"- Register widths: {profile.register_widths}")
    parts.append(f"- 32-bit encoding: {'yes' if profile.has_32bit_encoding else 'no'}")
    parts.append(f"- 64-bit encoding: {'yes' if profile.has_64bit_encoding else 'no'}")
    parts.append("")

    # Immediate ranges
    if profile.immediate_ranges:
        parts.append("### Immediate Fields")
        for ir in profile.immediate_ranges:
            signed_str = "signed" if ir.signed else "unsigned"
            parts.append(
                f"- **{ir.operand_symbol}** ({ir.encoded_field}): "
                f"{ir.bit_width}-bit {signed_str}, range 0-{ir.max_value}"
            )
        parts.append("")

    # Constraints
    if profile.constrained_unpredictable:
        parts.append(f"### CONSTRAINED_UNPREDICTABLE ({len(profile.constrained_unpredictable)})")
        for c in profile.constrained_unpredictable[:5]:
            parts.append(f"- `{c.condition}`: {c.description}")
        parts.append("")

    if profile.feature_gates:
        parts.append(f"### Feature Gates ({len(profile.feature_gates)})")
        for c in profile.feature_gates[:5]:
            parts.append(f"- {c.description}")
        parts.append("")

    if profile.encoding_undefined:
        parts.append(f"### Encoding Undefined ({len(profile.encoding_undefined)})")
        for c in profile.encoding_undefined[:3]:
            parts.append(f"- {c.description}")
        parts.append("")

    # Features
    if profile.feature_dependencies:
        parts.append("### Feature Dependencies")
        for f in profile.feature_dependencies:
            version = f" ({f.display_name})" if f.display_name else ""
            parts.append(f"- {f.feature_name}{version}")
        parts.append("")

    # Flags
    parts.append("### Other Properties")
    parts.append(f"- Affects NZCV flags: {'yes' if profile.affects_flags else 'no'}")
    parts.append(f"- Shift/extend: {'yes' if profile.has_shift_extend else 'no'}")
    parts.append(f"- Predicated: {'yes' if profile.is_predicated else 'no'}")

    return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════
# Assembly test system prompt
# ═══════════════════════════════════════════════════════════════

ARM_ASSEMBLY_TEST_PROMPT = """You are an ARM A64 assembly testing expert. 
Generate a standalone ARM assembly test file for the given instruction.

Format requirements:
```asm
// Test: <test_name>
// Description: <what this verifies>
// Requires: <feature if any>

    .text
    .global <test_name>
    .align 2

<test_name>:
    // Register initialization
    // ... mov instructions to set up registers ...

    // Instruction under test
    <instruction>

    // Expected result check
    // ... comparison and branch to fail label ...

    // Success
    mov x0, #0
    ret

fail:
    mov x0, #1
    ret
```

Rules:
1. Use explicit register values (hex preferred: #0xNN)
2. Initialize ALL input registers before the instruction
3. Compare results with expected values
4. Return 0 on success, non-zero on failure
5. Include edge-case tests in separate labels when relevant
6. Use proper ARM A64 syntax (lowercase mnemonics, comma separators)
7. If flags are affected, add flag checking logic with CSET/MRS

Output ONLY the assembly code in a markdown code block."""


INLINE_ASM_SYSTEM_PROMPT = """You are an expert in ARM A64 GCC/Clang inline assembly.
Generate complete C functions using extended asm syntax.

Format:
```c
#include <stdint.h>
#include <stdio.h>

void test_func(void) {
    uint64_t in1 = 0x...;
    uint64_t in2 = 0x...;
    uint64_t result;

    asm volatile(
        "<instruction> %[out], %[in1], %[in2]"
        : [out] "=&r" (result)
        : [in1] "r" (in1), [in2] "r" (in2)
        : "cc"
    );

    // Verify
    uint64_t expected = ...;
    if (result != expected) {
        printf("FAIL: got 0x%lx, expected 0x%lx\\n", result, expected);
    } else {
        printf("PASS\\n");
    }
}
```

Register constraints:
- GP registers: "r" (X0-X30), "=r" for write, "+r" for read-write, "=&r" for early-clobber
- SIMD/FP registers: "w" (V0-V31)
- Immediate: use "I" (0-4095), "J" (-4095 to 0), "K" (shift amounts)
- Flags: always include "cc" in clobbers if NZCV is modified
- Memory: include "memory" if memory is accessed

Output ONLY the C code in a markdown code block."""


LLVM_MC_SYSTEM_PROMPT = """You are an ARM A64 LLVM MC testing expert.
Generate llvm-mc compatible test cases with FileCheck directives.

Format:
```
// RUN: llvm-mc -triple=aarch64 -show-encoding %s | FileCheck %s
// RUN: llvm-mc -triple=aarch64 -filetype=obj %s -o /dev/null

// CHECK: <instruction> <operands>   // encoding: [0xNN,0xNN,0xNN,0xNN]
<instruction> <operands>
```

Rules:
1. FIRST line must have the CHECK encoding comment with proper byte encoding
2. Include at least one RUN line with -show-encoding
3. Use // CHECK: for exact match, // CHECK-NEXT: for sequential checks
4. Use // CHECK-NOT: for negative tests
5. Test all encoding variants
6. Add feature-dependent RUN lines with -mattr=+feature for feature-gated instructions

Output ONLY the assembly test code in a markdown code block."""


# ═══════════════════════════════════════════════════════════════
# Boundary tests prompt
# ═══════════════════════════════════════════════════════════════

BOUNDARY_TEST_PROMPT_TEMPLATE = """Generate comprehensive boundary value tests for this ARM instruction.

For each immediate field found, generate:
1. **Min bound**: smallest valid value (usually 0)
2. **Max bound**: largest valid value
3. **Zero**: zero immediate value
4. **Overflow**: value just beyond valid range (if safe to test)

For register operands, generate:
5. **XZR/WZR**: zero register as source
6. **SP**: stack pointer usage if applicable
7. **Register overlap**: same register as source and destination

For 32/64-bit width variants, generate:
8. **Width boundary**: W registers (32-bit) vs X registers (64-bit)

Output each boundary test as a JSON object:
{
  "test_name": "...",
  "category": "max_immediate|min_immediate|zero|overflow|register_edge|alignment|width_boundary|shift_extreme",
  "instruction": "...",
  "boundary_value": "...",
  "input_state": {"X0": "0x...", "X1": "0x..."},
  "expected_state": {"X0": "0x..."},
  "expected_flags": {"N": "0", "Z": "1", "C": "0", "V": "0"},
  "expected_behavior": "...",
  "risk_assessment": "..."
}

Return a JSON array of boundary test objects."""


# ═══════════════════════════════════════════════════════════════
# Alias tests prompt
# ═══════════════════════════════════════════════════════════════

ALIAS_TEST_PROMPT_TEMPLATE = """For an ARM instruction that is an alias of another canonical form,
generate equivalence tests that verify:

1. The alias produces the same encoding as the canonical form
2. Both produce the same architectural result
3. The alias is correctly decoded/disassembled

Common ARM A64 aliases:
- MOV Xd, Xm  ≡  ORR Xd, XZR, Xm
- MOV Wd, Wm  ≡  ORR Wd, WZR, Wm
- CMP Xn, Xm  ≡  SUBS XZR, Xn, Xm
- CMN Xn, Xm  ≡  ADDS XZR, Xn, Xm
- NEG Xd, Xm  ≡  SUB Xd, XZR, Xm
- TST Xn, Xm  ≡  ANDS XZR, Xn, Xm
- MVN Xd, Xm  ≡  ORN Xd, XZR, Xm

Output each alias test as JSON:
{
  "test_name": "test_mov_alias",
  "alias_mnemonic": "MOV",
  "canonical_mnemonic": "ORR",
  "alias_instruction": "MOV X0, X1",
  "canonical_instruction": "ORR X0, XZR, X1",
  "input_state": {"X1": "0xDEADBEEF"},
  "expected_state": {"X0": "0xDEADBEEF"},
  "behavior_equivalence": "MOV copies register; ORR with XZR achieves same result"
}

Return a JSON array of alias test objects."""


# ═══════════════════════════════════════════════════════════════
# Invalid operand tests prompt
# ═══════════════════════════════════════════════════════════════

INVALID_OPERAND_PROMPT_TEMPLATE = """Based on CONSTRAINED_UNPREDICTABLE and encoding constraints,
generate tests that verify invalid operand combinations are handled correctly.

For each constraint, generate at least one test that exercises the invalid condition.

Categories:
- **register_combination**: e.g., destination == SP when not allowed
- **immediate_range**: value outside the valid immediate range
- **feature_missing**: instruction used without required feature
- **alignment_violation**: unaligned address for alignment-required instruction
- **reserved_bits**: reserved bit pattern set in encoding
- **type_mismatch**: wrong register type for operand

For CONSTRAINED_UNPREDICTABLE conditions, mark is_safe_to_test appropriately:
- Generally safe: register overlap, zero register variants, width variants
- Use caution: truly unpredictable behavior may hang or crash

Output each test as JSON:
{
  "test_name": "...",
  "instruction": "...",
  "invalid_aspect": "register_combination|immediate_range|feature_missing|...",
  "constraint_source": "CONSTRAINED_UNPREDICTABLE",
  "constraint_condition": "...",
  "expected_outcome": "CONSTRAINED_UNPREDICTABLE|UNDEFINED|RESERVED",
  "rationale": "...",
  "is_safe_to_test": true
}

Return a JSON array of invalid operand test objects."""


# ═══════════════════════════════════════════════════════════════
# Feature enable tests prompt
# ═══════════════════════════════════════════════════════════════

FEATURE_ENABLE_PROMPT_TEMPLATE = """For instructions that depend on specific ARM architecture features,
generate tests that verify:

1. **Positive test**: instruction assembles correctly when the feature is enabled
2. **Negative test**: instruction fails to assemble (or produces a diagnostic) when the feature is absent

This ensures the assembler/compiler correctly gates the instruction behind the feature.

Output each test as JSON:
{
  "test_name": "...",
  "instruction": "...",
  "feature_name": "FEAT_SVE",
  "feature_description": "Scalable Vector Extension",
  "architecture_version": "ARMv8.2",
  "enable_flag": "-march=armv8.2-a+sve",
  "test_without_feature": true,
  "assembly_lines": ["..."],
  "check_lines": ["// CHECK: ..."],
  "error_check_lines": ["// CHECK: error: instruction requires: sve"],
  "expected_error": "error: instruction requires: sve"
}

Return a JSON array of feature enable test objects."""


# ═══════════════════════════════════════════════════════════════
# C++ verification program prompt
# ═══════════════════════════════════════════════════════════════

CPP_VERIFICATION_PROMPT = """You are an expert in ARM A64 C++ verification.
Generate a complete, self-checking C++ program that:

1. Implements a reference model of the instruction's expected behavior
2. Uses inline assembly to execute the actual instruction
3. Compares results across a set of strategically chosen inputs
4. Reports PASS/FAIL for each test case

The program should:
- Include proper headers (<cstdint>, <cstdio>)
- Use uint64_t for all register values
- Have a clean test vector format
- Include both trivial (0, small) and non-trivial (large, edge) inputs
- If flags are affected, capture and compare them using NZCV readback

Output ONLY the complete C++ program in a markdown code block."""


# ═══════════════════════════════════════════════════════════════
# Master orchestrator prompt
# ═══════════════════════════════════════════════════════════════

MASTER_GENERATION_PROMPT = """You are an ARM ISA test generation orchestrator.
Given a complete instruction profile, generate a comprehensive test suite covering all relevant test types:

1. ARM Assembly Tests (standalone .s files)
2. LLVM MC Tests (CHECK directives)
3. GCC/Clang Inline Assembly Tests
4. C++ Verification Programs
5. Boundary Value Tests
6. Alias Tests (if instruction has aliases)
7. Invalid Operand Tests (based on constraints)
8. Feature Enable Tests (if feature dependencies exist)

For each test type, generate only the tests that are relevant to this instruction.
Skip test types that don't apply (e.g., skip alias tests if not an alias).

Return a JSON object:
{
  "assembly_tests": [ ... ],
  "llvm_mc_tests": [ ... ],
  "inline_asm_tests": [ ... ],
  "cpp_verification_tests": [ ... ],
  "boundary_tests": [ ... ],
  "alias_tests": [ ... ],
  "invalid_operand_tests": [ ... ],
  "feature_enable_tests": [ ... ],
  "generation_warnings": [ "..." ]
}"""
