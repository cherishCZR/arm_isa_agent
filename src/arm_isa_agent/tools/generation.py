"""Generation tools — validate, generate, and create ARM assembly/test code."""

from __future__ import annotations

import json

import structlog
from langchain_core.messages import HumanMessage, SystemMessage

from arm_isa_agent.agent.tool_registry import get_llm, get_rag, get_sqlite, register_tool

logger = structlog.get_logger(__name__)


# ── validate_operand ────────────────────────────────────────────

@register_tool(
    "validate_operand",
    "Validate operand combinations for an ARM instruction against its defined encodings. "
    "Checks operand types, register widths, and compatibility. "
    "Use when the user asks 'is this valid?' or needs to verify operand usage.",
)
def validate_operand(mnemonic: str, operands: str) -> str:
    """Validate if given operands are compatible with the instruction's encodings.

    Args:
        mnemonic: ARM instruction mnemonic (e.g., "ADD", "LDR").
        operands: Operand string (e.g., "X0, X1, X2, LSL #3").

    Returns:
        Validation result with compatibility analysis.
    """
    try:
        sqlite = get_sqlite()
        llm = get_llm()

        # First, search for the instruction in SQLite
        from arm_isa_agent.kb.sqlite.models import InstructionModel

        with sqlite.session() as session:
            inst = session.query(InstructionModel).filter(
                InstructionModel.mnemonic.ilike(mnemonic)
            ).first()

            if inst is None:
                # Try RAG search as fallback
                rag = get_rag()
                results = rag.search(f"{mnemonic} {operands}", top_k=3)
                context = "\n".join([
                    f"- {r.metadata.get('mnemonic', '?')} ({r.doc_id}): {r.document[:300]}"
                    for r in results.results
                ])
            else:
                # Build context from instruction details
                enc_ctx = []
                for enc in inst.encodings:
                    enc_ctx.append(f"  Encoding: {enc.name} | Template: {enc.assembly_template}")
                op_ctx = []
                for op in inst.operands:
                    op_ctx.append(f"  {op.symbol}: {op.description} (type={op.operand_type}, reg_class={op.register_class})")

                context = f"""Instruction: {inst.mnemonic} ({inst.xml_id})
Class: {inst.instr_class}
Brief: {inst.brief}
Encodings:
{chr(10).join(enc_ctx)}
Operands:
{chr(10).join(op_ctx)}"""

            # Use LLM to validate
            system_msg = SystemMessage(content="""You are an ARM ISA validation expert.
Analyze whether the given operands are valid for the specified instruction.
Consider:
1. Operand count matches an encoding
2. Operand types (register/immediate/label) are compatible
3. Register widths (W vs X, B/H/S/D/Q) are correct
4. Shift/extend amounts are in range
5. Any CONSTRAINED_UNPREDICTABLE conditions

Respond with a JSON object:
{
  "valid": true/false,
  "matched_encoding": "encoding name or null",
  "issues": ["list of issues if any"],
  "suggestions": ["list of fixes if invalid"],
  "explanation": "detailed analysis"
}""")

            user_msg = HumanMessage(content=f"""Instruction context:
{context}

Validate: {mnemonic} {operands}

Output ONLY the JSON response.""")

            response = llm.invoke([system_msg, user_msg])
            return str(response.content)

    except Exception as e:
        logger.error("validate_operand.error", error=str(e)[:200])
        return json.dumps({"error": f"Validation failed: {str(e)[:300]}"}, ensure_ascii=False)


# ── generate_assembly ───────────────────────────────────────────

