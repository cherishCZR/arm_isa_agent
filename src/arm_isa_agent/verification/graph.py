"""LangGraph control plane for the compile-only verification workflow.

The graph deliberately delegates XML retrieval, assembly instantiation, static
review, and compilation to the existing deterministic verification services.
LangGraph owns request normalization, conditional routing, bounded LLM retries,
and a trace that can be streamed or persisted by callers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable
from uuid import uuid4

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from arm_isa_agent.verification.graph_state import VerificationGraphEvent, VerificationGraphState
from arm_isa_agent.verification.models import VerificationReport
from arm_isa_agent.verification.progress import ProgressCallback

if TYPE_CHECKING:
    from arm_isa_agent.verification.orchestrator import VerificationOrchestrator


CoreVerification = Callable[..., VerificationReport]


class VerificationGraphRunner:
    """Run one verification request through an observable LangGraph workflow."""

    def __init__(
        self,
        orchestrator: "VerificationOrchestrator | None" = None,
        core_verify: CoreVerification | None = None,
        checkpointer: Any | None = None,
        max_llm_retries: int = 1,
        progress_callback: ProgressCallback | None = None,
    ) -> None:
        if core_verify is None:
            if orchestrator is None:
                raise ValueError("orchestrator or core_verify is required")
            core_verify = orchestrator._verify_single_instruction_program
        self._core_verify = core_verify
        self._max_llm_retries = max(0, max_llm_retries)
        self._progress_callback = progress_callback
        self._graph = self._build_graph(checkpointer or MemorySaver())

    def run(
        self,
        instruction: str,
        use_llm: bool = False,
        instruction_count: int = 100,
        target_instruction_count: int = 1,
        request_id: str | None = None,
    ) -> VerificationReport:
        """Invoke the graph and return the compatible VerificationReport."""
        thread_id = request_id or str(uuid4())
        state = self._graph.invoke(
            {
                "request_id": thread_id,
                "instruction": instruction,
                "use_llm": use_llm,
                "instruction_count": instruction_count,
                "target_instruction_count": target_instruction_count,
                "retry_count": 0,
                "max_retries": self._max_llm_retries if use_llm else 0,
                "events": [],
            },
            config={"configurable": {"thread_id": thread_id}},
        )
        report = state.get("report")
        if report is None:
            raise RuntimeError("Verification graph completed without a report")
        self._attach_trace(report, state.get("events", []), thread_id)
        return report

    def stream(
        self,
        instruction: str,
        use_llm: bool = False,
        instruction_count: int = 100,
        target_instruction_count: int = 1,
        request_id: str | None = None,
    ):
        """Expose LangGraph update events for API adapters and observability."""
        thread_id = request_id or str(uuid4())
        initial_state: VerificationGraphState = {
            "request_id": thread_id,
            "instruction": instruction,
            "use_llm": use_llm,
            "instruction_count": instruction_count,
            "target_instruction_count": target_instruction_count,
            "retry_count": 0,
            "max_retries": self._max_llm_retries if use_llm else 0,
            "events": [],
        }
        yield from self._graph.stream(
            initial_state,
            config={"configurable": {"thread_id": thread_id}},
            stream_mode="updates",
        )

    def _build_graph(self, checkpointer: Any):
        graph = StateGraph(VerificationGraphState)
        graph.add_node("normalize_request", self._normalize_request)
        graph.add_node("resolve_targets", self._resolve_targets)
        graph.add_node("execute_verification", self._execute_verification)
        graph.add_node("static_review_gate", self._static_review_gate)
        graph.add_node("compile_gate", self._compile_gate)
        graph.add_node("repair", self._repair)
        graph.add_node("finalize", self._finalize)

        graph.add_edge(START, "normalize_request")
        graph.add_edge("normalize_request", "resolve_targets")
        graph.add_edge("resolve_targets", "execute_verification")
        graph.add_edge("execute_verification", "static_review_gate")
        graph.add_conditional_edges(
            "static_review_gate",
            self._after_static_review,
            {"compile_gate": "compile_gate", "repair": "repair", "finalize": "finalize"},
        )
        graph.add_conditional_edges(
            "compile_gate",
            self._after_compile,
            {"repair": "repair", "finalize": "finalize"},
        )
        graph.add_edge("repair", "static_review_gate")
        graph.add_edge("finalize", END)
        return graph.compile(checkpointer=checkpointer)

    @staticmethod
    def _event(node: str, status: str, message: str, state: VerificationGraphState, **metadata: Any) -> VerificationGraphEvent:
        return {
            "node": node,
            "status": status,  # type: ignore[typeddict-item]
            "message": message,
            "retry_count": state.get("retry_count", 0),
            "metadata": metadata,
        }

    def _normalize_request(self, state: VerificationGraphState) -> dict[str, Any]:
        raw = state.get("instruction", "").strip()
        normalized = raw if state.get("use_llm", False) else raw.upper()
        self._publish("planner", "start", "Normalizing verification request", instruction=normalized)
        return {
            "normalized_instruction": normalized,
            "events": [self._event("normalize_request", "completed", "Normalized verification request", state, instruction=normalized)],
        }

    def _resolve_targets(self, state: VerificationGraphState) -> dict[str, Any]:
        mode = "LLM-assisted target extraction" if state.get("use_llm") else "deterministic XML target resolution"
        return {
            "events": [self._event("resolve_targets", "completed", mode, state)],
        }

    def _execute_verification(self, state: VerificationGraphState) -> dict[str, Any]:
        report = self._core_verify(
            state.get("normalized_instruction", state.get("instruction", "")),
            state.get("use_llm", False),
            state.get("instruction_count", 100),
            state.get("target_instruction_count", 1),
            progress_callback=self._progress_callback,
        )
        return {
            "report": report,
            "events": [self._event(
                "execute_verification", "completed", "Executed XML-aware generation and validation services", state,
                report_status=report.status, generated=report.generated_status, static_review=report.static_review_status,
                compiled=report.compile_status,
            )],
        }

    def _static_review_gate(self, state: VerificationGraphState) -> dict[str, Any]:
        report = state.get("report")
        if report is None:
            return {"events": [self._event("static_review_gate", "failed", "No verification report was produced", state)]}
        passed = report.static_review_status in {"PASS", "WARNING"}
        return {"events": [self._event(
            "static_review_gate", "completed" if passed else "failed",
            f"Static review status: {report.static_review_status}", state,
        )]}

    def _after_static_review(self, state: VerificationGraphState) -> str:
        report = state.get("report")
        if report and report.static_review_status in {"PASS", "WARNING"}:
            return "compile_gate"
        if self._can_retry(state):
            return "repair"
        return "finalize"

    def _compile_gate(self, state: VerificationGraphState) -> dict[str, Any]:
        report = state.get("report")
        compile_status = report.compile_status if report else "NOT_STARTED"
        passed = compile_status == "PASS"
        return {"events": [self._event(
            "compile_gate", "completed" if passed else "failed",
            f"Compile-only status: {compile_status}", state,
        )]}

    def _after_compile(self, state: VerificationGraphState) -> str:
        report = state.get("report")
        if report and report.compile_status == "PASS":
            return "finalize"
        return "repair" if self._can_retry(state) else "finalize"

    def _repair(self, state: VerificationGraphState) -> dict[str, Any]:
        retry_count = state.get("retry_count", 0) + 1
        self._publish("llm", "progress", "Retrying LLM generation after validation failure", retry_count=retry_count)
        report = self._core_verify(
            state.get("normalized_instruction", state.get("instruction", "")),
            True,
            state.get("instruction_count", 100),
            state.get("target_instruction_count", 1),
            progress_callback=self._progress_callback,
        )
        return {
            "retry_count": retry_count,
            "report": report,
            "events": [self._event(
                "repair", "completed", "Retried LLM generation after validation failure", {**state, "retry_count": retry_count},
                report_status=report.status, static_review=report.static_review_status, compiled=report.compile_status,
            )],
        }

    def _finalize(self, state: VerificationGraphState) -> dict[str, Any]:
        report = state.get("report")
        return {"events": [self._event(
            "finalize", "completed", "Finalized verification report", state,
            report_status=report.status if report else "ERROR",
        )]}

    @staticmethod
    def _can_retry(state: VerificationGraphState) -> bool:
        return bool(state.get("use_llm")) and state.get("retry_count", 0) < state.get("max_retries", 0)

    @staticmethod
    def _attach_trace(report: VerificationReport, events: list[VerificationGraphEvent], thread_id: str) -> None:
        report.generation_trace.extend(
            f"LangGraph {event['node']}: {event['message']}" for event in events
        )
        report.budget.setdefault("langgraph", {"thread_id": thread_id, "events": events})

    def _publish(self, stage: str, event: str, message: str, **snapshot: Any) -> None:
        if self._progress_callback is not None:
            self._progress_callback(stage, event, message, snapshot)
