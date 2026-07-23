"""Testcase Generators — rule-based + LLM-assisted test generation for all 8 formats.

Each generator:
1. Takes an InstructionProfile as input
2. Has a rule-based (deterministic) code path for fast local generation
3. Supports LLM-assisted generation for higher-quality outputs
4. Returns typed Pydantic model instances
"""

from __future__ import annotations

import json
import re
from typing import Any, Optional

import structlog

from arm_isa_agent.generation.models import (
    ARMAssemblyTestCase,
    AliasTestCase,
    BoundaryTestCase,
    CppVerificationTestCase,
    FeatureEnableTestCase,
    InlineAsmTestCase,
    InvalidOperandTestCase,
    LLVMMCTestCase,
    TestCaseSuite,
)
from arm_isa_agent.generation.prompts import (
    ALIAS_TEST_PROMPT_TEMPLATE,
    ARM_ASSEMBLY_TEST_PROMPT,
    BOUNDARY_TEST_PROMPT_TEMPLATE,
    CPP_VERIFICATION_PROMPT,
    FEATURE_ENABLE_PROMPT_TEMPLATE,
    INLINE_ASM_SYSTEM_PROMPT,
    INVALID_OPERAND_PROMPT_TEMPLATE,
    LLVM_MC_SYSTEM_PROMPT,
    format_profile_context,
)
from arm_isa_agent.planning.models import InstructionProfile

logger = structlog.get_logger(__name__)

# ═══════════════════════════════════════════════════════════════
# Common helpers
# ═══════════════════════════════════════════════════════════════

# Known ARM A64 aliases: alias → (canonical_mnemonic, canonical_transformation)
_KNOWN_ALIASES: dict[str, tuple[str, str, str]] = {
    "MOV": ("ORR", "ORR {{dst}}, XZR, {{src}}", "MOV {dst}, {src} copies register; ORR with XZR is identity"),
    "CMP": ("SUBS", "SUBS XZR, {{src1}}, {{src2}}", "CMP subtracts and discards result, only setting flags"),
    "CMN": ("ADDS", "ADDS XZR, {{src1}}, {{src2}}", "CMN adds and discards result, only setting flags"),
    "NEG": ("SUB", "SUB {{dst}}, XZR, {{src}}", "NEG subtracts from zero"),
    "TST": ("ANDS", "ANDS XZR, {{src1}}, {{src2}}", "TST performs bitwise AND and discards result"),
    "MVN": ("ORN", "ORN {{dst}}, XZR, {{src}}", "MVN is bitwise NOT via ORN with zero"),
    "MADD": ("MADD", "MADD {{dst}}, {{src1}}, {{src2}}, XZR", "MADD with zero accumulator is MUL"),
}

# Regex patterns for instruction operand parsing
_RE_REGISTERS = re.compile(r"[XW]\d{1,2}|[XW]ZR|SP|WSP|[BVHSDQ]\d{1,2}|[ZP]\d{1,2}")
_RE_IMMEDIATE = re.compile(r"#-?\d+|#0x[0-9a-fA-F]+|#\d+")
_RE_SHIFT = re.compile(r"(LSL|LSR|ASR|ROR|UXTB|UXTH|UXTW|UXTX|SXTB|SXTH|SXTW|SXTX)\s+#?\d*")

# Register ranges for boundary tests
_GP_REGS_32 = [f"W{i}" for i in range(31)] + ["WZR"]
_GP_REGS_64 = [f"X{i}" for i in range(31)] + ["XZR"]


def _select_register(
    index: int,
    prefer_64: bool = True,
    exclude_special: bool = False,
) -> str:
    """Pick a general-purpose register by index, avoiding special registers."""
    if prefer_64:
        pool = _GP_REGS_64
    else:
        pool = _GP_REGS_32
    if exclude_special:
        pool = [r for r in pool if r not in ("XZR", "WZR", "SP", "WSP")]
    idx = index % len(pool)
    return pool[idx]


def _to_reg_list(count: int, start: int = 0, prefer_64: bool = True, exclude_special: bool = False) -> list[str]:
    """Generate a list of unique register names."""
    regs: list[str] = []
    for i in range(count):
        regs.append(_select_register(start + i, prefer_64, exclude_special))
    return regs


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
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Try extracting from code blocks
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
    # Try finding outermost { or [
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


# ═══════════════════════════════════════════════════════════════
# 1. ARM Assembly Test Generator
# ═══════════════════════════════════════════════════════════════

