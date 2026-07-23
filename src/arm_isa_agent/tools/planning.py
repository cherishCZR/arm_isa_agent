"""Planning tools — instruction test planning and strategy generation.

These tools provide the Instruction Planning capability:
- plan_instruction_tests: Generate a comprehensive test plan for an ARM instruction
- analyze_instruction_profile: Quick profile analysis without full plan generation
"""

from __future__ import annotations

import json

import structlog

from arm_isa_agent.agent.tool_registry import get_llm, get_sqlite, register_tool
from arm_isa_agent.planning.planner import InstructionPlanner

logger = structlog.get_logger(__name__)


# ── plan_instruction_tests ──────────────────────────────────────

@register_tool(
    "plan_instruction_tests",
    "Generate a comprehensive test plan for an ARM instruction. "
    "Analyzes instruction metadata (encodings, operands, constraints, features, "
    "immediate ranges, register usage) and produces a structured test strategy "
    "covering Normal operations, Boundary values, Register constraints, "
    "Encoding variants, CONSTRAINED_UNPREDICTABLE conditions, and more. "
    "Use this when the user asks for test planning, test strategy, "
    "\"how to test X\", or systematic verification planning.",
)
def plan_instruction_tests(
    mnemonic_or_xml_id: str,
    user_goal: str = "",
    use_llm: bool = True,
) -> str:
    """Generate a structured test plan for an ARM instruction.

    Args:
        mnemonic_or_xml_id: Instruction mnemonic (e.g. "ADD") or XML ID
            (e.g. "ADD_shifted_imm") for precise identification.
        user_goal: Optional user goal description for context
            (e.g. "Generate comprehensive tests for SVE load instructions").
        use_llm: Whether to use LLM for strategy refinement (True) or
            rule-based only (False).

    Returns:
        Markdown-formatted test plan with:
          - Instruction profile (metadata, encodings, operands)
          - Test strategy with prioritized dimensions
          - Key edge cases and risks
          - Recommended test scenarios
    """
    try:
        sqlite = get_sqlite()
        llm = get_llm()

        planner = InstructionPlanner(sqlite_client=sqlite, llm=llm)

        # Determine if input looks like an xml_id (contains underscore)
        # or a mnemonic (plain word)
        mnemonic = ""
        xml_id = ""
        if "_" in mnemonic_or_xml_id or "/" in mnemonic_or_xml_id:
            xml_id = mnemonic_or_xml_id
        else:
            mnemonic = mnemonic_or_xml_id

        result = planner.plan(
            mnemonic=mnemonic,
            xml_id=xml_id,
            user_goal=user_goal,
            use_llm=use_llm,
        )

        if result["status"] == "not_found":
            return json.dumps({
                "status": "not_found",
                "query": mnemonic_or_xml_id,
                "message": result.get("message", "Instruction not found"),
                "suggestion": "Try using retrieve_instruction to find the correct instruction first.",
            }, ensure_ascii=False)

        if result["status"] == "error":
            return json.dumps({
                "status": "error",
                "query": mnemonic_or_xml_id,
                "error": result.get("error", "Unknown error"),
            }, ensure_ascii=False)

        # Return the markdown plan as the main content
        return result.get("plan_markdown", "Plan generation succeeded but no summary was produced.")

    except Exception as e:
        logger.error("plan_instruction_tests.error", error=str(e)[:200])
        return json.dumps({
            "error": f"Test planning failed: {str(e)[:300]}",
            "hint": "Ensure the SQLite knowledge base is populated and the instruction exists.",
        }, ensure_ascii=False)


# ── analyze_instruction_profile ──────────────────────────────────

@register_tool(
    "analyze_instruction_profile",
    "Quick analysis of an ARM instruction's metadata profile. "
    "Extracts encodings, operands, immediate ranges, register constraints, "
    "feature dependencies, and constraints without generating a full test plan. "
    "Use for quick inspection or as a precursor to detailed planning.",
)
def analyze_instruction_profile(mnemonic_or_xml_id: str) -> str:
    """Analyze instruction metadata and return a structured profile.

    Args:
        mnemonic_or_xml_id: Instruction mnemonic (e.g. "ADD") or XML ID.

    Returns:
        JSON string with detailed instruction profile data.
    """
    try:
        sqlite = get_sqlite()
        from arm_isa_agent.planning.analyzer import InstructionAnalyzer

        analyzer = InstructionAnalyzer(sqlite_client=sqlite)

        mnemonic = ""
        xml_id = ""
        if "_" in mnemonic_or_xml_id or "/" in mnemonic_or_xml_id:
            xml_id = mnemonic_or_xml_id
        else:
            mnemonic = mnemonic_or_xml_id

        profile = analyzer.extract_profile(mnemonic=mnemonic, xml_id=xml_id)

        if profile is None:
            return json.dumps({
                "status": "not_found",
                "query": mnemonic_or_xml_id,
                "message": "Instruction not found in knowledge base.",
            }, ensure_ascii=False)

        from arm_isa_agent.planning.prompts import serialize_profile_to_json
        return json.dumps({
            "status": "ok",
            "profile": json.loads(serialize_profile_to_json(profile)),
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error("analyze_instruction_profile.error", error=str(e)[:200])
        return json.dumps({
            "error": f"Profile analysis failed: {str(e)[:300]}",
        }, ensure_ascii=False)