@register_tool(
    "generate_assembly",
    "Generate ARM A64 assembly code for a given instruction with specific operands. "
    "Grounds output in authoritative encoding data from the knowledge base. "
    "Use when the user needs to write or understand assembly snippets.",
)
def generate_assembly(mnemonic: str, operands: str, context_description: str = "") -> str:
    """Generate correct ARM A64 assembly using ISA encoding data.

    Args:
        mnemonic: ARM instruction mnemonic (e.g., "ADD", "STP").
        operands: Operand string (e.g., "X0, X1, X2").
        context_description: Optional description of the use case/context.

    Returns:
        Generated assembly with encoding information and explanation.
    """
    try:
        sqlite = get_sqlite()
        llm = get_llm()
        rag = get_rag()

        # Gather instruction context
        from arm_isa_agent.kb.sqlite.models import InstructionModel

        with sqlite.session() as session:
            inst = session.query(InstructionModel).filter(
                InstructionModel.mnemonic.ilike(mnemonic)
            ).first()

        context_parts: list[str] = []

        if inst:
            context_parts.append(f"## Instruction: {inst.mnemonic} ({inst.xml_id})")
            context_parts.append(f"Brief: {inst.brief}")
            context_parts.append(f"Class: {inst.instr_class}")
            context_parts.append("")

            for enc in inst.encodings:
                parts = [f"### Encoding: {enc.name}"]
                if enc.bitdiffs:
                    parts.append(f"Condition: {enc.bitdiffs}")
                parts.append(f"Template: {enc.assembly_template}")
                if enc.bit_pattern:
                    parts.append(f"Bit pattern: {enc.bit_pattern}")
                context_parts.extend(parts)

            context_parts.append("")
            context_parts.append("### Constraints:")
            for c in inst.constraints:
                context_parts.append(f"- [{c.constraint_type}] {c.condition}: {c.description}")
        else:
            # Fallback: RAG search
            results = rag.search(f"{mnemonic} {operands}", top_k=3)
            for r in results.results:
                context_parts.append(r.document[:800])
                context_parts.append("---")

        context = "\n".join(context_parts)

        system_msg = SystemMessage(content="""You are an ARM A64 assembly expert.
Generate correct ARM A64 assembly code based on the authoritative ISA data provided.
Include:
1. The assembly instruction(s) in a code block
2. Explanation of each operand
3. Any constraints or edge cases to be aware of
4. Architecture feature requirements (e.g., FEAT_FP required)
Use proper ARM assembly syntax (lowercase preferred, comma-separated operands).""")

        user_msg = HumanMessage(content=f"""ISA Reference Data:
{context[:3000]}

Use case: {context_description if context_description else 'General usage'}

Generate assembly for: {mnemonic} {operands}""")

        response = llm.invoke([system_msg, user_msg])
        return str(response.content)

    except Exception as e:
        logger.error("generate_assembly.error", error=str(e)[:200])
        return json.dumps({"error": f"Generation failed: {str(e)[:300]}"}, ensure_ascii=False)


# ── generate_inline_asm ─────────────────────────────────────────

@register_tool(
    "generate_inline_asm",
    "Generate C/C++ inline assembly (GCC/Clang style) for ARM A64 instructions. "
    "Includes proper clobber lists, input/output operands, and memory barriers. "
    "Use when embedding ARM assembly in C/C++ code.",
)
def generate_inline_asm(mnemonic: str, operands: str, compiler: str = "gcc") -> str:
    """Generate C inline assembly with proper GCC/Clang extended asm syntax.

    Args:
        mnemonic: ARM instruction mnemonic.
        operands: Operand string.
        compiler: Target compiler ("gcc" or "clang", default "gcc").

    Returns:
        C inline assembly code with operand constraints, clobbers, and explanation.
    """
    try:
        sqlite = get_sqlite()
        llm = get_llm()

        from arm_isa_agent.kb.sqlite.models import InstructionModel

        with sqlite.session() as session:
            inst = session.query(InstructionModel).filter(
                InstructionModel.mnemonic.ilike(mnemonic)
            ).first()

        context_parts: list[str] = []
        if inst:
            context_parts.append(f"Instruction: {inst.mnemonic} ({inst.xml_id})")
            context_parts.append(f"Brief: {inst.brief}")
            for enc in inst.encodings[:3]:
                context_parts.append(f"Encoding '{enc.name}': {enc.assembly_template}")
            for op in inst.operands:
                context_parts.append(f"Operand: {op.symbol} ({op.operand_type}, reg_class={op.register_class}, width={op.register_width})")

        context = "\n".join(context_parts) if context_parts else f"ARM instruction: {mnemonic} {operands}"

        system_msg = SystemMessage(content=f"""You are an expert in ARM A64 inline assembly for {compiler.upper()}.
Generate C inline assembly using extended asm syntax:
```c
asm volatile(
    "instruction %[out], %[in1], %[in2]"
    : [out] "=r" (output_var)     // output operands
    : [in1] "r" (input_var1)      // input operands
    : "cc", "memory"              // clobber list
);
```

Rules:
- Use "=r" for write-only register output, "+r" for read-write
- Use "r" for general-purpose register input (X0-X30)
- Use "w" for SIMD/FP registers (V0-V31)
- Always include "cc" in clobbers if flags are modified
- Include "memory" if memory is accessed
- Use %[name] syntax for named operands
- Add explanatory comments""")

        user_msg = HumanMessage(content=f"""ISA Context:
{context[:2000]}

Generate {compiler.upper()} inline assembly for: {mnemonic} {operands}

Provide a complete, compilable example function.""")

        response = llm.invoke([system_msg, user_msg])
        return str(response.content)

    except Exception as e:
        logger.error("generate_inline_asm.error", error=str(e)[:200])
        return json.dumps({"error": f"Inline asm generation failed: {str(e)[:300]}"}, ensure_ascii=False)