class ARMAssemblyTestGenerator:
    """Generate standalone ARM assembly test files (.s)."""

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def generate(
        self,
        profile: InstructionProfile,
        use_llm: bool = False,
        count: int = 3,
    ) -> list[ARMAssemblyTestCase]:
        """Generate assembly test cases."""
        if use_llm and self._llm:
            return self._generate_with_llm(profile, count)
        return self._generate_rule_based(profile, count)

    def _generate_rule_based(
        self,
        profile: InstructionProfile,
        count: int,
    ) -> list[ARMAssemblyTestCase]:
        """Rule-based assembly test generation."""
        tests: list[ARMAssemblyTestCase] = []
        mnemonic = profile.mnemonic.upper()
        is_64bit = profile.has_64bit_encoding
        reg_prefix = "X" if is_64bit else "W"
        immediate_val = "0x10"

        # Determine if we have an immediate operand
        has_imm = any(op.operand_type == "immediate" for op in profile.operands)

        # Count register operands
        reg_ops = [op for op in profile.operands if op.operand_type == "register"]
        n_regs = len(reg_ops)

        # Build instruction string from template
        if profile.encodings:
            template = profile.encodings[0].assembly_template
            inst_str = self._instantiate_template(template, profile, reg_prefix, immediate_val)
        else:
            inst_str = f"{mnemonic.lower()} {reg_prefix}0, {reg_prefix}1"

        # Test 1: Normal case
        inputs: dict[str, str] = {}
        expected: dict[str, str] = {}
        if n_regs >= 2:
            dst = _select_register(0, is_64bit, exclude_special=True)
            src1 = _select_register(1, is_64bit, exclude_special=True)
            inputs = {src1: "0x10"}
            if n_regs >= 3:
                src2 = _select_register(2, is_64bit, exclude_special=True)
                inputs[src2] = "0x20" if not has_imm else "0x20"
                expected[dst] = "0x30"  # 0x10 + 0x20 for ADD-like
            else:
                expected[dst] = "0x10"
            expected[dst] = expected.get(dst, "0x10")

        tests.append(ARMAssemblyTestCase(
            test_name=f"test_{mnemonic.lower()}_normal",
            description=f"Normal {profile.brief or 'operation'} with standard register values",
            instruction=inst_str,
            input_state=inputs,
            expected_state=expected,
            encoding_name=profile.encodings[0].name if profile.encodings else "",
            comments=["Normal case", f"mnemonic={mnemonic}", f"operands={len(profile.operands)}"],
        ))

        # Test 2: Zero register (XZR) test if applicable
        if profile.has_special_register and "XZR" in str(profile.operands) or profile.gp_register_count >= 2:
            zr = "XZR" if is_64bit else "WZR"
            zero_inputs: dict[str, str] = {}
            zero_expected: dict[str, str] = {}
            if n_regs >= 2:
                dst0 = _select_register(1, is_64bit, exclude_special=True)
                src0 = _select_register(2, is_64bit, exclude_special=True)
                zero_inputs = {src0: "0x42"}
                zero_expected = {dst0: "0x42"}  # any op with XZR likely passes through

            tests.append(ARMAssemblyTestCase(
                test_name=f"test_{mnemonic.lower()}_zero_reg",
                description=f"Zero register ({zr}) as operand",
                instruction=inst_str.replace(reg_prefix + "1", zr),
                input_state=zero_inputs,
                expected_state=zero_expected,
                comments=["Zero register test"],
            ))

        # Test 3: Flag effects (if applicable)
        if profile.affects_flags or mnemonic.endswith("S"):
            flag_inputs: dict[str, str] = {}
            flag_expected: dict[str, str] = {}
            if n_regs >= 2:
                dst_f = _select_register(3, is_64bit, exclude_special=True)
                src_f = _select_register(4, is_64bit, exclude_special=True)
                flag_inputs = {src_f: "0x1"}
                flag_expected = {dst_f: "0x1"}
                flag_expected_flags = {"N": "0", "Z": "0", "C": "0", "V": "0"}

            tests.append(ARMAssemblyTestCase(
                test_name=f"test_{mnemonic.lower()}_flags",
                description="Verify NZCV flag effects",
                instruction=inst_str,
                input_state=flag_inputs,
                expected_state=flag_expected,
                expected_flags=flag_expected_flags if 'flag_expected_flags' in dir() else {},
                comments=["Flag verification test"],
            ))

        return tests[:count]

    def _generate_with_llm(
        self,
        profile: InstructionProfile,
        count: int,
    ) -> list[ARMAssemblyTestCase]:
        """LLM-assisted assembly test generation."""
        ctx = format_profile_context(profile)
        prompt = f"""Generate {count} ARM assembly test cases.

{ctx}

Output ONLY a JSON array of objects with: test_name, description, instruction, input_state, expected_state, expected_flags, comments."""
        result = _safe_llm_invoke(self._llm, ARM_ASSEMBLY_TEST_PROMPT, prompt)
        data = _parse_json_response(result, [])
        return [ARMAssemblyTestCase(**item) for item in data]

    @staticmethod
    def _instantiate_template(
        template: str,
        profile: InstructionProfile,
        reg_prefix: str,
        immediate_val: str,
    ) -> str:
        """Instantiate an assembly template with concrete register values."""
        inst = template
        # Replace operand placeholders with concrete values
        for i, op in enumerate(profile.operands):
            symbol = op.symbol.strip("<>")
            if op.operand_type == "register":
                reg = _select_register(i, reg_prefix == "X", exclude_special=True)
                inst = inst.replace(f"<{symbol}>", reg)
            elif op.operand_type == "immediate":
                inst = inst.replace(f"<{symbol}>", f"#{immediate_val}")
            elif op.operand_type == "label":
                inst = inst.replace(f"<{symbol}>", "target_label")
        return inst


# ═══════════════════════════════════════════════════════════════
# 2. LLVM MC Test Generator
# ═══════════════════════════════════════════════════════════════

class LLVMMCTestGenerator:
    """Generate LLVM MC test files with CHECK directives."""

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def generate(
        self,
        profile: InstructionProfile,
        use_llm: bool = False,
    ) -> list[LLVMMCTestCase]:
        """Generate LLVM MC tests for all encodings."""
        if use_llm and self._llm:
            return self._generate_with_llm(profile)
        return self._generate_rule_based(profile)

    def _generate_rule_based(self, profile: InstructionProfile) -> list[LLVMMCTestCase]:
        """Rule-based LLVM MC test generation."""
        tests: list[LLVMMCTestCase] = []
        mnemonic = profile.mnemonic.lower()

        for enc in profile.encodings:
            # Build concrete assembly from template
            asm_template = enc.assembly_template or f"{mnemonic} X0, X1, X2"
            asm_line = self._concretize_template(asm_template, profile)

            check_lines: list[str] = []
            check_lines.append(f"// CHECK: {asm_line}")
            if enc.bit_pattern:
                check_lines.append(f"// CHECK-SAME: encoding: [{enc.bit_pattern}]")

            tests.append(LLVMMCTestCase(
                test_name=f"test_{mnemonic}_{enc.name.replace(' ', '_').replace('-', '_').lower()}",
                description=f"LLVM MC test for {enc.name} encoding",
                assembly_lines=[f"\t{asm_line}"],
                check_lines=check_lines,
                encoding_name=enc.name,
            ))

        # Add a negative test for invalid encoding if constraints exist
        if profile.encoding_undefined or profile.constrained_unpredictable:
            bad_asm = self._generate_invalid_assembly(profile)
            if bad_asm:
                tests.append(LLVMMCTestCase(
                    test_name=f"test_{mnemonic}_invalid_encoding",
                    description="Verify invalid encoding is rejected",
                    assembly_lines=[f"\t{bad_asm}"],
                    check_lines=[f"// CHECK: error:"],
                    check_not_lines=[f"// CHECK-NOT: {bad_asm}"],
                ))

        return tests

    def _generate_with_llm(self, profile: InstructionProfile) -> list[LLVMMCTestCase]:
        """LLM-assisted LLVM MC test generation."""
        ctx = format_profile_context(profile)
        prompt = f"""Generate LLVM MC test cases for this instruction.

{ctx}

Output a JSON array with: test_name, description, assembly_lines, check_lines, check_not_lines, encoding_name."""
        result = _safe_llm_invoke(self._llm, LLVM_MC_SYSTEM_PROMPT, prompt)
        data = _parse_json_response(result, [])
        return [LLVMMCTestCase(**item) for item in data]

    @staticmethod
    def _concretize_template(template: str, profile: InstructionProfile) -> str:
        """Replace template placeholders with concrete register values."""
        inst = template
        for i, op in enumerate(profile.operands):
            symbol = op.symbol.strip("<>")
            if op.operand_type == "register":
                reg = _select_register(i, True, True)
                inst = inst.replace(f"<{symbol}>", reg)
            elif op.operand_type == "immediate":
                inst = inst.replace(f"<{symbol}>", "#0")
            elif op.operand_type == "label":
                inst = inst.replace(f"<{symbol}>", "label")
        return inst

    @staticmethod
    def _generate_invalid_assembly(profile: InstructionProfile) -> str:
        """Generate deliberately invalid assembly for negative testing."""
        mnemonic = profile.mnemonic.lower()
        # Use a register type that doesn't match any operand
        return f"{mnemonic} x255, x255, x255"


