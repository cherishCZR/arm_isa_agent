from __future__ import annotations

from pathlib import Path
import json
import re

from arm_isa_agent.assembly.scenario import ScenarioProgramGenerator, ScenarioRequest, make_assembly_symbol
from arm_isa_agent.kb.sqlite.client import SQLiteClient
from arm_isa_agent.resolution import InstructionResolver
from arm_isa_agent.verification import run_verification


class _MockResponse:
    def __init__(self, content: str) -> None:
        self.content = content


class _MockLlm:
    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, _messages: object) -> _MockResponse:
        self.calls += 1
        if self.calls == 1:
            return _MockResponse(json.dumps({"target_queries": ["ADD imm"]}))
        return _MockResponse(json.dumps({"statements": [
            {"line": "add w0, w0, #0, lsl #0", "target_query": "ADD imm"},
            {"line": "nop", "target_query": None},
            {"line": "add w0, w0, #0, lsl #0", "target_query": "ADD imm"},
            {"line": "nop", "target_query": None},
            {"line": "nop", "target_query": None},
            {"line": "ret", "target_query": None},
        ]}))


class _AbsMockLlm:
    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, _messages: object) -> _MockResponse:
        self.calls += 1
        if self.calls == 1:
            return _MockResponse(json.dumps({"target_queries": ["ABS"]}))
        statements = [{"line": "abs w0, w0", "target_query": "ABS"}] * 50
        statements += [{"line": "nop", "target_query": None}] * 49
        statements += [{"line": "ret", "target_query": None}]
        return _MockResponse(json.dumps({"statements": statements}))


class _InvalidLlm:
    def invoke(self, _messages: object) -> _MockResponse:
        return _MockResponse("not json")


class _AliasedAbsMockLlm:
    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, _messages: object) -> _MockResponse:
        self.calls += 1
        if self.calls == 1:
            return _MockResponse(json.dumps({"target_queries": ["ABS", "ABS vector", "ABS sve"]}))
        statements = [{"line": "abs w0, w0", "target_query": "ABS vector"}] * 25
        statements += [{"line": "abs w0, w0", "target_query": "ABS sve"}] * 25
        statements += [{"line": "nop", "target_query": None}] * 49
        statements += [{"line": "ret", "target_query": None}]
        return _MockResponse(json.dumps({"statements": statements}))


class _CompatibleTargetShapeLlm:
    def __init__(self, target_payload: object, first_response_invalid: bool = False) -> None:
        self.target_payload = target_payload
        self.first_response_invalid = first_response_invalid
        self.calls = 0

    def invoke(self, _messages: object) -> _MockResponse:
        self.calls += 1
        if self.calls == 1 and self.first_response_invalid:
            return _MockResponse('{"unexpected":"shape"}')
        if self.calls <= 2 and self.first_response_invalid or self.calls == 1:
            return _MockResponse(json.dumps(self.target_payload))
        return _MockResponse(json.dumps({"statements": [
            {"line": "abs w0, w0", "target_query": "ABS"},
            {"line": "nop", "target_query": None},
            {"line": "abs w0, w0", "target_query": "ABS"},
            {"line": "nop", "target_query": None},
            {"line": "nop", "target_query": None},
            {"line": "ret", "target_query": None},
        ]}))


class _BudgetRepairAbsLlm:
    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, _messages: object) -> _MockResponse:
        self.calls += 1
        if self.calls == 1:
            return _MockResponse(json.dumps({"target_queries": ["ABS"]}))
        count = 52 if self.calls == 2 else 50
        statements = [{"line": "abs w0, w1", "target_query": "ABS"}] * count
        statements += [{"line": "nop", "target_query": None}] * 49
        statements += [{"line": "ret", "target_query": None}]
        return _MockResponse(json.dumps({"statements": statements}))


