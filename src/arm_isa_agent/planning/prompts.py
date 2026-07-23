"""Planning prompt templates — instruction analysis and test strategy generation."""

from __future__ import annotations

import json
from typing import Any

from arm_isa_agent.planning.models import InstructionProfile


# ── Instruction Profile → Context ────────────────────────────────

def format_profile_context(profile: InstructionProfile) -> str:
    """Convert InstructionProfile into a structured text blob for the LLM."""

    def _presence(b: bool) -> str:
        return "YES" if b else "NO"

    lines: list[str] = []
    lines.append(f"## Instruction: {profile.mnemonic} ({profile.xml_id})")
    lines.append(f"**Title**: {profile.title}")
    lines.append(f"**Class**: {profile.instr_class}")
    lines.append(f"**Brief**: {profile.brief}")
    if profile.is_alias:
        lines.append(f"**Alias**: YES (canonical: {profile.alias_of})")
    if profile.description_preview:
        lines.append(f"**Description**: {profile.description_preview}")
    lines.append("")

    # ---- Encodings ----
    lines.append(f"### Encodings ({profile.encoding_count})")
    for i, enc in enumerate(profile.encodings):
        bits = "32-bit" if profile.has_32bit_encoding else ""
        bits_64 = "64-bit" if profile.has_64bit_encoding else ""
        if bits and bits_64:
            bits = "32/64-bit"
        elif not bits and bits_64:
            bits = "64-bit"
        lines.append(f"  {i+1}. **{enc.name}** ({enc.label})")
        lines.append(f"     Template: `{enc.assembly_template}`")
        if enc.bitdiffs:
            lines.append(f"     Condition: {enc.bitdiffs}")
        if enc.bit_pattern:
            lines.append(f"     Bit pattern: {enc.bit_pattern}")
        if enc.has_shift_extend:
            lines.append(f"     Supports shift/extend: YES")
    lines.append("")

    # ---- Operands ----
    lines.append(f"### Operands ({profile.operand_count})")
    for op in profile.operands:
        extra: list[str] = []
        if op.register_class:
            extra.append(f"reg_class={op.register_class}")
        if op.register_width:
            extra.append(f"width={op.register_width}bit")
        if op.encoded_in:
            extra.append(f"field={op.encoded_in}")
        meta = ", ".join(extra)
        lines.append(f"  - `{op.symbol}` [{op.operand_type}]: {op.description}" +
                     (f" ({meta})" if meta else ""))
    lines.append("")

    # ---- Register Summary ----
    lines.append("### Register Usage Summary")
    lines.append(f"  GP registers: {profile.gp_register_count}")
    lines.append(f"  SIMD/FP registers: {profile.simd_register_count}")
    lines.append(f"  SVE registers: {profile.sv_register_count}")
    lines.append(f"  Special registers (SP/XZR/PC): {_presence(profile.has_special_register)}")
    if profile.register_widths:
        lines.append(f"  Register widths: {', '.join(str(w) + 'bit' for w in sorted(profile.register_widths))}")
    lines.append("")

    # ---- Immediate Ranges ----
    if profile.immediate_ranges:
        lines.append("### Immediate Value Ranges")
        for ir in profile.immediate_ranges:
            sign = "signed" if ir.signed else "unsigned"
            shift_info = f", shift={ir.shift}" if ir.shift else ""
            lines.append(f"  {ir.operand_symbol}: {ir.bit_width}-bit {sign}, "
                         f"range=[{ir.min_value}, {ir.max_value}]{shift_info}")
        lines.append("")

    # ---- Constraints ----
    total_cons = len(profile.constrained_unpredictable) + len(profile.feature_gates) + len(profile.encoding_undefined)
    if total_cons > 0:
        lines.append(f"### Constraints ({total_cons})")
        if profile.constrained_unpredictable:
            lines.append(f"  **CONSTRAINED_UNPREDICTABLE ({len(profile.constrained_unpredictable)}):**")
            for c in profile.constrained_unpredictable[:5]:
                desc = c.description[:120] if c.description else "(no description)"
                cond = c.condition[:80] if c.condition else "always"
                lines.append(f"    - Condition: {cond}")
                lines.append(f"      Behavior: {desc}")
        if profile.feature_gates:
            lines.append(f"  **FEATURE_GATE ({len(profile.feature_gates)}):**")
            for c in profile.feature_gates[:3]:
                lines.append(f"    - {c.description[:120]}")
        if profile.encoding_undefined:
            lines.append(f"  **ENCODING_UNDEF ({len(profile.encoding_undefined)}):**")
        lines.append("")

    # ---- Features ----
    if profile.feature_dependencies:
        lines.append("### Feature Dependencies")
        for fd in profile.feature_dependencies:
            label = f"{fd.feature_name} ({fd.display_name})" if fd.display_name else fd.feature_name
            lines.append(f"  - {label}")
        lines.append("")

    # ---- Architecture ----
    if profile.architecture_versions:
        lines.append(f"### Architecture Versions: {', '.join(profile.architecture_versions)}")
        lines.append("")

    # ---- Flags ----
    lines.append("### Behavioral Characteristics")
    lines.append(f"  Affects NZCV flags: {_presence(profile.affects_flags)}")
    lines.append(f"  Supports shift/extend: {_presence(profile.has_shift_extend)}")
    lines.append(f"  Is predicated: {_presence(profile.is_predicated)}")
    lines.append(f"  Uses DIT: {_presence(profile.uses_dit)}")
    lines.append(f"  Has 32-bit encoding: {_presence(profile.has_32bit_encoding)}")
    lines.append(f"  Has 64-bit encoding: {_presence(profile.has_64bit_encoding)}")
    if profile.pseudocode_section_types:
        lines.append(f"  Pseudocode sections: {', '.join(profile.pseudocode_section_types)}")
    lines.append("")

    lines.append(f"**Complexity Score**: {profile.complexity_score}/10")
    return "\n".join(lines)


