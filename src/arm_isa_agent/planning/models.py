"""Planning data models — structured types for instruction analysis and test strategy."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class OperandSummary(BaseModel):
    """Summarized operand metadata for planning."""

    symbol: str = Field(description="Operand symbol, e.g. <Xd>, <imm12>")
    description: str = Field(default="", description="Human-readable description")
    operand_type: str = Field(default="register", description="register | immediate | label | memory | ...")
    register_class: str = Field(default="", description="Register letter class: W/X/B/H/S/D/Q/V/Z")
    register_width: int = Field(default=0, description="Register bit width, 0 for non-register")
    encoded_in: str = Field(default="", description="Encoding field name, e.g. Rd, immhi:immlo")


class ImmediateRange(BaseModel):
    """Immediate operand range extracted from encoding analysis."""

    operand_symbol: str = Field(description="Associated operand, e.g. <imm12>")
    encoded_field: str = Field(default="", description="Bitfield name: imm12, imm9, etc.")
    bit_width: int = Field(default=0, description="Number of bits in the immediate field")
    min_value: int = Field(default=0, description="Minimum possible value (unsigned)")
    max_value: int = Field(default=0, description="Maximum possible value (unsigned)")
    signed: bool = Field(default=False, description="Whether the immediate is sign-extended")
    shift: int = Field(default=0, description="Applied shift multiplier (0, 12, 16, etc.)")


class EncodingSummary(BaseModel):
    """Key encoding metadata for planning."""

    name: str = Field(description="Encoding name, e.g. '32-bit', '64-bit'")
    label: str = Field(default="", description="Human label: 32-bit, 64-bit")
    assembly_template: str = Field(default="", description="Assembly format string")
    bitdiffs: str = Field(default="", description="Encoding selection condition, e.g. sf==0")
    bit_pattern: str = Field(default="", description="Fixed bit pattern")
    has_shift_extend: bool = Field(default=False, description="Encoding includes shift/extend fields")

    @classmethod
    def from_encoding(cls, enc: Any) -> "EncodingSummary":
        has_shift = any(kw in enc.assembly_template.lower()
                        for kw in ["lsl", "lsr", "asr", "ror", "uxt", "sxt"])
        return cls(
            name=enc.name,
            label=enc.label,
            assembly_template=enc.assembly_template,
            bitdiffs=enc.bitdiffs,
            bit_pattern=enc.bit_pattern,
            has_shift_extend=has_shift,
        )


class ConstraintSummary(BaseModel):
    """Constraint summary grouped by type."""

    constraint_type: str = Field(description="CONSTRAINED_UNPREDICTABLE | FEATURE_GATE | ENCODING_UNDEF | DECODE_FALLBACK")
    condition: str = Field(default="", description="Constraint condition expression")
    description: str = Field(default="", description="Human-readable description")
    count: int = Field(default=0, description="Number of constraints of this type")


class FeatureDependency(BaseModel):
    """Architecture feature required by the instruction."""

    feature_name: str = Field(description="e.g. FEAT_FP, FEAT_SVE")
    display_name: str = Field(default="", description="e.g. ARMv8.0, ARMv9.3")
    feature_level: str = Field(default="", description="section | iclass | encoding")


class InstructionProfile(BaseModel):
    """Complete instruction metadata profile for test planning.

    This is the core data structure produced by InstructionAnalyzer
    and consumed by the LLM for test strategy generation.
    """

    # ---- Identification ----
    xml_id: str = Field(default="", description="Unique XML identifier")
    mnemonic: str = Field(default="", description="Assembly mnemonic")
    title: str = Field(default="", description="Full instruction title")
    instr_class: str = Field(default="", description="Instruction class: general, fpsimd, sve, ...")
    is_alias: bool = Field(default=False, description="True if this is an alias instruction")
    alias_of: str = Field(default="", description="Canonical instruction if alias")

    # ---- Description ----
    brief: str = Field(default="", description="One-line summary")
    description_preview: str = Field(default="", description="First 500 chars of description")

    # ---- Encodings ----
    encoding_count: int = Field(default=0, description="Total number of encoding variants")
    encodings: list[EncodingSummary] = Field(default_factory=list, description="Encoding summaries")

    # ---- Operands ----
    operand_count: int = Field(default=0)
    operands: list[OperandSummary] = Field(default_factory=list, description="All operands")

    # ---- Immediate Analysis ----
    immediate_ranges: list[ImmediateRange] = Field(default_factory=list, description="Detected immediate fields")

    # ---- Register Analysis ----
    gp_register_count: int = Field(default=0, description="General-purpose register operands")
    simd_register_count: int = Field(default=0, description="SIMD/FP register operands")
    sv_register_count: int = Field(default=0, description="SVE register operands (Z/P)")
    has_special_register: bool = Field(default=False, description="Uses SP/WZR/XZR/PC")
    register_widths: list[int] = Field(default_factory=list, description="Register widths used (32, 64, 128)")

    # ---- Shift/Extend ----
    has_shift_extend: bool = Field(default=False, description="Instruction supports shift/extend")

    # ---- Constraints ----
    constrained_unpredictable: list[ConstraintSummary] = Field(default_factory=list)
    feature_gates: list[ConstraintSummary] = Field(default_factory=list)
    encoding_undefined: list[ConstraintSummary] = Field(default_factory=list)

    # ---- Features ----
    feature_dependencies: list[FeatureDependency] = Field(default_factory=list)

    # ---- Architecture ----
    architecture_versions: list[str] = Field(default_factory=list, description="Supported arch versions, e.g. [ARMv8.0, ARMv9.3]")
    has_32bit_encoding: bool = Field(default=False)
    has_64bit_encoding: bool = Field(default=False)

    # ---- Pseudocode ----
    pseudocode_section_types: list[str] = Field(default_factory=list, description="Available pseudocode sections")

    # ---- Flags ----
    affects_flags: bool = Field(default=False, description="Modifies NZCV condition flags")
    is_predicated: bool = Field(default=False)
    uses_dit: bool = Field(default=False)

    @property
    def complexity_score(self) -> int:
        """Heuristic complexity score (0-10). Used to estimate test effort."""
        score = 1  # base
        score += min(self.encoding_count, 3)  # more encodings = more complex
        score += self.operand_count // 2  # more operands
        if self.has_shift_extend:
            score += 1
        if self.constrained_unpredictable:
            score += 2
        if self.feature_dependencies:
            score += 1
        if self.is_alias:
            score -= 1  # aliases tend to be simpler
        if self.simd_register_count > 0:
            score += 1
        if self.sv_register_count > 0:
            score += 2
        return min(score, 10)


class TestDimension(BaseModel):
    """A single test dimension with priority and focus areas."""

    name: str = Field(description="Dimension name: Normal, Boundary, Register, Encoding, ...")
    priority: str = Field(default="medium", description="high | medium | low")
    coverage_percentage: float = Field(default=0.0, description="Recommended test allocation %")
    focus_areas: list[str] = Field(default_factory=list, description="Specific areas to focus testing on")
    rationale: str = Field(default="", description="Why this dimension is important for this instruction")
    suggested_test_count: int = Field(default=2, description="Number of test cases recommended")


class TestStrategy(BaseModel):
    """Complete test strategy for an instruction."""

    instruction_id: str = Field(description="Instruction mnemonic or xml_id")
    total_test_count: int = Field(default=8, description="Recommended total test cases")
    complexity: int = Field(default=3, description="Complexity score (0-10)")
    dimensions: list[TestDimension] = Field(default_factory=list, description="Test dimensions with priorities")
    coverage_matrix: dict[str, list[str]] = Field(default_factory=dict, description="Dimension → covered encodings/features")
    risk_analysis: str = Field(default="", description="Risk assessment and mitigation suggestions")
    constraints_to_verify: list[str] = Field(default_factory=list, description="CONSTRAINED_UNPREDICTABLE conditions to test")


class PlanOutput(BaseModel):
    """Final structured planning output."""

    instruction: InstructionProfile
    strategy: TestStrategy
    reasoning: str = Field(default="", description="LLM's reasoning about the plan")
    test_plan_summary: str = Field(default="", description="Human-readable test plan summary")