# ═══════════════════════════════════════════════════════════════
# 3. Inline Assembly Test Generator
# ═══════════════════════════════════════════════════════════════

class InlineAsmTestGenerator:
    """Generate GCC/Clang inline assembly test functions."""

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def generate(
        self,
        profile: InstructionProfile,
        use_llm: bool = False,
        count: int = 2,
    ) -> list[InlineAsmTestCase]:
        """Generate inline assembly tests."""
        if use_llm and self._llm:
            return self._generate_with_llm(profile, count)
        return self._generate_rule_based(profile, count)

    def _generate_rule_based(
        self,
        profile: InstructionProfile,
        count: int,
    ) -> list[InlineAsmTestCase]:
        """Rule-based inline assembly test generation."""
        tests: list[InlineAsmTestCase] = []
        mnemonic = profile.mnemonic.lower()
        is_64bit = profile.has_64bit_encoding

        # Parse operands to build inline asm
        reg_ops = [op for op in profile.operands if op.operand_type == "register"]
        imm_ops = [op for op in profile.operands if op.operand_type == "immediate"]
        n_regs = len(reg_ops)

        # Build instruction with named operands
        operands_list: list[str] = []
        in_constraints: list[str] = []
        out_constraints: list[str] = []
        clobber_list = ['"cc"'] if profile.affects_flags else []
        if profile.operands and any(op.operand_type == "memory" or "memory" in str(op.symbol).lower()
                                    for op in profile.operands):
            clobber_list.append('"memory"')

        op_idx = 0
        for op in profile.operands:
            name = op.symbol.strip("<>").replace("{", "").replace("}", "")
            if op.operand_type == "register":
                if op_idx == 0:
                    # First register is usually destination
                    operands_list.append(f"%[out{op_idx}]")
                    out_constraints.append(f'[out{op_idx}] "=&r" (result)')
                else:
                    operands_list.append(f"%[in{op_idx}]")
                    in_constraints.append(f'[in{op_idx}] "r" (in{op_idx})')
                op_idx += 1
            elif op.operand_type == "immediate":
                operands_list.append(f"%[imm{op_idx}]")
                in_constraints.append(f'[imm{op_idx}] "I" (imm{op_idx})')
                op_idx += 1

        inst_str = f"{mnemonic} {', '.join(operands_list)}"
        clobbers = ", ".join(clobber_list) if clobber_list else '""'

        feature = ""
        if profile.feature_dependencies:
            feature = profile.feature_dependencies[0].feature_name

        tests.append(InlineAsmTestCase(
            test_name=f"test_{mnemonic}_inline",
            description=f"Inline assembly test for {mnemonic}",
            instruction=inst_str,
            input_operands=", ".join(in_constraints),
            output_operands=", ".join(out_constraints),
            clobbers=clobbers,
            feature_required=feature,
        ))

        # Width variant test
        if profile.has_32bit_encoding and profile.has_64bit_encoding:
            tests.append(InlineAsmTestCase(
                test_name=f"test_{mnemonic}_32bit_inline",
                description=f"32-bit width inline assembly test for {mnemonic}",
                instruction=inst_str,
                input_operands=", ".join(in_constraints).replace("r\"", "w\""),
                output_operands=", ".join(out_constraints).replace("r\"", "w\""),
                clobbers=clobbers,
                feature_required=feature,
            ))

        return tests[:count]

    def _generate_with_llm(
        self,
        profile: InstructionProfile,
        count: int,
    ) -> list[InlineAsmTestCase]:
        """LLM-assisted inline assembly generation."""
        ctx = format_profile_context(profile)
        prompt = f"""Generate {count} inline assembly test functions.

{ctx}

Output a JSON array with: test_name, description, instruction, input_operands, output_operands, clobbers, feature_required."""
        result = _safe_llm_invoke(self._llm, INLINE_ASM_SYSTEM_PROMPT, prompt)
        data = _parse_json_response(result, [])
        return [InlineAsmTestCase(**item) for item in data]


# ═══════════════════════════════════════════════════════════════
# 4. C++ Verification Program Generator
# ═══════════════════════════════════════════════════════════════