class _ExplicitTargetRepairLlm:
    """First drops explicit targets, then returns the complete repaired set."""

    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, _messages: object) -> _MockResponse:
        self.calls += 1
        if self.calls == 1:
            return _MockResponse(json.dumps({"target_queries": ["ABS"]}))
        if self.calls == 2:
            return _MockResponse(json.dumps({"target_queries": ["ADD", "SUB", "ABS"]}))
        statements = [{"line": "add w0, w1, #0", "target_query": "ADD"}] * 2
        statements += [{"line": "sub w2, w3, #1", "target_query": "SUB"}] * 2
        statements += [{"line": "abs w4, w5", "target_query": "ABS"}] * 2
        statements += [{"line": "nop", "target_query": None}] * 3
        statements += [{"line": "ret", "target_query": None}]
        return _MockResponse(json.dumps({"statements": statements}))


def _sqlite() -> SQLiteClient:
    db = SQLiteClient("data/sqlite/isa_kb.db")
    db.initialize()
    return db


def test_instruction_resolver_variant_hints() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    resolver = InstructionResolver(_sqlite())

    assert resolver.resolve("ADD imm").selected_xml_id == "ADD_addsub_imm"
    assert resolver.resolve("ADD shift").selected_xml_id == "ADD_addsub_shift"
    assert resolver.resolve("ADD sve").selected_xml_id == "add_z_p_zz"
    assert resolver.resolve("ADDP sve").selected_xml_id == "addp_z_p_zz"


def test_scenario_program_generates_one_assembly_file() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    generator = ScenarioProgramGenerator(_sqlite(), seed=1)
    program = generator.generate_and_verify(
        ScenarioRequest(
            scenario_id="scenario_001",
            raw="ADD imm,ADD shift,mov",
            queries=["ADD imm", "ADD shift", "mov"],
        )
    )

    assert program.generated_status == "PASS"
    assert program.static_review_status == "PASS"
    assert program.test_file is not None
    assert program.test_file["filename"] == "scenario_001.S"
    assert program.test_file["format"] == "s"
    assert "add w0, w0, #0, lsl #0" in program.test_file["content"]
    assert "add w0, w0, w0, lsl #0" in program.test_file["content"]


def test_scenario_program_honors_exact_instruction_and_target_budgets() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    program = ScenarioProgramGenerator(_sqlite(), seed=1).generate_and_verify(
        ScenarioRequest(
            scenario_id="budget_001",
            raw="ADD imm,ADD shift",
            queries=["ADD imm", "ADD shift"],
            program_instruction_count=12,
            target_instruction_count=3,
        )
    )

    assert program.status == "COMPILED"
    assert len(program.statement_metadata) == 12
    assert program._target_counts() == {
        "ADD_addsub_imm": 3,
        "ADD_addsub_shift": 3,
    }


def test_scenario_program_rejects_impossible_budget() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    program = ScenarioProgramGenerator(_sqlite(), seed=1).generate_and_verify(
        ScenarioRequest(
            scenario_id="budget_invalid",
            raw="ADD imm,ADD shift",
            queries=["ADD imm", "ADD shift"],
            program_instruction_count=6,
            target_instruction_count=3,
        )
    )

    assert program.status == "FAILED"
    assert any(issue["type"] == "invalid_budget" for issue in program.issues)


def test_llm_mode_uses_descriptive_request_and_never_falls_back_to_rules() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    llm = _MockLlm()
    program = ScenarioProgramGenerator(_sqlite(), seed=1, llm=llm).generate_and_verify(
        ScenarioRequest(
            scenario_id="llm_001",
            raw="Generate a small ADD immediate compilation test",
            program_instruction_count=6,
            target_instruction_count=2,
            generation_mode="llm",
        )
    )

    assert llm.calls == 2
    assert program.status == "COMPILED"
    assert program.generation_mode == "llm"
    assert program._target_counts() == {"ADD_addsub_imm": 2}


def test_abs_llm_program_enables_cssc_from_xml_feature_dependency() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    program = ScenarioProgramGenerator(_sqlite(), llm=_AbsMockLlm()).generate_and_verify(
        ScenarioRequest(
            scenario_id="abs_llm_001",
            raw="Generate random ABS instruction tests",
            program_instruction_count=100,
            target_instruction_count=50,
            generation_mode="llm",
        )
    )

    assert program.status == "COMPILED"
    assert program.required_features == ["FEAT_CSSC"]
    assert program._target_counts() == {"ABS": 50}
    assert "+cssc" in " ".join(program.compile_summary.results[0].command)


