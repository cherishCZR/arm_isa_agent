"""Phase 8 — Compiler Verification Agent Integration Tests."""

import json
import os
import sys
import time

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 60)
print("Phase 8 — Compiler Verification Agent Integration Tests")
print("=" * 60)

# ---------------------------------------------------------------------------
# Test 1: Models
# ---------------------------------------------------------------------------
print("\n[Test 1] Verification Data Models")

from arm_isa_agent.verification.models import (
    CoverageBreakdown,
    StageResult,
    VerificationReport,
)

# CoverageBreakdown
cov = CoverageBreakdown(boundary=100, alias=80, invalid=100, normal=100, encoding=100, feature=0)
assert cov.overall == (100 + 80 + 100 + 100 + 100) / 5
assert cov.feature == 0
print("  [PASS] CoverageBreakdown (overall avg, zero feature)")

# StageResult
sr = StageResult(stage="retrieval", status="ok", duration_ms=12.5, output_summary="Loaded ADD")
assert sr.stage == "retrieval"
assert sr.status == "ok"
print("  [PASS] StageResult")

# VerificationReport (minimal)
report = VerificationReport(
    instruction="ADD",
    status="PASS",
    generated_tests=15,
    coverage=cov,
    review_score=92,
    review_passed=True,
    stage_results=[sr],
    total_duration_ms=500,
)
assert report.status == "PASS"
assert report.generated_tests == 15
md = report.to_markdown()
assert "[PASS]" in md
assert "ADD" in md
assert "92/100" in md
assert "boundary" in md
json_data = report.to_json_api()
assert json_data["instruction"] == "ADD"
print("  [PASS] VerificationReport (markdown + json export)")

# Edge: ERROR status
err_report = VerificationReport(
    instruction="UNKNOWN",
    status="ERROR",
    issues=[{"type": "orchestration_error", "severity": "high", "description": "Not found"}],
)
assert err_report.status == "ERROR"
assert err_report.generated_tests == 0
md_err = err_report.to_markdown()
assert "[ERROR]" in md_err
print("  [PASS] VerificationReport (ERROR status)")

# ---------------------------------------------------------------------------
# Test 2: VerificationOrchestrator (requires DB)
# ---------------------------------------------------------------------------
print("\n[Test 2] VerificationOrchestrator Full Pipeline")

try:
    from arm_isa_agent.kb.sqlite.client import SQLiteClient
    sqlite = SQLiteClient("data/sqlite/isa_kb.db")
    sqlite.initialize()

    # Check ADD exists
    from arm_isa_agent.planning.analyzer import InstructionAnalyzer
    analyzer = InstructionAnalyzer(sqlite)
    profile = analyzer.extract_profile(mnemonic="ADD")
    assert profile is not None, "ADD profile not found"
    print(f"  [PASS] ADD profile found: {profile.mnemonic}, complexity={profile.complexity_score}")

    from arm_isa_agent.verification.orchestrator import VerificationOrchestrator

    orchestrator = VerificationOrchestrator(
        sqlite_client=sqlite,
        llm=None,  # Rule-based mode (no LLM needed)
        use_llm_planning=False,
        use_llm_review=False,
    )

    t0 = time.perf_counter()
    report = orchestrator.verify("ADD")
    elapsed = time.perf_counter() - t0

    print(f"  Status: {report.status}")
    print(f"  Generated Tests: {report.generated_tests}")
    print(f"  Review Score: {report.review_score:.0f}/100")
    print(f"  Review Passed: {report.review_passed}")
    print(f"  Repair Attempts: {report.repair_attempts}")
    print(f"  Coverage: normal={report.coverage.normal:.0f}% boundary={report.coverage.boundary:.0f}% encoding={report.coverage.encoding:.0f}% alias={report.coverage.alias:.0f}% invalid={report.coverage.invalid:.0f}% feature={report.coverage.feature:.0f}%")
    print(f"  Issues: {len(report.issues)}")
    print(f"  Stages: {len(report.stage_results)} (total {report.total_duration_ms:.0f}ms)")

    # Assertions
    assert report.instruction == "ADD"
    assert report.generated_tests > 0, "Should generate test cases"
    assert 0 <= report.review_score <= 100
    assert len(report.stage_results) >= 5  # retrieval + constraint + planning + generation + review
    for sr in report.stage_results:
        stage_names = [s.stage for s in report.stage_results]
        print(f"    - {sr.stage}: {sr.status} ({sr.duration_ms:.0f}ms)")
    assert "retrieval" in stage_names
    assert "constraint_analysis" in stage_names
    assert "test_planning" in stage_names
    assert "test_generation" in stage_names
    assert "test_review" in stage_names
    print("  [PASS] Full pipeline completed all 5 stages")

    # Markdown output
    md_report = report.to_markdown()
    assert "Compiler Verification Report" in md_report
    assert "ADD" in md_report
    assert "Coverage" in md_report
    assert "Pipeline Stages" in md_report
    print(f"  [PASS] Markdown report generated ({len(md_report)} chars)")

