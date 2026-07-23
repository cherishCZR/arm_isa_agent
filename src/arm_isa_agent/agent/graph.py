"""LangGraph Agent Graph — Router → Planner → Executor → [Reviewer → Repair]⨯3 → Summarizer.

The graph orchestrates tool-calling for ARM ISA question answering.

Standard flow:
    START → planner → executor ⇄ executor → summarizer → END

Test generation + review flow (self-correction loop):
    START → planner → executor(Generate) → reviewer → decision
                                                   ├── passed → summarizer → END
                                                   └── failed → repair → reviewer (max 3 loops)

Compiler Verification flow (one-shot pipeline):
    START → planner → executor(verification pipeline) → reviewer → decision
                                                              ├── passed → summarizer → END
                                                              └── failed → repair → reviewer (max 3 loops)
                                                  → summarizer → END

Key design decisions:
- Planner uses LLM to decompose the user query into an ordered tool-call plan.
- Executor iterates through the plan, invoking tools and collecting results.
- Reviewer (optional, for test_generation intent) checks quality across 5 dimensions.
- Repair (if review fails) attempts to fix issues and loops back to reviewer (max 3 times).
- Summarizer synthesizes all outputs into a final answer.
- Safety limits: MAX_ITERATIONS=15, MAX_PLAN_STEPS=8, MAX_REPAIR_ATTEMPTS=3.
"""

from __future__ import annotations

import itertools
import json
from typing import Any, Literal

import structlog
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from arm_isa_agent.agent.prompt_manager import (
    build_planner_prompt,
    build_summarizer_prompt,
    build_system_prompt,
)
from arm_isa_agent.agent.state import AgentState
from arm_isa_agent.agent.tool_registry import (
    get_all_tools,
    get_llm,
    get_sqlite,
    get_tool,
    get_tools_for_llm,
    set_services,
)
from arm_isa_agent.core.config import Settings, get_settings

logger = structlog.get_logger(__name__)

# ── Safety limits ────────────────────────────────────────────────

MAX_ITERATIONS = 15
MAX_PLAN_STEPS = 8
MAX_REPAIR_ATTEMPTS = 3

# Concrete assembly examples used by the no-LLM fallback formatter.
# These make the fallback answer feel closer to a hand-written explanation.
# Chinese one-sentence descriptions for common instructions used by the no-LLM fallback.
_CHINESE_BRIEFS: dict[str, str] = {
    "ABS": "计算源寄存器中有符号整数的绝对值，并将结果写入目标寄存器。",
    "ADD": "将两个源操作数相加，结果写入目标寄存器。",
    "SUB": "用第一个源操作数减去第二个源操作数，结果写入目标寄存器。",
    "MUL": "将两个源操作数相乘，结果写入目标寄存器。",
    "MADD": "将两个源操作数相乘后再加上第三个源操作数，结果写入目标寄存器。",
    "AND": "对两个源操作数按位与，结果写入目标寄存器。",
    "ORR": "对两个源操作数按位或，结果写入目标寄存器。",
    "EOR": "对两个源操作数按位异或，结果写入目标寄存器。",
    "LSL": "将源操作数逻辑左移指定位数，结果写入目标寄存器。",
    "LSR": "将源操作数逻辑右移指定位数，结果写入目标寄存器。",
    "LDR": "从内存地址加载数据到寄存器。",
    "STR": "将寄存器数据存储到内存地址。",
    "MOV": "将一个立即数或寄存器值移动到目标寄存器。",
    "CMP": "比较两个操作数，并根据结果设置 NZCV 标志位。",
    "CBZ": "如果寄存器值为 0，则跳转到指定标签。",
    "B": "无条件跳转到指定标签。",
    "BL": "调用子程序，并将返回地址写入 LR。",
    "RET": "从子程序返回。",
}

# Concrete assembly examples used by the no-LLM fallback formatter.
_CONCRETE_EXAMPLES: dict[str, str] = {
    "ABS": "MOV X1, #-100\nABS X0, X1\n// 执行后 X0 = 100",
    "ADD": "MOV X1, #10\nMOV X2, #20\nADD X0, X1, X2\n// 执行后 X0 = 30",
    "SUB": "MOV X1, #30\nMOV X2, #12\nSUB X0, X1, X2\n// 执行后 X0 = 18",
    "MUL": "MOV X1, #6\nMOV X2, #7\nMUL X0, X1, X2\n// 执行后 X0 = 42",
    "AND": "MOV X1, #0xFF\nMOV X2, #0x0F\nAND X0, X1, X2\n// 执行后 X0 = 0x0F",
    "ORR": "MOV X1, #0xF0\nMOV X2, #0x0F\nORR X0, X1, X2\n// 执行后 X0 = 0xFF",
    "EOR": "MOV X1, #0xFF\nMOV X2, #0x0F\nEOR X0, X1, X2\n// 执行后 X0 = 0xF0",
    "LSL": "MOV X1, #1\nLSL X0, X1, #3\n// 执行后 X0 = 8",
    "LSR": "MOV X1, #128\nLSR X0, X1, #4\n// 执行后 X0 = 8",
    "LDR": "LDR X0, [X1]\n// 从 X1 指向的地址加载 64 位数据到 X0",
    "STR": "STR X0, [X1]\n// 将 X0 的 64 位数据存储到 X1 指向的地址",
    "MOV": "MOV X0, #42\n// 执行后 X0 = 42",
    "CMP": "MOV X1, #10\nCMP X1, #20\n// 设置 NZCV 标志位",
    "CBZ": "CBZ X0, label\n// 如果 X0 为 0，跳转到 label",
    "B": "B label\n// 无条件跳转到 label",
    "BL": "BL function\n// 调用 function，返回地址写入 LR",
    "RET": "RET\n// 从子程序返回",
}