def test_llm_aliases_merge_into_one_canonical_xml_target() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    program = ScenarioProgramGenerator(_sqlite(), llm=_AliasedAbsMockLlm()).generate_and_verify(
        ScenarioRequest(
            scenario_id="abs_alias_001",
            raw="Generate random ABS instruction tests",
            program_instruction_count=100,
            target_instruction_count=50,
            generation_mode="llm",
        )
    )

    assert program.status == "COMPILED"
    assert len(program.targets) == 1
    assert program.targets[0].key == "ABS"
    assert program.targets[0].aliases == ["ABS", "ABS vector", "ABS sve"]
    assert program._target_counts() == {"ABS": 50}
    assert not any(issue["type"] == "duplicate_target" for issue in program.issues)


def test_llm_target_payload_compatibility_and_protocol_retry() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    payloads = [
        ["ABS"],
        {"targets": ["ABS"]},
        {"instructions": ["ABS"]},
        {"target_queries": ["ABS"]},
    ]
    for index, payload in enumerate(payloads):
        program = ScenarioProgramGenerator(_sqlite(), llm=_CompatibleTargetShapeLlm(payload)).generate_and_verify(
            ScenarioRequest(
                scenario_id=f"compatible_{index}",
                raw="Generate ABS tests",
                program_instruction_count=6,
                target_instruction_count=2,
                generation_mode="llm",
            )
        )
        assert program.status == "COMPILED"
        assert program._target_counts() == {"ABS": 2}

    retried = ScenarioProgramGenerator(
        _sqlite(), llm=_CompatibleTargetShapeLlm({"target_queries": ["ABS"]}, first_response_invalid=True)
    ).generate_and_verify(
        ScenarioRequest(
            scenario_id="compatible_retry",
            raw="Generate ABS tests",
            program_instruction_count=6,
            target_instruction_count=2,
            generation_mode="llm",
        )
    )
    assert retried.status == "COMPILED"
    assert any("protocol-correction retry" in entry for entry in retried.generation_trace)


def test_llm_budget_repair_uses_second_full_program_without_silent_truncation() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    llm = _BudgetRepairAbsLlm()
    program = ScenarioProgramGenerator(_sqlite(), llm=llm).generate_and_verify(
        ScenarioRequest(
            scenario_id="budget_repair_abs",
            raw="Generate random ABS tests",
            program_instruction_count=100,
            target_instruction_count=50,
            generation_mode="llm",
        )
    )

    assert llm.calls == 3
    assert program.status == "COMPILED"
    assert len(program.statement_metadata) == 100
    assert program._target_counts() == {"ABS": 50}
    assert any("budget-correction retry" in entry for entry in program.generation_trace)


def test_llm_repairs_omitted_explicit_targets_from_chinese_request() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    llm = _ExplicitTargetRepairLlm()
    program = ScenarioProgramGenerator(_sqlite(), llm=llm).generate_and_verify(
        ScenarioRequest(
            scenario_id="explicit_target_repair",
            raw="生成ADD，sub，ABS指令的随机测试",
            program_instruction_count=10,
            target_instruction_count=2,
            generation_mode="llm",
        )
    )

    assert llm.calls == 3
    assert program.status == "COMPILED"
    assert [target.canonical_query for target in program.targets] == ["ADD", "SUB", "ABS"]
    assert program._target_counts() == {"ADD_addsub_imm": 2, "SUB_addsub_imm": 2, "ABS": 2}
    assert any("Explicit targets detected" in entry for entry in program.generation_trace)
    assert any("omitted explicit targets" in entry for entry in program.generation_trace)