except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"  [FAIL] {e}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Test 3: Convenience function
# ---------------------------------------------------------------------------
print("\n[Test 3] run_verification() Convenience Function")

from arm_isa_agent.verification import run_verification

report2 = run_verification("SUB", sqlite_client=sqlite, llm=None, use_llm=False)
assert report2.instruction == "SUB"
assert report2.generated_tests > 0
assert len(report2.stage_results) >= 5
print(f"  [PASS] SUB verification: status={report2.status}, tests={report2.generated_tests}, score={report2.review_score:.0f}")

# ---------------------------------------------------------------------------
# Test 4: API Schemas
# ---------------------------------------------------------------------------
print("\n[Test 4] API Request/Response Schemas")

from arm_isa_agent.api.schemas import (
    BatchGenerateRequest,
    BatchGenerateResponse,
    GenerateTestcaseRequest,
    GenerateTestcaseResponse,
    HealthResponse,
)

req = GenerateTestcaseRequest(instruction="ADD")
assert req.instruction == "ADD"
assert req.use_llm is False
print("  [PASS] GenerateTestcaseRequest")

resp = GenerateTestcaseResponse(
    instruction="ADD",
    status="PASS",
    generated_tests=20,
    coverage={"normal": 100, "boundary": 100, "encoding": 100, "alias": 80, "invalid": 100, "feature": 0, "overall": 80},
    review_score=95,
    review_passed=True,
    repair_attempts=0,
    repair_successful=False,
    total_duration_ms=1200,
    stage_results=[],
    issues=[],
    suggestions=[],
    generated_at="2026-01-01T00:00:00Z",
)
assert resp.status == "PASS"
assert resp.coverage["overall"] == 80
print("  [PASS] GenerateTestcaseResponse")

h = HealthResponse()
assert h.status == "ok"
print("  [PASS] HealthResponse")

# Batch
batch_req = BatchGenerateRequest(instructions=["ADD", "SUB"])
assert len(batch_req.instructions) == 2
print("  [PASS] BatchGenerateRequest")

# ---------------------------------------------------------------------------
# Test 5: FastAPI App Factory
# ---------------------------------------------------------------------------
print("\n[Test 5] FastAPI App Factory")

from arm_isa_agent.api.app import create_app
from arm_isa_agent.api.deps import set_services as api_set_services

# Set up services
api_set_services(sqlite_client=sqlite, llm=None, rag_pipeline=None)

app = create_app(sqlite_client=sqlite, llm=None, rag_pipeline=None)
assert app.title == "ARM ISA Copilot Agent"

# Check routes via OpenAPI schema (includes router sub-routes)
openapi = app.openapi()
api_paths = list(openapi["paths"].keys())
assert "/api/generate_testcase" in api_paths, f"Missing /api/generate_testcase in {api_paths}"
assert "/api/generate_testcases" in api_paths
assert "/api/health" in api_paths
print(f"  [PASS] App created with {len(api_paths)} API paths: {api_paths}")

# ---------------------------------------------------------------------------
# Test 6: AgentState with verification_report
# ---------------------------------------------------------------------------
print("\n[Test 6] AgentState Verification Field")

from arm_isa_agent.agent.state import AgentState

state: AgentState = {
    "messages": [],
    "user_query": "verify ADD",
    "intent": "verification",
    "plan": [],
    "current_step": 0,
    "tool_results": [],
    "final_answer": "",
    "iteration_count": 0,
    "review_results": [],
    "repair_count": 0,
    "verification_report": {},
}
assert "verification_report" in state
assert state["verification_report"] == {}
print("  [PASS] AgentState includes verification_report field")

# ---------------------------------------------------------------------------
# Test 7: Multi-instruction pipeline
# ---------------------------------------------------------------------------
print("\n[Test 7] Multi-Instruction Pipeline")

for instr in ["LDR"]:
    r = run_verification(instr, sqlite_client=sqlite, llm=None, use_llm=False)
    assert r.instruction == instr
    status_icon = "[PASS]" if r.status in ("PASS", "REPAIRED") else "[OK]"
    print(f"  {status_icon} {instr}: status={r.status}, tests={r.generated_tests}, score={r.review_score:.0f}, duration={r.total_duration_ms:.0f}ms")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("All tests passed! Compiler Verification Agent is ready.")
print("=" * 60)