class CppVerificationGenerator:
    """Generate self-checking C++ verification programs."""

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def generate(
        self,
        profile: InstructionProfile,
        use_llm: bool = False,
    ) -> list[CppVerificationTestCase]:
        """Generate C++ verification programs."""
        if use_llm and self._llm:
            return self._generate_with_llm(profile)
        return self._generate_rule_based(profile)

    def _generate_rule_based(self, profile: InstructionProfile) -> list[CppVerificationTestCase]:
        """Rule-based C++ verification generation."""
        mnemonic = profile.mnemonic.lower()
        is_64bit = profile.has_64bit_encoding
        reg_prefix = "X" if is_64bit else "W"

        # Build instruction with concrete registers
        regs = _to_reg_list(3, prefer_64=is_64bit, exclude_special=True)
        inst = f"{mnemonic} {regs[0]}, {regs[1]}, {regs[2]}" if len(regs) >= 3 else f"{mnemonic} {regs[0]}, {regs[1]}"

        # Determine reference model hint based on instruction class
        ref_model = self._infer_reference_model(profile, regs)

        # Generate test vectors
        test_vectors_in = [
            {"a": "0", "b": "0"},
            {"a": "1", "b": "1"},
            {"a": "0xFFFFFFFF", "b": "1"},
            {"a": "0x70000000", "b": "0x10000000"},
        ]
        test_vectors_out = [
            {"result": "0"},
            {"result": "2"},
            {"result": "0x100000000"},
            {"result": "0x80000000"},
        ]

        # Adjust for immediate operand presence
        has_imm = any(op.operand_type == "immediate" for op in profile.operands)
        if has_imm:
            test_vectors_in = [
                {"a": "0", "b": "0"},
                {"a": "0xFF", "b": "0"},
                {"a": "0", "b": "0xFF"},
            ]
            test_vectors_out = [
                {"result": "0"},
                {"result": "0xFF"},
                {"result": "0xFFFFFFFFFFFFFF00"},
            ]

        feature = profile.feature_dependencies[0].feature_name if profile.feature_dependencies else ""

        return [CppVerificationTestCase(
            test_name=f"verify_{mnemonic}",
            description=f"Self-checking verification for {mnemonic} ({profile.brief})",
            instruction=inst,
            reference_model=ref_model,
            test_inputs=test_vectors_in,
            expected_outputs=test_vectors_out,
            feature_required=feature,
        )]

    def _generate_with_llm(self, profile: InstructionProfile) -> list[CppVerificationTestCase]:
        """LLM-assisted C++ verification."""
        ctx = format_profile_context(profile)
        prompt = f"""Generate a C++ verification program.

{ctx}

Output a JSON object with: test_name, description, instruction, reference_model, test_inputs, expected_outputs, feature_required.
test_inputs and expected_outputs should be arrays of dicts."""
        result = _safe_llm_invoke(self._llm, CPP_VERIFICATION_PROMPT, prompt)
        data = _parse_json_response(result, [])
        if isinstance(data, dict):
            data = [data]
        return [CppVerificationTestCase(**item) for item in data]

    @staticmethod
    def _infer_reference_model(profile: InstructionProfile, regs: list[str]) -> str:
        """Infer reference model description from instruction class."""
        cls_lower = profile.instr_class.lower()
        mn = profile.mnemonic.upper()
        dst = regs[0] if regs else "Xd"
        s1 = regs[1] if len(regs) > 1 else "Xn"
        s2 = regs[2] if len(regs) > 2 else "Xm"

        if "add" in mn.lower() or mn in ("ADD", "ADDS"):
            return f"{dst} = {s1} + {s2}"
        elif "sub" in mn.lower() or mn in ("SUB", "SUBS", "NEG"):
            return f"{dst} = {s1} - {s2}"
        elif "mul" in mn.lower() or "MUL" in mn:
            return f"{dst} = {s1} * {s2}"
        elif "and" in mn.lower() or "AND" in mn:
            return f"{dst} = {s1} & {s2}"
        elif "orr" in mn.lower() or "ORR" in mn:
            return f"{dst} = {s1} | {s2}"
        elif "eor" in mn.lower() or "EOR" in mn:
            return f"{dst} = {s1} ^ {s2}"
        elif "lsl" in mn.lower() or "LSL" in mn:
            return f"{dst} = {s1} << {s2}"
        elif "lsr" in mn.lower() or "LSR" in mn:
            return f"{dst} = {s1} >> {s2}"
        elif "mov" in mn.lower() or "MOV" in mn:
            return f"{dst} = {s1}"
        elif "ldr" in mn.lower() or "LDR" in mn:
            return f"Mem[{s1} + offset]"
        elif "str" in mn.lower() or "STR" in mn:
            return f"Mem[{s1} + offset] = {s2}"
        elif "cmp" in mn.lower() or "CMN" in mn:
            return f"Flags = {s1} {'+' if 'CMN' in mn else '-'} {s2}"
        return f"{dst} = f({s1}, {s2})  // TODO: implement ARM reference model"


# ═══════════════════════════════════════════════════════════════
# 5. Boundary Test Generator
# ═══════════════════════════════════════════════════════════════