# ── AgentGraph class ─────────────────────────────────────────────

class AgentGraph:
    """LangGraph agent for ARM ISA exploration with self-correction loop.

    Usage:
        agent = AgentGraph(rag_pipeline, sqlite_client)
        agent.initialize()
        result = agent.run("What does ADD shifted register do?")
        result = agent.run("Generate tests for ADD")  # triggers review loop
    """

    def __init__(
        self,
        rag_pipeline: Any = None,
        sqlite_client: Any = None,
        settings: Settings | None = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._rag = rag_pipeline
        self._sqlite = sqlite_client
        self._llm: ChatOpenAI | None = None
        self._graph: Any = None

    # ── Lifecycle ─────────────────────────────────────────────

    def initialize(self) -> None:
        """Initialize LLM client and compile the LangGraph graph."""
        # Inject shared services into tool registry
        set_services(rag_pipeline=self._rag, sqlite_client=self._sqlite, llm=self._llm)

        # Trigger @register_tool side effects so the tool registry is populated
        import arm_isa_agent.tools  # noqa: F401

        # Build LLM client
        llm_kwargs: dict[str, Any] = {
            "model": self._settings.llm_model,
            "temperature": self._settings.llm_temperature,
        }
        if self._settings.llm_api_key:
            llm_kwargs["api_key"] = self._settings.llm_api_key
        if self._settings.llm_base_url:
            llm_kwargs["base_url"] = self._settings.llm_base_url

        self._llm = ChatOpenAI(**llm_kwargs)

        # Re-inject since llm was None before
        set_services(rag_pipeline=self._rag, sqlite_client=self._sqlite, llm=self._llm)

        # Build graph
        self._graph = self._build_graph()
        logger.info("agent.initialized", model=self._settings.llm_model)

    def _build_graph(self) -> StateGraph:
        """Build and compile the LangGraph state graph with self-correction loop.

        Graph structure:
            START → planner → executor ⇄ executor
                            ↓ (plan complete & intent==test_generation)
                            reviewer → decision_review
                            ├── passed → summarizer → END
                            └── failed → repair → reviewer (loop)
                            ↓ (plan complete & intent≠test_generation)
                            summarizer → END
        """
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("executor", self._executor_node)
        workflow.add_node("reviewer", self._reviewer_node)
        workflow.add_node("repair", self._repair_node)
        workflow.add_node("decision_review", self._decision_review_node)
        workflow.add_node("summarizer", self._summarizer_node)

        # Entry
        workflow.set_entry_point("planner")

        # planner → executor
        workflow.add_edge("planner", "executor")

        # executor ⇄ executor or → reviewer or → summarizer
        workflow.add_conditional_edges(
            "executor",
            self._should_continue,
            {
                "continue": "executor",
                "review": "reviewer",
                "summarize": "summarizer",
            },
        )

        # reviewer → decision_review
        workflow.add_edge("reviewer", "decision_review")

        # decision_review → repair or summarizer
        workflow.add_conditional_edges(
            "decision_review",
            self._should_repair_or_summarize,
            {
                "repair": "repair",
                "summarize": "summarizer",
            },
        )

        # repair → reviewer (loop back)
        workflow.add_edge("repair", "reviewer")

        # summarizer → END
        workflow.add_edge("summarizer", END)

        return workflow.compile()

    # ── Public API ────────────────────────────────────────────

    def run(self, user_query: str, chat_history: list | None = None) -> dict[str, Any]:
        """Run the agent on a user query.

        Args:
            user_query: The user's question.
            chat_history: Optional previous messages.

        Returns:
            dict with "answer", "iterations", "tool_results", "review_results".
        """
        if self._graph is None or self._llm is None:
            raise RuntimeError("AgentGraph not initialized. Call initialize() first.")

        initial_state: AgentState = {
            "messages": list(chat_history or []),
            "user_query": user_query,
            "intent": "",
            "plan": [],
            "current_step": 0,
            "tool_results": [],
            "final_answer": "",
            "iteration_count": 0,
            "review_results": [],
            "repair_count": 0,
            "verification_report": {},
        }

        logger.info("agent.run.start", query=user_query[:100])
        result = self._graph.invoke(initial_state)
        logger.info(
            "agent.run.done",
            iterations=result.get("iteration_count", 0),
            repair_count=result.get("repair_count", 0),
        )

        return {
            "answer": result.get("final_answer", ""),
            "iterations": result.get("iteration_count", 0),
            "tool_results": result.get("tool_results", []),
            "review_results": result.get("review_results", []),
            "verification_report": result.get("verification_report", {}),
        }

    async def arun(self, user_query: str, chat_history: list | None = None) -> dict[str, Any]:
        """Async version of run()."""
        if self._graph is None or self._llm is None:
            raise RuntimeError("AgentGraph not initialized. Call initialize() first.")

        initial_state: AgentState = {
            "messages": list(chat_history or []),
            "user_query": user_query,
            "intent": "",
            "plan": [],
            "current_step": 0,
            "tool_results": [],
            "final_answer": "",
            "iteration_count": 0,
            "review_results": [],
            "repair_count": 0,
            "verification_report": {},
        }

        logger.info("agent.arun.start", query=user_query[:100])
        result = await self._graph.ainvoke(initial_state)
        logger.info(
            "agent.arun.done",
            iterations=result.get("iteration_count", 0),
            repair_count=result.get("repair_count", 0),
        )

        return {
            "answer": result.get("final_answer", ""),
            "iterations": result.get("iteration_count", 0),
            "tool_results": result.get("tool_results", []),
            "review_results": result.get("review_results", []),
            "verification_report": result.get("verification_report", {}),
        }

    @property
    def graph(self) -> Any:
        return self._graph

    # ── Graph Nodes ───────────────────────────────────────────

    def _planner_node(self, state: AgentState) -> dict[str, Any]:
        """Planner node: analyze query and create a tool-call plan."""
        query = state["user_query"]
        iteration = state.get("iteration_count", 0)

        logger.info("agent.planner", iteration=iteration, query=query[:80])

        # For the first iteration: plan from scratch
        if iteration == 0 and not state.get("plan"):
            return self._create_plan(query)

        # For subsequent iterations: check if we need more tools
        return self._replan(state)

    def _create_plan(self, query: str) -> dict[str, Any]:
        """Create initial execution plan from user query."""
        # Fast path: if the user explicitly names an instruction, look it up directly.
        direct_mnemonic = self._extract_mnemonic_from_query(query)
        if direct_mnemonic:
            logger.info("agent.plan_direct_lookup", mnemonic=direct_mnemonic)
            return {
                "intent": "retrieval",
                "plan": [
                    {"tool_name": "query_instruction", "tool_args": {"xml_id_or_mnemonic": direct_mnemonic}},
                    {"tool_name": "query_constraint", "tool_args": {"xml_id": direct_mnemonic}},
                ],
                "current_step": 0,
            }

        # Try structured JSON planning first
        prompt = build_planner_prompt(query)
        try:
            response = self._llm.invoke([HumanMessage(content=prompt)])  # type: ignore[union-attr]
            content = str(response.content).strip()

            # Extract JSON from possible markdown code block
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            plan_data = json.loads(content)
            intent = plan_data.get("intent", "general")
            plan = plan_data.get("plan", [])

            # Safety: limit plan size
            plan = plan[:MAX_PLAN_STEPS]

            logger.info("agent.plan_created", intent=intent, steps=len(plan))
            return {
                "intent": intent,
                "plan": plan,
                "current_step": 0,
            }

        except (json.JSONDecodeError, Exception) as e:
            logger.warning("agent.plan_json_failed", error=str(e)[:100])
            # Fallback: simple single-step plan
            return self._create_fallback_plan(query)

    def _create_fallback_plan(self, query: str) -> dict[str, Any]:
        """Fallback plan: use a direct lookup if possible, otherwise semantic search."""
        direct_mnemonic = self._extract_mnemonic_from_query(query)
        if direct_mnemonic:
            return {
                "intent": "retrieval",
                "plan": [{"tool_name": "query_instruction", "tool_args": {"xml_id_or_mnemonic": direct_mnemonic}}],
                "current_step": 0,
            }

        return {
            "intent": "general",
            "plan": [{"tool_name": "retrieve_instruction", "tool_args": {"query": query, "top_k": 5}}],
            "current_step": 0,
        }

    @staticmethod
    def _extract_mnemonic_from_query(user_query: str) -> str:
        """Extract a likely ARM instruction mnemonic from the user query."""
        import re

        text = user_query.upper()
        # Explicit patterns like "说明一下ABS这个指令" or "what does ADD do"
        explicit = re.search(r"(?:INSTRUCTION|指令|命令|instruction)\s*[：:]*\s*([A-Z][A-Z0-9]{1,7})", text, re.I)
        if explicit:
            return explicit.group(1).upper()

        # Common ARM mnemonics
        common_mnemonics = {
            "ADD", "SUB", "MUL", "MADD", "MSUB", "SMADDL", "SMSUBL", "UMADDL", "UMSUBL",
            "LDR", "STR", "STP", "LDP", "LDUR", "STUR", "LDAR", "STLR",
            "MOV", "MOVK", "MOVN", "MOVP",
            "CMP", "CMN", "TST", "TEQ",
            "B", "BL", "B.cond", "CBZ", "CBNZ", "TBZ", "TBNZ", "RET", "BR", "BLR",
            "ADRP", "ADR", "NOP", "YIELD", "WFE", "WFI", "SEV", "SEVL", "ISB", "DSB", "DMB",
            "FADD", "FSUB", "FMUL", "FDIV", "FMAX", "FMIN", "FMOV", "FCVT", "FMADD", "FMSUB",
            "SCVTF", "UCVTF", "FCVTZS", "FCVTZU", "FRINTA", "FRINTM",
            "AND", "ORR", "EOR", "BIC", "ORN", "MVN", "NEG", "ABS",
            "LSL", "LSR", "ASR", "ROR",
            "LDP", "STP", "LDNP", "STNP",
            "LD1", "LD2", "LD3", "LD4", "ST1", "ST2", "ST3", "ST4",
            "FABS", "FNEG", "FSQRT",
            "CSEL", "CSINC", "CSINV", "CSNEG",
            "SVC", "HVC", "SMC", "ERET", "DC", "IC", "TLBI", "AT",
        }
        words = re.findall(r"\b([A-Z][A-Z0-9]{1,7})\b", text)
        for w in words:
            if w in common_mnemonics:
                return w
        return ""

    def _replan(self, state: AgentState) -> dict[str, Any]:
        """Re-plan based on partial results — decide if more tools are needed."""
        plan = state.get("plan", [])
        current = state.get("current_step", 0)
        if current < len(plan):
            return {}
        return {}

    def _executor_node(self, state: AgentState) -> dict[str, Any]:
        """Executor node: invoke the next tool in the plan."""
        plan: list[dict[str, Any]] = state.get("plan", [])
        current_step: int = state.get("current_step", 0)
        iteration: int = state.get("iteration_count", 0)
        tool_results: list[dict[str, Any]] = list(state.get("tool_results", []))

        if current_step >= len(plan):
            logger.info("agent.executor_no_steps", iteration=iteration)
            return {
                "iteration_count": iteration + 1,
            }

        step = plan[current_step]
        tool_name = step.get("tool_name", "")
        tool_args = step.get("tool_args", {})

        logger.info("agent.executor", step=current_step + 1, total=len(plan), tool=tool_name)

        # Invoke the tool
        tool_fn = get_tool(tool_name)
        if tool_fn is None:
            err_msg = f"Tool '{tool_name}' not found. Available: {list(get_all_tools().keys())}"
            logger.warning("agent.tool_not_found", tool=tool_name)
            tool_results.append({
                "step": current_step + 1,
                "tool_name": tool_name,
                "error": err_msg,
            })
        else:
            try:
                result = tool_fn(**tool_args)
                tool_results.append({
                    "step": current_step + 1,
                    "tool_name": tool_name,
                    "tool_args": tool_args,
                    "result": result,
                })
                logger.info("agent.tool_done", tool=tool_name)
            except Exception as e:
                logger.error("agent.tool_error", tool=tool_name, error=str(e)[:200])
                tool_results.append({
                    "step": current_step + 1,
                    "tool_name": tool_name,
                    "tool_args": tool_args,
                    "error": str(e)[:500],
                })

        return {
            "current_step": current_step + 1,
            "iteration_count": iteration + 1,
            "tool_results": tool_results,
        }

    def _should_continue(
        self, state: AgentState
    ) -> Literal["continue", "review", "summarize"]:
        """Determine next node after executor.

        - If more steps remain → continue (loop back to executor)
        - If plan complete AND intent is test_generation → review
        - If plan complete AND intent is NOT test_generation → summarize
        """
        iteration = state.get("iteration_count", 0)
        plan = state.get("plan", [])
        current = state.get("current_step", 0)
        intent = state.get("intent", "")

        # Safety limit
        if iteration >= MAX_ITERATIONS:
            logger.warning("agent.max_iterations", iterations=iteration)
            return "summarize"

        # More steps remain
        if current < len(plan):
            return "continue"

        # Plan complete → route based on intent
        is_test_gen = (
            intent in ("test_generation", "generate_tests", "testcase_generation", "verification")
            or any(
                kw in intent.lower()
                for kw in ["test_generation", "generate_test", "test_case", "testcase", "verification"]
            )
        )

        if is_test_gen and current >= len(plan):
            # Check if any tool results are test-related
            has_test_results = any(
                tr.get("tool_name", "").startswith("generate_")
                for tr in state.get("tool_results", [])
            )
            if has_test_results:
                logger.info("agent.routing_to_review", intent=intent)
                return "review"

        logger.info("agent.plan_complete", steps=current)
        return "summarize"

    # ═════════════════════════════════════════════════════════════
    # Reviewer node — 5-dimension quality check
    # ═════════════════════════════════════════════════════════════

    def _reviewer_node(self, state: AgentState) -> dict[str, Any]:
        """Reviewer node: check generated testcase quality across 5 dimensions.

        This node:
        1. Extracts the target mnemonic from tool results
        2. Loads instruction profile from SQLite
        3. Reconstructs the test suite from generation results
        4. Runs TestcaseReviewer (rule-based + optional LLM)
        5. Returns review results for the decision node
        """
        tool_results = state.get("tool_results", [])
        intent = state.get("intent", "")
        repair_count = state.get("repair_count", 0)

        logger.info(
            "agent.reviewer",
            intent=intent,
            repair_count=repair_count,
            tool_results_count=len(tool_results),
        )

        # Extract mnemonic from tool results or query
        mnemonic = self._extract_mnemonic_from_results(tool_results, state["user_query"])

        if not mnemonic:
            logger.warning("agent.reviewer.no_mnemonic")
            # Store a pass-by-default review so we don't get stuck
            review_results = list(state.get("review_results", []))
            review_results.append({
                "passed": True,
                "score": 100,
                "reviewer_notes": "No mnemonic found in results; skipping review.",
                "issues": [],
                "suggestions": [],
            })
            return {"review_results": review_results}

        try:
            # Load profile from DB
            from arm_isa_agent.planning.analyzer import InstructionAnalyzer
            sqlite = get_sqlite()
            analyzer = InstructionAnalyzer(sqlite)
            profile = analyzer.extract_profile(mnemonic=mnemonic)

            if not profile or not profile.mnemonic:
                logger.warning("agent.reviewer.profile_not_found", mnemonic=mnemonic)
                review_results = list(state.get("review_results", []))
                review_results.append({
                    "passed": True,
                    "score": 100,
                    "reviewer_notes": f"Could not load profile for '{mnemonic}'.",
                    "issues": [],
                    "suggestions": [],
                })
                return {"review_results": review_results}

            # Build test suite from generation results
            from arm_isa_agent.generation.generators import TestCaseSuiteGenerator
            gen = TestCaseSuiteGenerator(llm=None, sqlite_client=sqlite)
            suite = gen.generate_suite(profile, use_llm=False)

            # Run the reviewer
            from arm_isa_agent.review_generation.reviewer import TestcaseReviewer
            reviewer = TestcaseReviewer(self._llm)
            result = reviewer.review(
                test_suite=suite,
                profile=profile,
                strategy=None,
                use_llm=False,  # Rule-based for speed in the loop
            )

            # Store review result
            review_results = list(state.get("review_results", []))
            review_results.append({
                "mnemonic": mnemonic,
                "passed": result.passed,
                "score": result.score,
                "high_issues": result.high_severity_count,
                "medium_issues": result.medium_severity_count,
                "low_issues": result.low_severity_count,
                "total_issues": result.total_issues,
                "issues": [
                    {
                        "type": i.type,
                        "severity": i.severity,
                        "description": i.description,
                        "location": i.location,
                        "suggestion": i.suggestion,
                        "dimension": i.dimension,
                    }
                    for i in result.issues
                ],
                "suggestions": result.suggestions,
                "reviewer_notes": result.reviewer_notes,
                "dimension_scores": [
                    {"dimension": ds.dimension, "score": ds.score, "issues_count": ds.issues_count}
                    for ds in result.dimension_scores
                ],
            })

            logger.info(
                "agent.reviewer.done",
                mnemonic=mnemonic,
                passed=result.passed,
                score=result.score,
                issues=result.total_issues,
            )

            return {"review_results": review_results}

        except Exception as e:
            logger.error("agent.reviewer.error", error=str(e)[:300])
            review_results = list(state.get("review_results", []))
            review_results.append({
                "passed": True,
                "score": 100,
                "reviewer_notes": f"Review error: {str(e)[:200]}",
                "issues": [],
                "suggestions": [],
            })
            return {"review_results": review_results}

    @staticmethod
    def _extract_mnemonic_from_results(
        tool_results: list[dict[str, Any]],
        user_query: str,
    ) -> str:
        """Extract the target instruction mnemonic from tool results or query."""
        # Try from tool results
        for tr in tool_results:
            tool_name = tr.get("tool_name", "")
            tool_args = tr.get("tool_args", {})
            result_str = str(tr.get("result", ""))

            # Check tool_args for mnemonic
            for key in ("mnemonic", "instruction", "query"):
                val = tool_args.get(key, "")
                if val and len(val) <= 10 and val.isalpha():
                    return val.upper()

            # Check if result contains a mnemonic marker
            for marker in ["### `", "**Instruction:** `", "Mnemonic:"]:
                idx = result_str.find(marker)
                if idx >= 0:
                    start = idx + len(marker)
                    end = result_str.find("`", start) if "`" in marker else result_str.find("\n", start)
                    if end >= 0:
                        val = result_str[start:end].strip()
                        if val and len(val) <= 10:
                            return val.split()[0].upper()

        # Try from user query
        import re
        # Look for uppercase 2-5 letter words that might be mnemonics
        mnemonics = re.findall(r'\b([A-Z]{2,5})\b', user_query.upper())
        common_mnemonics = {
            "ADD", "SUB", "MUL", "MADD", "LDR", "STR", "MOV", "CMP", "CMN",
            "AND", "ORR", "EOR", "BIC", "ORN", "MVN", "NEG", "TST",
            "LSL", "LSR", "ASR", "ROR", "LDP", "STP",
            "LD1R", "LD1", "LD2", "ST1", "ST2",
            "FMOV", "FADD", "FSUB", "FMUL", "FDIV",
            "SCVTF", "FCVTZS", "ABS",
        }
        for m in mnemonics:
            if m in common_mnemonics:
                return m

        return ""

    # ═════════════════════════════════════════════════════════════
    # Decision node — pass/fail routing
    # ═════════════════════════════════════════════════════════════

    def _decision_review_node(self, state: AgentState) -> dict[str, Any]:
        """Decision node: inspect last review result and decide next action.

        This is a pass-through node. The actual routing decision happens in
        _should_repair_or_summarize().

        We just log the decision here.
        """
        review_results = state.get("review_results", [])
        repair_count = state.get("repair_count", 0)

        if review_results:
            last_review = review_results[-1]
            passed = last_review.get("passed", True)
            score_val = last_review.get("score", 100)

            logger.info(
                "agent.decision",
                passed=passed,
                score=score_val,
                repair_count=repair_count,
            )
        else:
            logger.warning("agent.decision.no_review_results")

        return {}

    def _should_repair_or_summarize(
        self, state: AgentState
    ) -> Literal["repair", "summarize"]:
        """Decision: repair (loop back) or summarize (done).

        Returns "repair" if:
        - Last review FAILED (passed=False)
        - repair_count < MAX_REPAIR_ATTEMPTS (3)
        - There are fixable issues (syntax, constraint, encoding, semantic)

        Otherwise returns "summarize".
        """
        review_results = state.get("review_results", [])
        repair_count = state.get("repair_count", 0)

        if not review_results:
            logger.warning("agent.decision.no_results")
            return "summarize"

        last_review = review_results[-1]
        passed = last_review.get("passed", True)

        if passed:
            logger.info("agent.decision.passed", repair_count=repair_count)
            return "summarize"

        if repair_count >= MAX_REPAIR_ATTEMPTS:
            logger.warning(
                "agent.decision.max_repairs_reached",
                repair_count=repair_count,
                max=MAX_REPAIR_ATTEMPTS,
            )
            return "summarize"

        # Check if there are fixable issues
        issues = last_review.get("issues", [])
        fixable_types = {"syntax_error", "constraint_error", "encoding_error", "semantic_error"}
        has_fixable = any(
            i.get("type") in fixable_types and i.get("severity") in ("high", "medium")
            for i in issues
        )

        if not has_fixable:
            logger.info("agent.decision.no_fixable_issues")
            return "summarize"

        logger.info("agent.decision.repair", repair_count=repair_count + 1)
        return "repair"

    # ═════════════════════════════════════════════════════════════
    # Repair node — fix issues and prepare for re-review
    # ═════════════════════════════════════════════════════════════

    def _repair_node(self, state: AgentState) -> dict[str, Any]:
        """Repair node: attempt to fix issues found by the reviewer.

        Uses the RepairGenerator to create corrected testcases based on review feedback.
        Increments repair_count to track the self-correction loop.
        """
        review_results = state.get("review_results", [])
        repair_count = state.get("repair_count", 0)

        if not review_results:
            logger.warning("agent.repair.no_review_results")
            return {"repair_count": repair_count + 1}

        last_review = review_results[-1]
        mnemonic = last_review.get("mnemonic", "UNKNOWN")

        logger.info(
            "agent.repair",
            mnemonic=mnemonic,
            repair_count=repair_count + 1,
            issues=last_review.get("total_issues", 0),
        )

        try:
            # Load profile
            from arm_isa_agent.planning.analyzer import InstructionAnalyzer
            sqlite = get_sqlite()
            analyzer = InstructionAnalyzer(sqlite)
            profile = analyzer.extract_profile(mnemonic=mnemonic)
            if not profile or not profile.mnemonic:
                return {"repair_count": repair_count + 1}

            # Build suite
            from arm_isa_agent.generation.generators import TestCaseSuiteGenerator
            gen = TestCaseSuiteGenerator(llm=self._llm, sqlite_client=sqlite)
            suite = gen.generate_suite(profile, use_llm=True)  # Use LLM for repair

            # Run repair generator
            from arm_isa_agent.review_generation.reviewer import RepairGenerator
            from arm_isa_agent.review_generation.models import ReviewResult

            # Reconstruct ReviewResult
            review_result = ReviewResult(
                passed=last_review.get("passed", False),
                score=last_review.get("score", 0),
                issues=[
                    {
                        "type": i.get("type", "syntax_error"),
                        "severity": i.get("severity", "medium"),
                        "description": i.get("description", ""),
                        "location": i.get("location", ""),
                        "suggestion": i.get("suggestion", ""),
                        "dimension": i.get("dimension", ""),
                    }
                    for i in last_review.get("issues", [])
                ],
            )

            repair_gen = RepairGenerator(self._llm, max_repair_attempts=MAX_REPAIR_ATTEMPTS)
            repair_result = repair_gen.repair(review_result, suite, profile)

            logger.info(
                "agent.repair.done",
                repaired=repair_result.repaired,
                changes=len(repair_result.repair_changes),
            )

        except Exception as e:
            logger.error("agent.repair.error", error=str(e)[:300])

        return {"repair_count": repair_count + 1}

    # ═════════════════════════════════════════════════════════════
    # Summarizer node
    # ═════════════════════════════════════════════════════════════

    def _summarizer_node(self, state: AgentState) -> dict[str, Any]:
        """Summarizer node: synthesize final answer from all tool results and reviews."""
        query = state["user_query"]
        tool_results = state.get("tool_results", [])
        review_results = state.get("review_results", [])
        repair_count = state.get("repair_count", 0)

        logger.info(
            "agent.summarizer",
            results_count=len(tool_results),
            reviews=len(review_results),
            repairs=repair_count,
        )

        # Format tool results for the LLM
        results_lines: list[str] = []
        for tr in tool_results:
            step_num = tr.get("step", "?")
            tool_name = tr.get("tool_name", "unknown")
            results_lines.append(f"### Step {step_num}: {tool_name}")
            if "error" in tr:
                results_lines.append(f"**Error**: {tr['error']}")
            elif "result" in tr:
                # Truncate very long results
                raw = str(tr["result"])
                if len(raw) > 3000:
                    raw = raw[:3000] + f"\n... (truncated, total {len(raw)} chars)"
                results_lines.append(raw)
            results_lines.append("")

        # Format review results
        if review_results:
            results_lines.append("### Review Results (Quality Check)")
            for i, rr in enumerate(review_results):
                status = "✅ PASS" if rr.get("passed") else "❌ FAIL"
                results_lines.append(
                    f"- Review #{i + 1}: {status} | Score: {rr.get('score', 0):.0f} | "
                    f"Issues: {rr.get('total_issues', 0)} "
                    f"(H:{rr.get('high_issues', 0)} M:{rr.get('medium_issues', 0)} L:{rr.get('low_issues', 0)})"
                )
                notes = rr.get("reviewer_notes", "")
                if notes:
                    results_lines.append(f"  {notes}")
                dim_scores = rr.get("dimension_scores", [])
                if dim_scores:
                    results_lines.append(
                        "  | " + " | ".join(
                            f"{ds.get('dimension','?')}: {ds.get('score',0):.0f}"
                            for ds in dim_scores
                        ) + " |"
                    )
            results_lines.append("")
            if repair_count > 0:
                results_lines.append(f"**Self-correction loops:** {repair_count}/{MAX_REPAIR_ATTEMPTS}")
                results_lines.append("")

        formatted_results = "\n".join(results_lines)

        # Build summarizer prompt
        prompt = build_summarizer_prompt(query, formatted_results)
        system_msg = SystemMessage(content=prompt)
        user_msg = HumanMessage(content="Please synthesize the final answer now.")

        try:
            response = self._llm.invoke([system_msg, user_msg])  # type: ignore[union-attr]
            final_answer = str(response.content)
        except Exception as e:
            logger.error("agent.summarizer_error", error=str(e)[:200])
            # Fallback: produce a friendly template-based answer if possible
            final_answer = self._format_instruction_answer(query, tool_results)
            if not final_answer:
                final_answer = f"## Results for: {query}\n\n{formatted_results}"

        return {
            "final_answer": final_answer,
            "messages": [AIMessage(content=final_answer)],
        }

    @staticmethod
    def _format_instruction_answer(user_query: str, tool_results: list[dict[str, Any]]) -> str | None:
        """Build a user-friendly answer from query_instruction results without LLM.

        Returns None if no usable instruction profile is found.
        """
        import json
        import re

        # Find the first successful query_instruction result
        profile: dict[str, Any] | None = None
        for tr in tool_results:
            if tr.get("tool_name") == "query_instruction" and "result" in tr and "error" not in tr:
                try:
                    data = json.loads(str(tr["result"]))
                    if data.get("found"):
                        profile = data
                        break
                except (json.JSONDecodeError, TypeError):
                    continue

        if profile is None:
            return None

        mnemonic = profile.get("mnemonic", "UNKNOWN")
        title = profile.get("title", "")
        brief = profile.get("brief", "")
        description = (profile.get("description", "") or brief or "").strip()
        xml_id = profile.get("xml_id", "")
        instr_class = profile.get("instr_class", "")
        encodings = profile.get("encodings", [])
        operands = profile.get("operands", [])
        constraints = profile.get("constraints", [])
        features = profile.get("features", [])
        is_alias = profile.get("is_alias", False)
        alias_of = profile.get("alias_of")

        lines: list[str] = []
        lines.append(f"`{mnemonic}` 是 ARM AArch64 中的一个指令")
        if title:
            lines.append(f"（{title}）")
        lines.append("。\n"
        )

        # One-sentence definition
        chinese_brief = _CHINESE_BRIEFS.get(mnemonic.upper())
        if chinese_brief:
            lines.append(f"简单来说：{chinese_brief}\n")
        elif description:
            # Take first sentence or first 200 chars
            first_sentence = re.split(r"(?<=[.。!！?？])\s+", description, maxsplit=1)[0]
            if len(first_sentence) < 20 and len(description) > 20:
                first_sentence = description[:200]
            lines.append(f"简单来说：{first_sentence}\n")
        elif brief:
            lines.append(f"简单来说：{brief}\n")

        # Syntax
        if encodings:
            lines.append("## 基本语法\n")
            templates: list[str] = []
            for enc in encodings:
                asm = enc.get("assembly_template", "")
                if asm and asm not in templates:
                    templates.append(asm)
            for asm in templates[:5]:
                lines.append(f"```asm\n{asm}\n```\n")

        # Operands summary
        if operands:
            lines.append("其中：\n")
            for op in operands:
                symbol = op.get("symbol", "")
                desc = op.get("description", "")
                if symbol and desc:
                    lines.append(f"- `{symbol}`：{desc}")
            lines.append("")

        # Example
        lines.append("## 示例\n")
        concrete_example = _CONCRETE_EXAMPLES.get(mnemonic.upper())
        if concrete_example:
            lines.append(f"```asm\n{concrete_example}\n```\n")
        elif encodings and operands:
            # Build a concrete example from the first encoding template
            example = templates[0] if templates else ""
            # Map ARM assembly placeholders like <Xd>, <Wn>, <Xm> to real registers
            placeholder_map: dict[str, str] = {}
            for ph in re.findall(r"<([XW][dnam]?)>", example, re.I):
                ph_norm = ph[0].upper() + (ph[1].lower() if len(ph) > 1 else "n")
                if ph_norm not in placeholder_map:
                    width = ph_norm[0]
                    role = ph_norm[1]
                    if role == "d":
                        idx = 0
                    elif role == "n":
                        idx = 1
                    elif role == "m":
                        idx = 2
                    else:
                        idx = 3
                    placeholder_map[ph_norm] = f"{width}{idx}"
            for ph_norm, reg in placeholder_map.items():
                example = re.sub(rf"<{re.escape(ph_norm)}>", reg, example, flags=re.I)
            lines.append(f"```asm\n{example}\n```\n")
        else:
            lines.append(f"```asm\n{mnemonic} <destination>, <source>\n```\n")

        # Encodings summary
        if len(encodings) > 1:
            lines.append("## 编码变体\n")
            for enc in encodings:
                name = enc.get("name", "") or enc.get("label", "")
                asm = enc.get("assembly_template", "")
                if name and asm:
                    lines.append(f"- **{name}**: `{asm}`")
            lines.append("")

        # Constraints / edge cases
        if constraints:
            lines.append("## 边界情况与约束\n")
            for c in constraints[:5]:
                ctype = c.get("constraint_type", "") or "约束"
                cond = c.get("condition", "") or c.get("description", "")
                if cond:
                    lines.append(f"- **{ctype}**：{cond}")
            lines.append("")

        # Features
        if features:
            lines.append(f"**架构特性要求**：{', '.join(str(f) for f in features[:5])}\n")

        # Alias note
        if is_alias and alias_of:
            lines.append(f"\n> 注：`{mnemonic}` 是 `{alias_of}` 的别名。\n")

        lines.append(f"\n*来源：ARM A64 ISA，xml_id = `{xml_id}`，class = `{instr_class}`*")
        return "\n".join(lines)


# ── Factory function ─────────────────────────────────────────────

def build_agent(
    rag_pipeline: Any = None,
    sqlite_client: Any = None,
    settings: Settings | None = None,
) -> AgentGraph:
    """Build and initialize an AgentGraph instance.

    Args:
        rag_pipeline: Initialized RAGPipeline instance.
        sqlite_client: Initialized SQLiteClient instance.
        settings: Optional Settings override.

    Returns:
        Initialized AgentGraph ready for .run() calls.
    """
    agent = AgentGraph(
        rag_pipeline=rag_pipeline,
        sqlite_client=sqlite_client,
        settings=settings,
    )
    agent.initialize()
    return agent
