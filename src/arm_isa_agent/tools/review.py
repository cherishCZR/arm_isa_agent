"""Review tool — validate and critique generated ARM assembly content."""

from __future__ import annotations

import json

import structlog
from langchain_core.messages import HumanMessage, SystemMessage

from arm_isa_agent.agent.tool_registry import get_llm, get_rag, get_sqlite, register_tool

logger = structlog.get_logger(__name__)


@register_tool(
    "review_result",
    "Review and critique generated ARM assembly, inline asm, or test cases for correctness. "
    "Cross-references against ISA specifications and encoding data. "
    "Use as the final quality-check step before delivering output to the user.",
)
def review_result(content: str, review_type: str = "assembly") -> str:
    """Review generated content against ISA specifications.

    Args:
        content: The generated content to review (assembly, inline asm, or test cases).
        review_type: Type of content: "assembly", "inline_asm", or "testcase".

    Returns:
        Review report with issues found, correctness assessment, and suggestions.
    """
    try:
        llm = get_llm()
        rag = get_rag()

        # Extract potential mnemonics from content for cross-reference
        import re
        mnemonics = list(set(re.findall(r'\b([A-Z][A-Z0-9]+)\b', content)))
        mnemonics = [m for m in mnemonics if len(m) >= 2 and m not in {
            "ASM", "C", "GCC", "CLANG", "ARM", "A64", "JSON", "XML",
            "SP", "PC", "XZR", "WZR", "NZCV", "LSL", "LSR", "ASR", "ROR",
            "UXTB", "UXTH", "UXTW", "SXTB", "SXTH", "SXTW", "SXTX",
        }]

        # Gather ISA context for detected mnemonics
        context_parts: list[str] = []
        for mnem in mnemonics[:5]:  # Limit to avoid overwhelming
            results = rag.search(mnem, top_k=2)
            for r in results.results:
                context_parts.append(f"## {r.metadata.get('mnemonic', mnem)} ({r.doc_id})")
                snippet = r.document[:600]
                # Extract encoding templates
                for line in snippet.split("\n"):
                    if "Assembly" in line or "Template" in line or "Encoding" in line:
                        context_parts.append(line.strip())
                context_parts.append("")

        context = "\n".join(context_parts) if context_parts else "No ISA context available for cross-reference."

        review_prompts = {
            "assembly": "assembly code (syntax, operands, flags, constraints)",
            "inline_asm": "C inline assembly (constraints, clobbers, operand modifiers, memory barriers)",
            "testcase": "test cases (coverage, edge cases, register state, expected behavior)",
        }
        review_focus = review_prompts.get(review_type, "generated content")

        system_msg = SystemMessage(content=f"""You are an ARM ISA review expert.
Critically review the following {review_focus}.

Check for:
1. **Syntax correctness**: valid ARM A64 syntax, proper operand formats
2. **Encoding accuracy**: operand types match instruction encoding requirements
3. **Constraint compliance**: no CONSTRAINED_UNPREDICTABLE violations
4. **Register usage**: correct register widths (W vs X), valid register numbers
5. **Architecture requirements**: correct feature flags mentioned (FEAT_*)
6. **Completeness**: all edge cases covered

Respond with a JSON review:
{{
  "overall_assessment": "correct" | "minor_issues" | "major_issues",
  "issues": [{{"severity": "error"|"warning"|"info", "description": "...", "suggestion": "..."}}],
  "correctness_score": 0-100,
  "summary": "brief overall assessment"
}}""")

        user_msg = HumanMessage(content=f"""ISA Reference Context:
{context[:2000]}

Content to review ({review_type}):
---
{content[:4000]}
---

Output ONLY the JSON review object.""")

        response = llm.invoke([system_msg, user_msg])
        return str(response.content)

    except Exception as e:
        logger.error("review_result.error", error=str(e)[:200])
        return json.dumps({"error": f"Review failed: {str(e)[:300]}"}, ensure_ascii=False)
