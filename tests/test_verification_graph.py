from __future__ import annotations

import asyncio
import time

from arm_isa_agent.verification.graph import VerificationGraphRunner
from arm_isa_agent.verification.models import VerificationReport
from arm_isa_agent.verification.orchestrator import VerificationOrchestrator


def _report(*, static: str = "PASS", compile_status: str = "PASS") -> VerificationReport:
    return VerificationReport(
        instruction="ADD",
        status="COMPILED" if compile_status == "PASS" else "FAILED",
        generated_status="PASS",
        static_review_status=static,  # type: ignore[arg-type]
        compile_status=compile_status,  # type: ignore[arg-type]
    )


def test_rule_verification_graph_uses_deterministic_path_once() -> None:
    calls: list[tuple[str, bool]] = []

    def core(instruction: str, use_llm: bool, *_: int, **__: object) -> VerificationReport:
        calls.append((instruction, use_llm))
        return _report()

    report = VerificationGraphRunner(core_verify=core).run("add", instruction_count=20, target_instruction_count=5)

    assert calls == [("ADD", False)]
    assert report.budget["langgraph"]["events"][-1]["node"] == "finalize"
    assert any("LangGraph compile_gate" in item for item in report.generation_trace)


def test_llm_verification_graph_retries_after_static_failure() -> None:
    calls: list[bool] = []

    def core(_: str, use_llm: bool, *__: int, **___: object) -> VerificationReport:
        calls.append(use_llm)
        return _report(static="FAIL", compile_status="SKIPPED") if len(calls) == 1 else _report()

    report = VerificationGraphRunner(core_verify=core, max_llm_retries=1).run("generate ADD test", use_llm=True)

    assert calls == [True, True]
    assert report.static_review_status == "PASS"
    assert any(event["node"] == "repair" for event in report.budget["langgraph"]["events"])


def test_verify_stream_forwards_worker_progress_before_final_report(monkeypatch) -> None:
    class FakeRunner:
        def __init__(self, *, progress_callback, **_: object) -> None:
            self._progress_callback = progress_callback

        def run(self, *_: object) -> VerificationReport:
            self._progress_callback("planner", "start", "Planning test", {})
            time.sleep(0.01)
            self._progress_callback("planner", "complete", "Plan complete", {"status": "ok"})
            return _report()

    monkeypatch.setattr("arm_isa_agent.verification.graph.VerificationGraphRunner", FakeRunner)
    orchestrator = object.__new__(VerificationOrchestrator)

    async def collect() -> list[str]:
        stream = orchestrator.verify_stream("add")
        first = await anext(stream)
        return [first, *[event async for event in stream]]

    events = asyncio.run(collect())

    assert "event: stage_start" in events[0]
    assert any("event: stage_complete" in event for event in events)
    assert any("event: result" in event for event in events)