def test_scenario_generation_reports_live_pipeline_progress() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    events: list[tuple[str, str, str, dict[str, object]]] = []
    program = ScenarioProgramGenerator(
        _sqlite(),
        llm=_MockLlm(),
        progress_callback=lambda stage, event, message, snapshot: events.append((stage, event, message, snapshot)),
    ).generate_and_verify(
        ScenarioRequest(
            scenario_id="progress_llm_001",
            raw="Generate a small ADD immediate compilation test",
            program_instruction_count=6,
            target_instruction_count=2,
            generation_mode="llm",
        )
    )

    assert program.status == "COMPILED"
    assert ("planner", "start") in [(stage, event) for stage, event, _, _ in events]
    assert ("retrieval", "complete") in [(stage, event) for stage, event, _, _ in events]
    assert ("llm", "progress") in [(stage, event) for stage, event, _, _ in events]
    assert ("generator", "complete") in [(stage, event) for stage, event, _, _ in events]
    assert ("reviewer", "complete") in [(stage, event) for stage, event, _, _ in events]
    assert ("compiler", "complete") in [(stage, event) for stage, event, _, _ in events]
    assert any("fixed assembly slots" in message for _, _, message, _ in events)


def test_assembly_symbols_and_content_are_ascii_for_chinese_request() -> None:
    symbol = make_assembly_symbol("随机生成ABS指令的测试", prefix="single_instruction")
    assert symbol.isascii()
    assert symbol.startswith("single_instruction_")

    if not Path("data/sqlite/isa_kb.db").exists():
        return
    program = ScenarioProgramGenerator(_sqlite(), llm=_AbsMockLlm()).generate_and_verify(
        ScenarioRequest(
            scenario_id="随机生成ABS指令的测试",
            raw="随机生成ABS指令的测试",
            program_instruction_count=100,
            target_instruction_count=50,
            generation_mode="llm",
        )
    )
    assert program.status == "COMPILED"
    assert program.test_file is not None
    assert program.test_file["filename"].isascii()
    assert program.test_file["content"].isascii()


def test_invalid_llm_response_is_reported_without_orchestration_exception() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    program = ScenarioProgramGenerator(_sqlite(), llm=_InvalidLlm()).generate_and_verify(
        ScenarioRequest(
            scenario_id="bad_llm_001",
            raw="Generate ABS tests",
            program_instruction_count=10,
            target_instruction_count=2,
            generation_mode="llm",
        )
    )

    assert program.status == "FAILED"
    assert program.test_file is None
    assert any(issue["type"] == "llm_target_error" for issue in program.issues)


def test_single_instruction_rule_verification_uses_xml_scenario_suite() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    report = run_verification("ADD", sqlite_client=_sqlite(), llm=None, use_llm=False)

    assert report.status == "COMPILED"
    assert report.verification_level == "compiled"
    assert report.compile_status == "PASS"
    assert len(report.test_files) >= 4
    assert {entry.test_type for entry in report.test_files} >= {
        "normal_assembly", "register_dependency_chain", "register_aliasing", "immediate_boundary",
    }
    assert {entry.format for entry in report.test_files} >= {"s", "c", "cpp"}
    assert report.scenario_plan
    assert all(item["status"] == "compiled" for item in report.scenario_plan)
    content = next(entry.content for entry in report.test_files if entry.test_type == "normal_assembly")
    assert "add " in content.lower()
    assert "uint64_t" not in content
    assert "<" not in content


def test_advsimd_pair_template_binds_register_fragments_and_varies_operands() -> None:
    if not Path("data/sqlite/isa_kb.db").exists():
        return
    report = run_verification(
        "ADDP",
        sqlite_client=_sqlite(),
        llm=None,
        use_llm=False,
        instruction_count=20,
        target_instruction_count=8,
    )

    assert report.status == "COMPILED"
    normal = next(entry for entry in report.test_files if entry.test_type == "normal_assembly")
    target_lines = [
        line.strip() for line in normal.content.splitlines()[4:]
        if line.strip() not in {"nop", "ret"}
    ]
    assert len(target_lines) == 8
    assert len(set(target_lines)) >= 4
    assert all(re.search(r"\bdd\d+\b", line.lower()) is None for line in target_lines)
    assert all(".2d.2d" not in line.lower() and ".4s.2d" not in line.lower() for line in target_lines)
    assert all("v" in line.lower() and ".2d" in line.lower() for line in target_lines)