class BoundaryTestGenerator:
    """Generate boundary / corner value test cases."""

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def generate(
        self,
        profile: InstructionProfile,
        use_llm: bool = False,
    ) -> list[BoundaryTestCase]:
        """Generate boundary test cases."""
        if use_llm and self._llm:
            return self._generate_with_llm(profile)
        return self._generate_rule_based(profile)

    def _generate_rule_based(self, profile: InstructionProfile) -> list[BoundaryTestCase]:
        """Rule-based boundary test generation."""
        tests: list[BoundaryTestCase] = []
        mnemonic = profile.mnemonic.lower()
        is_64bit = profile.has_64bit_encoding
        reg_prefix = "X" if is_64bit else "W"

        # For each immediate field, generate min/max/zero/overflow
        for imm_range in profile.immediate_ranges:
            sym = imm_range.operand_symbol.strip("<>")
            max_val = imm_range.max_value
            bit_w = imm_range.bit_width

            # 0. Zero immediate
            tests.append(BoundaryTestCase(
                test_name=f"test_{mnemonic}_{sym}_zero",
                category="zero",
                instruction=f"{mnemonic} {reg_prefix}0, {reg_prefix}1, #0",
                boundary_value=f"{sym}=0 (zero value)",
                input_state={f"{reg_prefix}1": "0x10"},
                expected_state={f"{reg_prefix}0": "0x10"},
                expected_behavior="Zero immediate value processed correctly",
                risk_assessment="Zero is a special case in encoding",
            ))

            # 1. Max immediate
            tests.append(BoundaryTestCase(
                test_name=f"test_{mnemonic}_{sym}_max",
                category="max_immediate",
                instruction=f"{mnemonic} {reg_prefix}0, {reg_prefix}1, #{max_val}",
                boundary_value=f"{sym}={max_val} (max {bit_w}-bit)",
                input_state={f"{reg_prefix}1": "0x0"},
                expected_state={f"{reg_prefix}0": f"0x{max_val:x}"},
                expected_behavior=f"Maximum {bit_w}-bit value ({max_val}) processed correctly",
                risk_assessment=f"Verifies that the full {bit_w}-bit immediate range is usable",
            ))

            # 2. Min immediate
            tests.append(BoundaryTestCase(
                test_name=f"test_{mnemonic}_{sym}_min",
                category="min_immediate",
                instruction=f"{mnemonic} {reg_prefix}0, {reg_prefix}1, #0",
                boundary_value=f"{sym}=0 (min value)",
                input_state={f"{reg_prefix}1": "0x10"},
                expected_state={f"{reg_prefix}0": "0x10"},
                expected_behavior="Zero immediate value processed correctly",
                risk_assessment="Zero is often a special case in encoding",
            ))

            # 3. Overflow (just beyond range, if safe)
            overflow_val = max_val + 1
            safe = overflow_val <= (1 << bit_w)
            if not safe:
                tests.append(BoundaryTestCase(
                    test_name=f"test_{mnemonic}_{sym}_overflow",
                    category="overflow",
                    instruction=f"{mnemonic} {reg_prefix}0, {reg_prefix}1, #{overflow_val}",
                    boundary_value=f"{sym}={overflow_val} (> max {bit_w}-bit)",
                    input_state={f"{reg_prefix}1": "0x0"},
                    expected_behavior="CONSTRAINED_UNPREDICTABLE or assembler error",
                    risk_assessment=f"Value {overflow_val} exceeds {bit_w}-bit immediate range",
                ))

        # Register edge cases
        if profile.gp_register_count >= 2:
            # Zero register destination
            if profile.has_special_register:
                zr = "XZR" if is_64bit else "WZR"
                tests.append(BoundaryTestCase(
                    test_name=f"test_{mnemonic}_zero_reg",
                    category="zero",
                    instruction=f"{mnemonic} {zr}, {reg_prefix}1, {reg_prefix}2",
                    boundary_value=f"destination={zr} (zero register)",
                    input_state={f"{reg_prefix}1": "0x10", f"{reg_prefix}2": "0x20"},
                    expected_behavior="Result discarded to zero register, flags may be set",
                    risk_assessment="Zero register destination discards result",
                ))

                # Also keep a register_edge variant for src/dst overlap
                r0 = _select_register(0, is_64bit, True)
                r1 = _select_register(1, is_64bit, True)
                tests.append(BoundaryTestCase(
                    test_name=f"test_{mnemonic}_src_dst_overlap",
                    category="register_edge",
                    instruction=f"{mnemonic} {r0}, {r0}, {r1}",
                    boundary_value=f"source={r0} also used as destination",
                    input_state={f"{r0}": "0x5", f"{r1}": "0x3"},
                    expected_state={f"{r0}": "0x8"},
                    expected_behavior="Source/dest overlap: result computed correctly before overwrite",
                    risk_assessment="Register overlap may cause intermediate value corruption in some implementations",
                ))
            else:
                # Source = dest (register overlap) for non-special-register cases
                r0 = _select_register(0, is_64bit, True)
                r1 = _select_register(1, is_64bit, True)
                tests.append(BoundaryTestCase(
                    test_name=f"test_{mnemonic}_src_dst_overlap",
                    category="register_edge",
                    instruction=f"{mnemonic} {r0}, {r0}, {r1}",
                    boundary_value=f"source={r0} also used as destination",
                    input_state={f"{r0}": "0x5", f"{r1}": "0x3"},
                    expected_state={f"{r0}": "0x8"},
                    expected_behavior="Source/dest overlap: result computed correctly before overwrite",
                    risk_assessment="Register overlap may cause intermediate value corruption in some implementations",
                ))

        # Width boundary (32/64 bit)
        if profile.has_32bit_encoding and profile.has_64bit_encoding:
            # 32-bit
            tests.append(BoundaryTestCase(
                test_name=f"test_{mnemonic}_w_reg_32bit",
                category="width_boundary",
                instruction=f"{mnemonic} W0, W1, W2",
                boundary_value="32-bit width (W registers)",
                input_state={"W1": "0xFFFFFFFF", "W2": "0x1"},
                expected_state={"W0": "0x0"},
                expected_behavior="32-bit ADD with overflow: 0xFFFFFFFF + 0x1 = 0x0 (wraps in 32-bit)",
                risk_assessment="32-bit overflow must wrap to 0 (modulo 2^32)",
            ))
            # 64-bit
            tests.append(BoundaryTestCase(
                test_name=f"test_{mnemonic}_x_reg_64bit",
                category="width_boundary",
                instruction=f"{mnemonic} X0, X1, X2",
                boundary_value="64-bit width (X registers)",
                input_state={"X1": "0xFFFFFFFF", "X2": "0x1"},
                expected_state={"X0": "0x100000000"},
                expected_behavior="64-bit ADD: 0xFFFFFFFF + 0x1 = 0x100000000 (no wrap)",
                risk_assessment="64-bit result must preserve full width",
            ))

        return tests

    def _generate_with_llm(self, profile: InstructionProfile) -> list[BoundaryTestCase]:
        """LLM-assisted boundary test generation."""
        ctx = format_profile_context(profile)
        result = _safe_llm_invoke(
            self._llm,
            BOUNDARY_TEST_PROMPT_TEMPLATE,
            f"Generate boundary tests for:\n\n{ctx}",
        )
        data = _parse_json_response(result, [])
        return [BoundaryTestCase(**item) for item in data]


# ═══════════════════════════════════════════════════════════════
# 6. Alias Test Generator
# ═══════════════════════════════════════════════════════════════

class AliasTestGenerator:
    """Generate alias ↔ canonical equivalence tests."""

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def generate(
        self,
        profile: InstructionProfile,
        use_llm: bool = False,
    ) -> list[AliasTestCase]:
        """Generate alias tests."""
        # If this IS an alias, generate tests comparing with canonical
        if profile.is_alias and profile.alias_of:
            return self._generate_for_alias(profile)

        # If this instruction appears in our known alias map (it IS the canonical)
        mnemonic_upper = profile.mnemonic.upper()
        if mnemonic_upper in _KNOWN_ALIASES:
            # This is a canonical instruction that has known aliases.
            # Normally alias tests are generated from the alias side.
            # But we might want to generate tests for its aliases too.
            pass

        # Try LLM if requested
        if use_llm and self._llm:
            return self._generate_with_llm(profile)

        return []

    def _generate_for_alias(self, profile: InstructionProfile) -> list[AliasTestCase]:
        """Generate equivalence tests when profile IS an alias."""
        alias_mnemonic = profile.mnemonic.upper()
        canonical_mnemonic = profile.alias_of.upper() if profile.alias_of else ""

        # Check known aliases
        alias_info = _KNOWN_ALIASES.get(alias_mnemonic)
        if alias_info:
            canon, canon_template, rationale = alias_info
        else:
            canon = canonical_mnemonic or "UNKNOWN"
            canon_template = f"{canon} Xd, Xn, Xm"
            rationale = f"{alias_mnemonic} is an alias of {canon}"

        is_64bit = profile.has_64bit_encoding
        dst = _select_register(0, is_64bit, True)
        src = _select_register(1, is_64bit, True)

        # Build alias and canonical instructions
        alias_inst = self._build_alias_instruction(alias_mnemonic, profile, dst, src, is_64bit)
        canon_inst = self._build_canonical_instruction(alias_mnemonic, canon_template, dst, src)

        return [AliasTestCase(
            test_name=f"test_{alias_mnemonic.lower()}_alias_equivalence",
            alias_mnemonic=alias_mnemonic,
            canonical_mnemonic=canon,
            alias_instruction=alias_inst,
            canonical_instruction=canon_inst,
            input_state={src: "0xDEADBEEFCAFE"},
            expected_state={dst: "0xDEADBEEFCAFE"},
            behavior_equivalence=rationale,
        )]

    def _generate_with_llm(self, profile: InstructionProfile) -> list[AliasTestCase]:
        """LLM-assisted alias test generation."""
        ctx = format_profile_context(profile)
        result = _safe_llm_invoke(
            self._llm,
            ALIAS_TEST_PROMPT_TEMPLATE,
            f"Generate alias tests for:\n\n{ctx}",
        )
        data = _parse_json_response(result, [])
        return [AliasTestCase(**item) for item in data]

    @staticmethod
    def _build_alias_instruction(
        mnemonic: str,
        profile: InstructionProfile,
        dst: str,
        src: str,
        is_64bit: bool,
    ) -> str:
        """Build a concrete alias instruction string."""
        if mnemonic == "MOV":
            return f"MOV {dst}, {src}"
        elif mnemonic == "CMP":
            return f"CMP {src}, #0"
        elif mnemonic == "NEG":
            return f"NEG {dst}, {src}"
        elif mnemonic == "TST":
            return f"TST {src}, #1"
        elif mnemonic == "MVN":
            return f"MVN {dst}, {src}"
        # Fallback: use template
        if profile.encodings:
            template = profile.encodings[0].assembly_template
            template = template.replace("<Xd>", dst).replace("<Xn>", src).replace("<Xm>", src)
            return template
        return f"{mnemonic.lower()} {dst}, {src}"

    @staticmethod
    def _build_canonical_instruction(
        alias: str,
        canon_template: str,
        dst: str,
        src: str,
    ) -> str:
        """Build concrete canonical instruction from alias."""
        return canon_template.replace("{dst}", dst).replace("{src}", src).replace(
            "{src1}", dst
        ).replace("{src2}", src)