# ── generate_testcase ───────────────────────────────────────────

@register_tool(
    "generate_testcase",
    "Generate comprehensive test cases for an ARM instruction. "
    "Includes normal cases, edge cases, boundary conditions, and CONSTRAINED_UNPREDICTABLE scenarios. "
    "Use when the user needs to test or verify instruction behavior.",
)
def generate_testcase(mnemonic: str, test_count: int = 5) -> str:
    """Generate test cases covering normal and edge conditions.

    Args:
        mnemonic: ARM instruction mnemonic.
        test_count: Number of test cases to generate (default 5, max 10).

    Returns:
        Test case descriptions with assembly, expected behavior, and edge cases.
    """
    try:
        sqlite = get_sqlite()
        llm = get_llm()
        rag = get_rag()

        from arm_isa_agent.kb.sqlite.models import InstructionModel

        with sqlite.session() as session:
            inst = session.query(InstructionModel).filter(
                InstructionModel.mnemonic.ilike(mnemonic)
            ).first()

        context_parts: list[str] = []
        if inst:
            context_parts.append(f"Instruction: {inst.mnemonic} ({inst.xml_id})")
            context_parts.append(f"Brief: {inst.brief}")
            context_parts.append(f"Class: {inst.instr_class}")
            for enc in inst.encodings[:2]:
                context_parts.append(f"Encoding: {enc.name} | Template: {enc.assembly_template}")
                context_parts.append(f"Bitdiffs: {enc.bitdiffs}" if enc.bitdiffs else "")

            # Constraints for edge cases
            if inst.constraints:
                context_parts.append("Constraints (for edge case testing):")
                for c in inst.constraints[:5]:
                    context_parts.append(f"- [{c.constraint_type}] {c.condition}: {c.description}")

            # Operands for register info
            for op in inst.operands[:5]:
                context_parts.append(f"Operand {op.symbol}: {op.description} (type={op.operand_type})")
        else:
            results = rag.search(mnemonic, top_k=2)
            for r in results.results:
                context_parts.append(r.document[:600])

        context = "\n".join(p for p in context_parts if p)

        system_msg = SystemMessage(content=f"""You are an ARM ISA testing expert.
Generate {min(test_count, 10)} comprehensive test cases for the instruction.
For each test case provide:
1. Test name and scenario description
2. Input register/memory state
3. The assembly instruction
4. Expected output state
5. Any relevant flags (NZCV) changes

Cover these categories:
- **Normal case**: standard usage
- **Boundary values**: min/max immediate, zero register (XZR/WZR)
- **Special registers**: SP, PC usage if applicable
- **CONSTRAINED_UNPREDICTABLE**: edge cases from constraints
- **Architecture variants**: if multiple encodings exist

Format output as markdown with assembly in code blocks.""")

        user_msg = HumanMessage(content=f"""ISA Reference:
{context[:3000]}

Generate {min(test_count, 10)} test cases for: {mnemonic}""")

        response = llm.invoke([system_msg, user_msg])
        return str(response.content)

    except Exception as e:
        logger.error("generate_testcase.error", error=str(e)[:200])
        return json.dumps({"error": f"Testcase generation failed: {str(e)[:300]}"}, ensure_ascii=False)
