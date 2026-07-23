"""InstructionPlanner — LLM-powered test strategy generation for ARM instructions.

Orchestrates:
1. Instruction metadata extraction via InstructionAnalyzer
2. Rule-based test dimension recommendation
3. LLM-powered strategy generation
4. Structured PlanOutput synthesis

Usage:
    planner = InstructionPlanner(sqlite_client, llm)
    plan = planner.plan("ADD")
"""

from __future__ import annotations

import json
from typing import Any

import structlog
from langchain_core.messages import HumanMessage, SystemMessage

from arm_isa_agent.planning.analyzer import InstructionAnalyzer
from arm_isa_agent.planning.models import InstructionProfile, PlanOutput, TestDimension, TestStrategy
from arm_isa_agent.planning.prompts import (
    PLAN_SYNTHESIS_PROMPT,
    STRATEGY_SYSTEM_PROMPT,
    build_strategy_prompt,
    format_profile_context,
    serialize_profile_to_json,
)

logger = structlog.get_logger(__name__)


class InstructionPlanner:
    """Generates comprehensive test plans for ARM instructions.

    Combines static analysis (InstructionAnalyzer) with LLM reasoning
    to produce structured test strategies covering encoding variants,
    operand constraints, edge cases, and architecture dependencies.
    """

    def __init__(self, sqlite_client: Any = None, llm: Any = None) -> None:
        self._analyzer = InstructionAnalyzer(sqlite_client)
        self._llm = llm

    def set_services(self, sqlite_client: Any = None, llm: Any = None) -> None:
        if sqlite_client is not None:
            self._analyzer.set_sqlite(sqlite_client)
        if llm is not None:
            self._llm = llm

    # ── Public API ───────────────────────────────────────────

    def plan(
        self,
        mnemonic: str = "",
        xml_id: str = "",
        user_goal: str = "",
        use_llm: bool = True,
    ) -> dict[str, Any]:
        """Generate a complete test plan for the given instruction.

        Args:
            mnemonic: Instruction mnemonic (e.g. "ADD", "LDR").
            xml_id: Exact XML id for disambiguation (optional).
            user_goal: User's specific testing goal (e.g. "Generate tests for ADD").
            use_llm: Whether to use LLM for strategy refinement (True) or rules only (False).

        Returns:
            Dict with:
                - status: "ok" | "not_found" | "error"
                - profile: InstructionProfile
                - strategy: TestStrategy (JSON-ready)
                - plan_json: Full plan as JSON string
                - plan_markdown: Human-readable plan as markdown
        """
        try:
            # Step 1: Extract instruction profile
            profile = self._analyzer.extract_profile(mnemonic=mnemonic, xml_id=xml_id)
            if profile is None:
                return {
                    "status": "not_found",
                    "query": mnemonic or xml_id,
                    "message": f"No instruction found for '{mnemonic or xml_id}'. "
                               "Check the mnemonic or use retrieve_instruction to search.",
                }

            logger.info("planner.profile_built",
                        mnemonic=profile.mnemonic,
                        complexity=profile.complexity_score)

            # Step 2: Generate test dimensions (rule-based)
            rule_dims = InstructionAnalyzer.recommend_test_dimensions(profile)

            # Step 3: LLM strategy refinement (optional)
            if use_llm and self._llm is not None:
                strategy_dims, reasoning, risk, constraints_verify, total_count = \
                    self._generate_strategy_llm(profile, user_goal)
                # Merge: use LLM output if available, fall back to rules
                if strategy_dims:
                    final_dims = self._convert_dimensions(strategy_dims)
                else:
                    final_dims = self._convert_rule_dims(rule_dims)
                    reasoning = "Rule-based strategy (LLM strategy generation failed, using defaults)"
            else:
                final_dims = self._convert_rule_dims(rule_dims)
                reasoning = "Rule-based strategy (use_llm=False)"
                risk = self._rule_based_risk(profile)
                constraints_verify = [
                    c.description[:120] for c in profile.constrained_unpredictable[:3]
                ]
                total_count = self._estimate_total_tests(profile, len(final_dims))

            # Step 4: Build strategy
            strategy = TestStrategy(
                instruction_id=profile.mnemonic or profile.xml_id,
                total_test_count=total_count,
                complexity=profile.complexity_score,
                dimensions=final_dims,
                risk_analysis=risk or self._rule_based_risk(profile),
                constraints_to_verify=constraints_verify or [],
            )

            # Step 5: Build output
            plan_output = PlanOutput(
                instruction=profile,
                strategy=strategy,
                reasoning=reasoning,
            )

            # Step 6: Synthesize markdown summary
            if use_llm and self._llm is not None:
                summary = self._synthesize_summary(profile, strategy, reasoning)
            else:
                summary = self._build_rule_summary(profile, strategy)

            plan_output.test_plan_summary = summary

            logger.info("planner.done",
                        mnemonic=profile.mnemonic,
                        dimensions=len(final_dims),
                        tests=strategy.total_test_count)

            return {
                "status": "ok",
                "profile": plan_output.instruction,
                "strategy": plan_output.strategy,
                "plan_json": serialize_profile_to_json(profile),
                "plan_markdown": summary,
                "metadata": {
                    "mnemonic": profile.mnemonic,
                    "xml_id": profile.xml_id,
                    "complexity": profile.complexity_score,
                    "total_tests": strategy.total_test_count,
                    "dimensions": len(final_dims),
                    "method": "llm" if (use_llm and self._llm) else "rules",
                },
            }

        except Exception as e:
            logger.error("planner.error", error=str(e)[:200])
            return {
                "status": "error",
                "query": mnemonic or xml_id,
                "error": str(e)[:500],
            }

    def plan_from_data(self, instruction_data: dict[str, Any], user_goal: str = "") -> dict[str, Any]:
        """Plan from pre-fetched instruction data (avoids second DB query)."""
        profile = self._analyzer.extract_profile_from_data(instruction_data)
        return self._plan_from_profile(profile, user_goal)

    def quick_analyze(self, mnemonic: str) -> InstructionProfile | None:
        """Quick analysis without LLM, returns raw profile."""
        return self._analyzer.extract_profile(mnemonic=mnemonic)

    # ── Internal: LLM Strategy Generation ────────────────────

    def _generate_strategy_llm(
        self, profile: InstructionProfile, user_goal: str
    ) -> tuple[list[dict[str, Any]], str, str, list[str], int]:
        """Use LLM to generate strategy JSON. Returns (dims, reasoning, risk, constraints, count)."""
        profile_ctx = format_profile_context(profile)
        user_prompt = build_strategy_prompt(profile_ctx, user_goal)

        try:
            response = self._llm.invoke([
                SystemMessage(content=STRATEGY_SYSTEM_PROMPT),
                HumanMessage(content=user_prompt),
            ])
            content = str(response.content).strip()

            # Parse JSON from potential markdown wrapping
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            data = json.loads(content)
            dims = data.get("dimensions", [])
            reasoning = data.get("reasoning", "")
            risk = data.get("risk_analysis", "")
            constraints = data.get("constraints_to_verify", [])
            total = int(data.get("total_test_count", self._estimate_total_tests(profile, len(dims))))

            return dims, reasoning, risk, constraints, total

        except (json.JSONDecodeError, Exception) as e:
            logger.warning("planner.llm_strategy_failed", error=str(e)[:100])
            return [], "", "", [], 0

    def _plan_from_profile(self, profile: InstructionProfile, user_goal: str) -> dict[str, Any]:
        """Internal: plan from an already-built profile."""
        rule_dims = InstructionAnalyzer.recommend_test_dimensions(profile)

        if self._llm is not None:
            strategy_dims, reasoning, risk, constraints_verify, total_count = \
                self._generate_strategy_llm(profile, user_goal)
            final_dims = self._convert_dimensions(strategy_dims) if strategy_dims \
                else self._convert_rule_dims(rule_dims)
        else:
            final_dims = self._convert_rule_dims(rule_dims)
            reasoning = "Rule-based strategy"
            risk = self._rule_based_risk(profile)
            constraints_verify = [c.description[:120] for c in profile.constrained_unpredictable[:3]]
            total_count = self._estimate_total_tests(profile, len(final_dims))

        strategy = TestStrategy(
            instruction_id=profile.mnemonic or profile.xml_id,
            total_test_count=total_count,
            complexity=profile.complexity_score,
            dimensions=final_dims,
            risk_analysis=risk,
            constraints_to_verify=constraints_verify,
        )

        summary = self._build_rule_summary(profile, strategy)

        return {
            "status": "ok",
            "profile": profile,
            "strategy": strategy,
            "plan_json": serialize_profile_to_json(profile),
            "plan_markdown": summary,
            "metadata": {
                "mnemonic": profile.mnemonic,
                "complexity": profile.complexity_score,
                "total_tests": strategy.total_test_count,
                "dimensions": len(final_dims),
            },
        }

    def _synthesize_summary(
        self, profile: InstructionProfile, strategy: TestStrategy, reasoning: str
    ) -> str:
        """Use LLM to generate a human-readable plan summary."""
        dims_text = "\n".join(
            f"### {d.name} (Priority: {d.priority}, {d.suggested_test_count} tests)\n"
            f"Focus: {', '.join(d.focus_areas)}\n"
            f"Rationale: {d.rationale}\n"
            for d in strategy.dimensions
        )
        user_content = f"""## Instruction: {profile.mnemonic} ({profile.xml_id})
**Class**: {profile.instr_class}
**Brief**: {profile.brief}
**Complexity**: {profile.complexity_score}/10

## AI Reasoning
{reasoning}

## Test Dimensions
{dims_text}

## Constraints to Verify
{chr(10).join(f'- {c}' for c in strategy.constraints_to_verify) if strategy.constraints_to_verify else 'None'}

## Risk Analysis
{strategy.risk_analysis}"""

        try:
            response = self._llm.invoke([
                SystemMessage(content=PLAN_SYNTHESIS_PROMPT),
                HumanMessage(content=user_content),
            ])
            return str(response.content)
        except Exception:
            return self._build_rule_summary(profile, strategy)

    # ── Conversion helpers ───────────────────────────────────

    @staticmethod
    def _convert_rule_dims(rule_dims: list[dict[str, Any]]) -> list[TestDimension]:
        """Convert rule-based dimension dicts to TestDimension objects."""
        return [
            TestDimension(
                name=d.get("name", ""),
                priority=d.get("priority", "medium"),
                coverage_percentage=round(float(d.get("coverage_pct", 0)), 1),
                focus_areas=d.get("focus", []),
                rationale=d.get("rationale", ""),
                suggested_test_count=int(d.get("suggested_count", 2)),
            )
            for d in rule_dims
        ]

    @staticmethod
    def _convert_dimensions(llm_dims: list[dict[str, Any]]) -> list[TestDimension]:
        """Convert LLM-generated dimension dicts to TestDimension objects."""
        dims = []
        for d in llm_dims:
            try:
                dims.append(TestDimension(
                    name=str(d.get("name", "")),
                    priority=str(d.get("priority", "medium")),
                    coverage_percentage=round(float(d.get("coverage_percentage", 0)), 1),
                    focus_areas=list(d.get("focus_areas", [])),
                    rationale=str(d.get("rationale", "")),
                    suggested_test_count=int(d.get("suggested_test_count", 2)),
                ))
            except Exception:
                continue
        return dims

    # ── Rule-based fallbacks ─────────────────────────────────

    @staticmethod
    def _rule_based_risk(profile: InstructionProfile) -> str:
        risk_parts: list[str] = []
        if profile.constrained_unpredictable:
            risk_parts.append(
                f"{len(profile.constrained_unpredictable)} CONSTRAINED_UNPREDICTABLE conditions "
                f"pose the highest risk — must verify behavior (UNDEFINED, NOP, or UNKNOWN)."
            )
        if profile.encoding_count > 2:
            risk_parts.append(
                f"Multiple ({profile.encoding_count}) encodings increase the risk of "
                f"missing encoding-specific behavior variations."
            )
        if profile.feature_dependencies:
            deps = ", ".join(f.feature_name for f in profile.feature_dependencies[:3])
            risk_parts.append(f"Feature dependencies ({deps}) require testing on appropriately configured systems.")
        if profile.simd_register_count > 0:
            risk_parts.append("SIMD/FP operations require element-size-aware testing (8B/16B, 4H/8H, etc.).")
        if profile.has_shift_extend:
            risk_parts.append("Shift/extend modifiers add combinatorial complexity to operand validation.")
        if not risk_parts:
            risk_parts.append("Low risk — standard register/immediate operations with minimal edge cases.")
        return " ".join(risk_parts)

    @staticmethod
    def _estimate_total_tests(profile: InstructionProfile, num_dims: int) -> int:
        """Estimate total test count based on complexity and dimensions."""
        base = max(1, num_dims) * 2
        complexity_bonus = profile.complexity_score
        encoding_bonus = max(0, profile.encoding_count - 1) * 2
        cu_bonus = len(profile.constrained_unpredictable)
        return min(base + complexity_bonus + encoding_bonus + cu_bonus, 30)

    @staticmethod
    def _build_rule_summary(profile: InstructionProfile, strategy: TestStrategy) -> str:
        """Build a markdown summary without LLM (rule-based)."""
        lines: list[str] = []
        lines.append(f"# Test Plan: {profile.mnemonic} ({profile.xml_id})")
        lines.append("")
        lines.append("## 1. Instruction Overview")
        lines.append(f"- **Mnemonic**: {profile.mnemonic}")
        lines.append(f"- **Class**: {profile.instr_class}")
        lines.append(f"- **Brief**: {profile.brief}")
        lines.append(f"- **Encodings**: {profile.encoding_count} variant(s)")
        lines.append(f"- **Operands**: {profile.operand_count}")
        lines.append(f"- **Complexity**: {profile.complexity_score}/10")
        if profile.is_alias:
            lines.append(f"- **Alias** of: {profile.alias_of}")
        lines.append("")

        lines.append("## 2. Test Strategy")
        lines.append(f"- **Total test cases**: {strategy.total_test_count}")
        lines.append(f"- **Test dimensions**: {len(strategy.dimensions)}")
        lines.append(f"- **Approach**: {'LLM-driven' if strategy.total_test_count > 8 else 'Rule-based'} planning")
        lines.append("")

        lines.append("## 3. Test Dimensions")
        for d in strategy.dimensions:
            lines.append(f"### {d.name} ({d.priority} priority, ~{d.suggested_test_count} tests)")
            focus_lines = "\n".join(f"  - {f}" for f in d.focus_areas)
            lines.append(f"{focus_lines}")
            lines.append(f"  *Rationale*: {d.rationale}")
            lines.append("")

        lines.append("## 4. Key Edge Cases")
        if strategy.constraints_to_verify:
            for i, c in enumerate(strategy.constraints_to_verify, 1):
                lines.append(f"{i}. {c}")
        else:
            lines.append("No CONSTRAINED_UNPREDICTABLE conditions identified.")
        lines.append("")

        lines.append("## 5. Risk Analysis")
        lines.append(strategy.risk_analysis)
        lines.append("")

        lines.append("## 6. Recommended Test Scenarios")
        lines.append("(Use `generate_testcase` tool to produce actual test cases for each dimension above.)")
        lines.append("")

        # Quick lookup params for each dimension
        for d in strategy.dimensions[:5]:
            profile_uri = f"mnemonic={profile.mnemonic}"
            if profile.xml_id:
                profile_uri = f"xml_id={profile.xml_id}"
            lines.append(f"- **{d.name}**: `generate_testcase({profile_uri}, test_count={d.suggested_test_count})`")

        return "\n".join(lines)


# ── Singleton convenience ────────────────────────────────────

_planner: InstructionPlanner | None = None


def get_planner(sqlite_client: Any = None, llm: Any = None) -> InstructionPlanner:
    """Get or create a global InstructionPlanner instance."""
    global _planner
    if _planner is None or sqlite_client is not None or llm is not None:
        _planner = InstructionPlanner(sqlite_client=sqlite_client, llm=llm)
    return _planner