# ═══════════════════════════════════════════════════════════════
# 7. Invalid Operand Test Generator
# ═══════════════════════════════════════════════════════════════

class InvalidOperandGenerator:
    """Generate tests for invalid/illegal operand combinations."""

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def generate(
        self,
        profile: InstructionProfile,
        use_llm: bool = False,
    ) -> list[InvalidOperandTestCase]:
        """Generate invalid operand tests."""
        if use_llm and self._llm:
            return self._generate_with_llm(profile)
        return self._generate_rule_based(profile)

    def _generate_rule_based(self, profile: InstructionProfile) -> list[InvalidOperandTestCase]:
        """Rule-based invalid operand test generation."""
        tests: list[InvalidOperandTestCase] = []
        mnemonic = profile.mnemonic.lower()

        # Category from ENCODING_UNDEF
        for eu in profile.encoding_undefined:
            tests.append(InvalidOperandTestCase(
                test_name=f"test_{mnemonic}_undef_encoding",
                instruction=f"{mnemonic} X0, X1, X2",
                invalid_aspect="reserved_bits",
                constraint_source="ENCODING_UNDEF",
                constraint_condition=eu.condition or "encoding undefined",
                expected_outcome="UNDEFINED",
                rationale=f"Encoding undefined condition: {eu.description[:100]}",
                is_safe_to_test=False,
            ))

        # Category 1: Immediate range violations
        for imm_range in profile.immediate_ranges:
            overflow_val = imm_range.max_value + 1
            tests.append(InvalidOperandTestCase(
                test_name=f"test_{mnemonic}_imm_overflow_{imm_range.encoded_field}",
                instruction=f"{mnemonic} X0, X1, #{overflow_val}",
                invalid_aspect="immediate_range",
                constraint_source="ENCODING_UNDEF" if overflow_val > (1 << (imm_range.bit_width + 1)) else "CONSTRAINED_UNPREDICTABLE",
                constraint_condition=f"{imm_range.encoded_field} > {imm_range.max_value}",
                expected_outcome="CONSTRAINED_UNPREDICTABLE",
                rationale=f"Immediate value {overflow_val} exceeds {imm_range.bit_width}-bit field max {imm_range.max_value}",
                is_safe_to_test=False,
            ))

        # Category 2: Register combination violations from CONSTRAINED_UNPREDICTABLE
        for cu in profile.constrained_unpredictable:
            condition = cu.condition or ""
            desc = cu.description or ""

            # Register overlap case
            if any(kw in condition.lower() for kw in ["same reg", "overlap", "identical"]):
                is_64bit = profile.has_64bit_encoding
                r = _select_register(0, is_64bit, True)
                reg_ops = [op for op in profile.operands if op.operand_type == "register"]
                n_regs = len(reg_ops)
                if n_regs >= 2:
                    bad_inst = f"{mnemonic} {r}, {r}, {r}"
                else:
                    bad_inst = f"{mnemonic} {r}, {r}"

                tests.append(InvalidOperandTestCase(
                    test_name=f"test_{mnemonic}_reg_overlap",
                    instruction=bad_inst,
                    invalid_aspect="register_combination",
                    constraint_source="CONSTRAINED_UNPREDICTABLE",
                    constraint_condition=condition,
                    expected_outcome="CONSTRAINED_UNPREDICTABLE",
                    rationale=f"Same register used as source and destination: {desc}",
                    is_safe_to_test=True,
                ))

            # SP restriction
            if "sp" in condition.lower() or "SP" in condition:
                is_64bit = profile.has_64bit_encoding
                bad_inst = f"{mnemonic} SP, X1, X2"
                tests.append(InvalidOperandTestCase(
                    test_name=f"test_{mnemonic}_sp_violation",
                    instruction=bad_inst,
                    invalid_aspect="register_combination",
                    constraint_source="CONSTRAINED_UNPREDICTABLE",
                    constraint_condition=condition,
                    expected_outcome="CONSTRAINED_UNPREDICTABLE",
                    rationale=f"SP used in restricted position: {desc}",
                    is_safe_to_test=False,
                ))

        # Category 3: Feature missing (if this instruction has feature deps)
        if profile.feature_dependencies:
            for fd in profile.feature_dependencies[:2]:
                is_64bit = profile.has_64bit_encoding
                dst = _select_register(0, is_64bit, True)
                src = _select_register(1, is_64bit, True)
                tests.append(InvalidOperandTestCase(
                    test_name=f"test_{mnemonic}_feature_{fd.feature_name.lower()}_missing",
                    instruction=f"{mnemonic} {dst}, {src}",
                    invalid_aspect="feature_missing",
                    constraint_source="FEATURE_GATE",
                    constraint_condition=f"{fd.feature_name} not enabled",
                    expected_outcome="UNDEFINED",
                    rationale=f"Instruction requires {fd.feature_name} which is not enabled",
                    is_safe_to_test=False,
                ))

        # Category 4: Alignment violation (for load/store instructions)
        cls_lower = profile.instr_class.lower()
        if "load" in cls_lower or "store" in cls_lower or "ld" in mnemonic or "st" in mnemonic:
            # Misaligned access
            bad_inst = f"{mnemonic} X0, [X1, #1]"
            tests.append(InvalidOperandTestCase(
                test_name=f"test_{mnemonic}_unaligned",
                instruction=bad_inst,
                invalid_aspect="alignment_violation",
                constraint_source="CONSTRAINED_UNPREDICTABLE",
                constraint_condition="address not aligned to access size",
                expected_outcome="CONSTRAINED_UNPREDICTABLE",
                rationale=f"Non-naturally-aligned address for {mnemonic}",
                is_safe_to_test=False,
            ))

        return tests

    def _generate_with_llm(self, profile: InstructionProfile) -> list[InvalidOperandTestCase]:
        """LLM-assisted invalid operand test generation."""
        ctx = format_profile_context(profile)
        result = _safe_llm_invoke(
            self._llm,
            INVALID_OPERAND_PROMPT_TEMPLATE,
            f"Generate invalid operand tests for:\n\n{ctx}",
        )
        data = _parse_json_response(result, [])
        return [InvalidOperandTestCase(**item) for item in data]