# ── Strategy Generation Prompt ────────────────────────────────────

STRATEGY_SYSTEM_PROMPT = """You are an ARM ISA testing expert specializing in comprehensive verification planning.

Your task: Given an instruction profile with detailed metadata (encodings, operands, constraints,
features, immediate ranges, register usage), produce a structured test strategy.

## Strategy Principles

1. **Coverage-first**: Every encoding variant and operand combination should be tested.
2. **Constraint-driven**: CONSTRAINED_UNPREDICTABLE and FEATURE_GATE constraints define
   critical edge cases that MUST be tested.
3. **Dimension-balanced**: Distribute test effort across Normal, Boundary, Register,
   Encoding, and Constraint dimensions based on instruction characteristics.
4. **Risk-aware**: Higher complexity instructions need more thorough testing.

## Output Requirements

Produce a JSON object with this structure:

```json
{
  "reasoning": "Brief explanation of your strategy (2-3 sentences)",
  "dimensions": [
    {
      "name": "Dimension name",
      "priority": "high|medium|low",
      "coverage_percentage": 25.0,
      "focus_areas": ["specific focus 1", "specific focus 2"],
      "rationale": "Why this dimension matters for this instruction",
      "suggested_test_count": 3
    }
  ],
  "total_test_count": 12,
  "risk_analysis": "Risk assessment and testing recommendations",
  "constraints_to_verify": ["constraint description 1", "constraint description 2"]
}
```

## Dimension Guidelines

Always consider these standard dimensions, adapting based on the profile:

- **Normal Operation**: Core functional correctness — always included (high priority).
- **Boundary Values**: Min/max immediate values, zero register — if immediate operands exist.
- **Register Constraints**: Overlapping src/dst, SP/XZR usage, register width — if applicable.
- **Encoding Coverage**: Each encoding variant separately — if multiple encodings exist.
- **CONSTRAINED_UNPREDICTABLE**: Conditions that trigger UNDEFINED behavior — if constraints exist.
- **Feature Dependency**: Feature-gated or architecture-specific behavior — if features exist.
- **Shift/Extend Coverage**: Various shift amounts and extend modes — if shift/extend supported.
- **Flag Effects**: NZCV flag transitions — if flags are modified.

## Test Count Recommendation

- Simple instructions (complexity 1-3): 6-10 test cases
- Medium complexity (4-6): 10-15 test cases
- High complexity (7-10): 15-25 test cases

Output ONLY the JSON object, no other text."""


def build_strategy_prompt(profile_context: str, user_goal: str = "") -> str:
    """Build the strategy generation user prompt."""
    goal_text = f"\n\n## User Goal\n{user_goal}" if user_goal else ""
    return f"""## Instruction Profile

{profile_context}
{goal_text}

Based on this profile, generate a comprehensive test strategy as JSON.
Focus on practical, implementable test dimensions that provide the most coverage
with the fewest test cases."""


# ── Plan Synthesis Prompt ─────────────────────────────────────────

PLAN_SYNTHESIS_PROMPT = """You are an ARM ISA documentation expert.

Given a test strategy for an ARM instruction, produce a human-readable summary
that answers: "What should I test, and why?"

## Format

Use markdown with these sections:
1. **Instruction Overview** — what this instruction does
2. **Test Strategy** — high-level testing approach
3. **Test Dimensions** — each dimension with specific focus areas
4. **Key Edge Cases** — critical CONSTRAINED_UNPREDICTABLE or boundary conditions
5. **Recommended Test Cases** — numbered list of specific test scenarios

Be concise but technically precise. Use ARM ISA terminology.
"""


# ── Profile Serialization ─────────────────────────────────────────

def serialize_profile_to_json(profile: InstructionProfile) -> str:
    """Serialize profile to JSON for programmatic consumption."""
    out: dict[str, Any] = {
        "xml_id": profile.xml_id,
        "mnemonic": profile.mnemonic,
        "title": profile.title,
        "instr_class": profile.instr_class,
        "is_alias": profile.is_alias,
        "alias_of": profile.alias_of or None,
        "brief": profile.brief,
        "complexity_score": profile.complexity_score,
        "encoding_count": profile.encoding_count,
        "operand_count": profile.operand_count,
        "has_shift_extend": profile.has_shift_extend,
        "affects_flags": profile.affects_flags,
        "has_32bit_encoding": profile.has_32bit_encoding,
        "has_64bit_encoding": profile.has_64bit_encoding,
        "gp_register_count": profile.gp_register_count,
        "simd_register_count": profile.simd_register_count,
        "sv_register_count": profile.sv_register_count,
        "has_special_register": profile.has_special_register,
        "register_widths": profile.register_widths,
        "immediate_ranges": [
            {
                "symbol": ir.operand_symbol,
                "field": ir.encoded_field,
                "bits": ir.bit_width,
                "min": ir.min_value,
                "max": ir.max_value,
                "signed": ir.signed,
            }
            for ir in profile.immediate_ranges
        ],
        "constrained_unpredictable_count": len(profile.constrained_unpredictable),
        "feature_gates_count": len(profile.feature_gates),
        "feature_dependencies": [
            fd.feature_name for fd in profile.feature_dependencies
        ],
        "architecture_versions": profile.architecture_versions,
    }
    return json.dumps(out, ensure_ascii=False, indent=2)