# ═══════════════════════════════════════════════════════════════
# 8. Feature Enable Test Generator
# ═══════════════════════════════════════════════════════════════

class FeatureEnableGenerator:
    """Generate tests verifying instruction availability behind feature flags."""

    # Map feature names to architecture versions and flags
    _FEATURE_MAP: dict[str, tuple[str, str]] = {
        "FEAT_SVE": ("ARMv8.2", "-march=armv8.2-a+sve"),
        "FEAT_SVE2": ("ARMv9.0", "-march=armv9.0-a+sve2"),
        "FEAT_FP": ("ARMv8.0", "-march=armv8.0-a"),
        "FEAT_FP16": ("ARMv8.2", "-march=armv8.2-a+fp16"),
        "FEAT_SIMD": ("ARMv8.0", "-march=armv8.0-a"),
        "FEAT_LSE": ("ARMv8.1", "-march=armv8.1-a+lse"),
        "FEAT_RDM": ("ARMv8.1", "-march=armv8.1-a+rdm"),
        "FEAT_DotProd": ("ARMv8.2", "-march=armv8.2-a+dotprod"),
        "FEAT_SHA3": ("ARMv8.2", "-march=armv8.2-a+sha3"),
        "FEAT_SM4": ("ARMv8.2", "-march=armv8.2-a+sm4"),
        "FEAT_MTE": ("ARMv8.5", "-march=armv8.5-a+mte"),
        "FEAT_BTI": ("ARMv8.5", "-march=armv8.5-a"),
        "FEAT_PAuth": ("ARMv8.3", "-march=armv8.3-a"),
        "FEAT_RNG": ("ARMv8.5", "-march=armv8.5-a+rng"),
        "FEAT_TME": ("ARMv9.0", "-march=armv9.0-a+tme"),
        "FEAT_BF16": ("ARMv8.2", "-march=armv8.2-a+bf16"),
        "FEAT_I8MM": ("ARMv8.2", "-march=armv8.2-a+i8mm"),
        "FEAT_F32MM": ("ARMv8.2", "-march=armv8.2-a+f32mm"),
        "FEAT_F64MM": ("ARMv8.2", "-march=armv8.2-a+f64mm"),
        "FEAT_FlagM": ("ARMv8.0", "-march=armv8.0-a+flagm"),
        "FEAT_FlagM2": ("ARMv9.0", "-march=armv9.0-a+flagm2"),
        "FEAT_PAN": ("ARMv8.1", "-march=armv8.1-a"),
        "FEAT_LOR": ("ARMv8.1", "-march=armv8.1-a"),
        "FEAT_RAS": ("ARMv8.0", "-march=armv8.0-a+ras"),
        "FEAT_CRC32": ("ARMv8.0", "-march=armv8.0-a+crc"),
        "FEAT_CSV2": ("ARMv8.0", "-march=armv8.0-a"),
        "FEAT_SB": ("ARMv8.0", "-march=armv8.0-a+sb"),
        "FEAT_SSBS": ("ARMv8.0", "-march=armv8.0-a+ssbs"),
    }

    def __init__(self, llm: Any = None) -> None:
        self._llm = llm

    def generate(
        self,
        profile: InstructionProfile,
        use_llm: bool = False,
    ) -> list[FeatureEnableTestCase]:
        """Generate feature enable tests."""
        if not profile.feature_dependencies:
            return []

        if use_llm and self._llm:
            return self._generate_with_llm(profile)
        return self._generate_rule_based(profile)

    def _generate_rule_based(self, profile: InstructionProfile) -> list[FeatureEnableTestCase]:
        """Rule-based feature enable test generation."""
        tests: list[FeatureEnableTestCase] = []
        mnemonic = profile.mnemonic.lower()

        for fd in profile.feature_dependencies:
            feat_name = fd.feature_name
            arch_info = self._FEATURE_MAP.get(feat_name)
            if arch_info:
                arch_ver, enable_flag = arch_info
            else:
                arch_ver = fd.display_name or "ARMv8.0"
                enable_flag = f"-march={arch_ver.lower()}"

            # Build a concrete assembly instruction for testing
            is_64bit = profile.has_64bit_encoding
            dst = _select_register(0, is_64bit, True)
            src = _select_register(1, is_64bit, True)

            if profile.encodings:
                asm = f"{mnemonic} {dst}, {src}"
            else:
                asm = f"{mnemonic} {dst}, {src}"

            feature_slug = feat_name.lower().replace("_", "-")
            expected_error = f"error: instruction requires: {feature_slug}"

            tests.append(FeatureEnableTestCase(
                test_name=f"test_{mnemonic}_{feat_name.lower()}",
                instruction=asm,
                feature_name=feat_name,
                feature_description=fd.display_name or feat_name,
                architecture_version=arch_ver,
                enable_flag=enable_flag,
                test_without_feature=True,
                assembly_lines=[f"\t{asm}"],
                check_lines=[f"// CHECK: {asm}"],
                error_check_lines=[f"// CHECK: {expected_error}"],
                expected_error=expected_error,
            ))

        return tests

    def _generate_with_llm(self, profile: InstructionProfile) -> list[FeatureEnableTestCase]:
        """LLM-assisted feature enable test generation."""
        ctx = format_profile_context(profile)
        result = _safe_llm_invoke(
            self._llm,
            FEATURE_ENABLE_PROMPT_TEMPLATE,
            f"Generate feature enable tests for:\n\n{ctx}",
        )
        data = _parse_json_response(result, [])
        return [FeatureEnableTestCase(**item) for item in data]


# ═══════════════════════════════════════════════════════════════
# TestCaseSuiteGenerator — orchestrates all 8 generators
# ═══════════════════════════════════════════════════════════════

class TestCaseSuiteGenerator:
    """Master orchestrator that runs all 8 generators and assembles a TestCaseSuite."""

    def __init__(self, llm: Any = None, sqlite_client: Any = None) -> None:
        self._llm = llm
        self._sqlite = sqlite_client
        # Sub-generators
        self.assembly_gen = ARMAssemblyTestGenerator(llm)
        self.llvm_mc_gen = LLVMMCTestGenerator(llm)
        self.inline_asm_gen = InlineAsmTestGenerator(llm)
        self.cpp_verify_gen = CppVerificationGenerator(llm)
        self.boundary_gen = BoundaryTestGenerator(llm)
        self.alias_gen = AliasTestGenerator(llm)
        self.invalid_gen = InvalidOperandGenerator(llm)
        self.feature_gen = FeatureEnableGenerator(llm)

    def generate_suite(
        self,
        profile: InstructionProfile,
        use_llm: bool = False,
        test_types: Optional[list[str]] = None,
        instruction_count: int = 100,
    ) -> TestCaseSuite:
        """Generate a complete test suite for an instruction.

        Args:
            profile: Instruction metadata profile.
            use_llm: If True, use LLM-assisted generation.
            test_types: Optional whitelist of test types to generate.
                       None or empty means all.
                       Valid values: assembly, llvm_mc, inline_asm, cpp_verify,
                                     boundary, alias, invalid_operand, feature_enable.
            instruction_count: Target number of instruction instances per test program.
                              The count is divided proportionally among test types.

        Returns:
            TestCaseSuite with all generated test cases.
        """
        all_types = test_types or [
            "assembly", "llvm_mc", "inline_asm", "cpp_verify",
            "boundary", "alias", "invalid_operand", "feature_enable",
        ]
        all_types_set = set(all_types)

        # Scale per-generator count proportionally from instruction_count
        per_type_count = max(1, instruction_count // len(all_types))

        suite = TestCaseSuite(
            instruction_mnemonic=profile.mnemonic,
            instruction_xml_id=profile.xml_id,
            generation_mode="llm_assisted" if use_llm else "rule_based",
        )

        warnings: list[str] = []

        # 1. Assembly tests
        if "assembly" in all_types_set:
            try:
                suite.assembly_tests = self.assembly_gen.generate(profile, use_llm, count=per_type_count)
            except Exception as e:
                warnings.append(f"assembly: {e}")

        # 2. LLVM MC tests
        if "llvm_mc" in all_types_set:
            try:
                suite.llvm_mc_tests = self.llvm_mc_gen.generate(profile, use_llm)
            except Exception as e:
                warnings.append(f"llvm_mc: {e}")

        # 3. Inline asm tests
        if "inline_asm" in all_types_set:
            try:
                suite.inline_asm_tests = self.inline_asm_gen.generate(profile, use_llm, count=per_type_count)
            except Exception as e:
                warnings.append(f"inline_asm: {e}")

        # 4. C++ verification
        if "cpp_verify" in all_types_set:
            try:
                suite.cpp_verification_tests = self.cpp_verify_gen.generate(profile, use_llm)
            except Exception as e:
                warnings.append(f"cpp_verify: {e}")

        # 5. Boundary tests
        if "boundary" in all_types_set:
            try:
                suite.boundary_tests = self.boundary_gen.generate(profile, use_llm)
            except Exception as e:
                warnings.append(f"boundary: {e}")

        # 6. Alias tests
        if "alias" in all_types_set and (profile.is_alias or profile.mnemonic.upper() in _KNOWN_ALIASES):
            try:
                suite.alias_tests = self.alias_gen.generate(profile, use_llm)
            except Exception as e:
                warnings.append(f"alias: {e}")

        # 7. Invalid operand tests
        if "invalid_operand" in all_types_set:
            try:
                suite.invalid_operand_tests = self.invalid_gen.generate(profile, use_llm)
            except Exception as e:
                warnings.append(f"invalid_operand: {e}")

        # 8. Feature enable tests
        if "feature_enable" in all_types_set and profile.feature_dependencies:
            try:
                suite.feature_enable_tests = self.feature_gen.generate(profile, use_llm)
            except Exception as e:
                warnings.append(f"feature_enable: {e}")

        suite.total_test_count = suite.total_tests
        suite.generation_warnings = warnings
        return suite

    def generate_multi_instruction(
        self,
        profiles: list[InstructionProfile],
        use_llm: bool = False,
        instruction_count: int = 100,
    ) -> TestCaseSuite:
        """Generate a combined test suite spanning multiple instruction profiles.

        Each profile's share of *instruction_count* is generated independently;
        results from all profiles are merged into a single TestCaseSuite.

        Args:
            profiles: One InstructionProfile per instruction in the scenario.
            use_llm: If True, use LLM-assisted generation.
            instruction_count: Total target instruction instances across the
                              merged test program.

        Returns:
            A single TestCaseSuite that aggregates all generated test cases.
        """
        num_profiles = max(1, len(profiles))
        per_ins_count = max(1, instruction_count // num_profiles)

        # Use the first profile as the suite identity
        primary = profiles[0]
        suite = TestCaseSuite(
            instruction_mnemonic=",".join(p.mnemonic for p in profiles),
            instruction_xml_id=primary.xml_id,
            generation_mode=use_llm and "llm_assisted" or "rule_based",
        )
        all_warnings: list[str] = []

        for profile in profiles:
            sub = self.generate_suite(profile, use_llm=use_llm, instruction_count=per_ins_count)
            # Merge fields from sub into suite
            if sub.assembly_tests:
                suite.assembly_tests.extend(sub.assembly_tests)
            if sub.llvm_mc_tests:
                suite.llvm_mc_tests.extend(sub.llvm_mc_tests)
            if sub.inline_asm_tests:
                suite.inline_asm_tests.extend(sub.inline_asm_tests)
            if sub.cpp_verification_tests:
                suite.cpp_verification_tests.extend(sub.cpp_verification_tests)
            if sub.boundary_tests:
                suite.boundary_tests.extend(sub.boundary_tests)
            if sub.alias_tests:
                suite.alias_tests.extend(sub.alias_tests)
            if sub.invalid_operand_tests:
                suite.invalid_operand_tests.extend(sub.invalid_operand_tests)
            if sub.feature_enable_tests:
                suite.feature_enable_tests.extend(sub.feature_enable_tests)
            all_warnings.extend(sub.generation_warnings or [])

        suite.total_test_count = suite.total_tests
        suite.generation_warnings = all_warnings
        return suite
