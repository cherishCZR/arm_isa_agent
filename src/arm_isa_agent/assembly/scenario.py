"""Scenario parsing and exact-budget AArch64 assembly program generation."""

from __future__ import annotations

import json
import random
import re
import traceback
from hashlib import sha256
from dataclasses import dataclass, field
from typing import Any, Callable

import structlog
from pydantic import BaseModel, ValidationError

from arm_isa_agent.assembly.instantiator import AssemblyInstantiator
from arm_isa_agent.compile.verifier import CompileVerifier
from arm_isa_agent.kb.sqlite.models import InstructionModel
from arm_isa_agent.planning.analyzer import InstructionAnalyzer
from arm_isa_agent.planning.models import InstructionProfile
from arm_isa_agent.resolution.resolver import InstructionResolver, ResolutionResult
from arm_isa_agent.verification.models import CompileSummary

logger = structlog.get_logger(__name__)


class LlmTargetPlan(BaseModel):
    """Validated target-extraction response from the LLM."""

    target_queries: list[str]


class LlmAssemblyStatement(BaseModel):
    """One executable assembly instruction produced by the LLM."""

    line: str
    target_key: str | None = None
    # Kept for compatibility with responses from the previous schema.
    target_query: str | None = None


class LlmAssemblyProgram(BaseModel):
    """Validated assembly-generation response from the LLM."""

    statements: list[LlmAssemblyStatement] | None = None
    slots: list["LlmAssemblySlot"] | None = None


class LlmAssemblySlot(LlmAssemblyStatement):
    """An LLM-provided instruction for one server-owned program slot."""

    index: int


class LlmProtocolError(ValueError):
    """A model response was valid JSON but not a supported target-plan shape."""


@dataclass
class ScenarioRequest:
    scenario_id: str
    raw: str
    queries: list[str] = field(default_factory=list)
    program_instruction_count: int = 100
    target_instruction_count: int = 1
    generation_mode: str = "rule_based"


@dataclass
class CanonicalTarget:
    """One unique XML instruction target, optionally reached via many aliases."""

    key: str
    canonical_query: str
    aliases: list[str]
    profile: InstructionProfile
    resolution: ResolutionResult


@dataclass(frozen=True)
class ProgramSlot:
    """A fixed executable-instruction position owned by the server."""

    index: int
    kind: str
    target_key: str | None = None


_ASSEMBLY_SYMBOL_RE = re.compile(r"^[A-Za-z_.$][A-Za-z0-9_.$]*$")
_EXPLICIT_HINTS = ("sve2", "shift", "extend", "imm", "sve", "simd", "base", "alias", "branch", "load", "store", "sme", "mops", "ls64")


def make_assembly_symbol(raw: str, prefix: str = "single") -> str:
    """Return a deterministic ASCII-only symbol safe for GNU/LLVM assembly."""
    ascii_raw = raw.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^A-Za-z0-9_]", "_", ascii_raw).strip("_")
    if slug and raw.isascii():
        return f"{prefix}_{slug}"
    return f"{prefix}_{sha256(raw.encode('utf-8')).hexdigest()[:12]}"


@dataclass
class ScenarioProgram:
    scenario_id: str
    raw: str
    queries: list[str]
    program_instruction_count: int
    target_instruction_count: int
    generation_mode: str
    resolved: list[dict[str, Any]] = field(default_factory=list)
    statement_metadata: list[dict[str, Any]] = field(default_factory=list)
    generation_trace: list[str] = field(default_factory=list)
    required_features: list[str] = field(default_factory=list)
    targets: list[CanonicalTarget] = field(default_factory=list)
    test_file: dict[str, Any] | None = None
    generated_status: str = "FAIL"
    static_review_status: str = "SKIPPED"
    compile_status: str = "SKIPPED"
    status: str = "FAILED"
    issues: list[dict[str, Any]] = field(default_factory=list)
    compile_summary: CompileSummary = field(default_factory=CompileSummary)

    def to_result_event(self, duration_ms: float) -> dict[str, Any]:
        test_files = [self.test_file] if self.test_file else []
        return {
            "instruction": self.raw,
            "status": self.status,
            "review_score": 100.0 if self.static_review_status in {"PASS", "WARNING"} else 0.0,
            "total_tests": self.program_instruction_count,
            "passing_tests": 1 if self.status == "COMPILED" else 0,
            "failing_tests": 0 if self.status == "COMPILED" else 1,
            "total_duration_ms": duration_ms,
            "stage_details": [],
            "test_files": test_files,
            "coverage": {
                "generated": 100.0 if self.generated_status == "PASS" else 0.0,
                "statically_reviewed": 100.0 if self.static_review_status in {"PASS", "WARNING"} else 0.0,
                "compiled": 100.0 if self.compile_status == "PASS" else 0.0,
            },
            "issues": self.issues,
            "verification_level": self._verification_level(),
            "generated_status": self.generated_status,
            "static_review_status": self.static_review_status,
            "compile_status": self.compile_status,
            "compile_results": [r.model_dump() for r in self.compile_summary.results],
            "resolved": self.resolved,
            "generation_mode": self.generation_mode,
            "generation_trace": self.generation_trace,
            "required_features": self.required_features,
            "canonical_targets": [
                {"key": target.key, "query": target.canonical_query, "aliases": target.aliases}
                for target in self.targets
            ],
            "budget": {
                "program_instruction_count": self.program_instruction_count,
                "target_instruction_count": self.target_instruction_count,
                "actual_instruction_count": len(self.statement_metadata),
                "target_counts": self._target_counts(),
            },
        }

    def _target_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for statement in self.statement_metadata:
            key = statement.get("target_key")
            if key:
                counts[key] = counts.get(key, 0) + 1
        return counts

    def _verification_level(self) -> str:
        if self.compile_status == "PASS":
            return "compiled"
        if self.static_review_status in {"PASS", "WARNING"}:
            return "statically_reviewed"
        return "generated"


def parse_scenario_text(text: str) -> list[ScenarioRequest]:
    """Parse one-row-per-scenario text into structured rule-based requests."""
    scenarios: list[ScenarioRequest] = []
    for line in text.splitlines():
        raw = line.strip()
        if not raw:
            continue
        queries = [part.strip() for part in raw.split(",") if part.strip()]
        if queries:
            scenarios.append(ScenarioRequest(
                scenario_id=f"scenario_{len(scenarios) + 1:03d}", raw=raw, queries=queries,
            ))
    return scenarios


class ScenarioProgramGenerator:
    """Generate one complete assembly program with an exact instruction budget."""

    def __init__(
        self,
        sqlite_client: Any,
        seed: int | None = None,
        llm: Any = None,
        progress_callback: Callable[[str, str, str, dict[str, Any]], None] | None = None,
    ) -> None:
        self._sqlite = sqlite_client
        self._resolver = InstructionResolver(sqlite_client)
        self._analyzer = InstructionAnalyzer(sqlite_client)
        self._instantiator = AssemblyInstantiator(seed=seed)
        self._compiler = CompileVerifier()
        self._llm = llm
        self._rng = random.Random(seed)
        self._progress_callback = progress_callback
        self._known_mnemonics: tuple[str, ...] | None = None

    def _progress(self, stage: str, event: str, message: str, **snapshot: Any) -> None:
        """Publish execution progress without coupling generation to SSE transport."""
        if self._progress_callback is not None:
            self._progress_callback(stage, event, message, snapshot)

    def generate_and_verify(self, scenario: ScenarioRequest) -> ScenarioProgram:
        self._progress(
            "planner", "start", "Planning exact assembly program budget",
            program_instruction_count=scenario.program_instruction_count,
            target_instruction_count=scenario.target_instruction_count,
        )
        program = self.generate(scenario)
        self._progress(
            "planner", "complete", "Program budget accepted",
            program_instruction_count=scenario.program_instruction_count,
            target_instruction_count=scenario.target_instruction_count,
        )
        if program.generated_status != "PASS":
            program.static_review_status = "SKIPPED"
            program.compile_status = "SKIPPED"
            program.status = self._overall_status(program)
            self._progress("generator", "complete", "Assembly generation failed", status="error")
            self._progress("reviewer", "complete", "Static review skipped because generation failed", status="skipped")
            self._progress("compiler", "complete", "Compile-only validation skipped because generation failed", status="skipped")
            return program
        self._progress("reviewer", "start", "Running static review on generated assembly")
        program.issues.extend(self.static_review(program))
        program.static_review_status = "PASS" if not program.issues else "FAIL"
        self._progress(
            "reviewer", "complete",
            "Static review passed" if program.static_review_status == "PASS" else "Static review failed",
            status="ok" if program.static_review_status == "PASS" else "error",
            issue_count=len(program.issues),
        )
        if program.test_file and program.static_review_status == "PASS":
            self._progress("compiler", "start", "Compiling generated AArch64 assembly")
            program.compile_summary = self._compiler.verify_files([program.test_file])
            program.compile_status = program.compile_summary.status
            self._progress(
                "compiler", "complete",
                "Compile-only validation passed" if program.compile_status == "PASS" else "Compile-only validation failed",
                status="ok" if program.compile_status == "PASS" else "error",
                compile_status=program.compile_status,
            )
        else:
            self._progress("compiler", "complete", "Compile-only validation skipped after static review", status="skipped")
        program.status = self._overall_status(program)
        if program.test_file:
            program.test_file["status"] = "pass" if program.status in {"COMPILED", "REVIEWED", "GENERATED"} else "fail"
            program.test_file["issue_count"] = len(program.issues)
        return program

    def generate(self, scenario: ScenarioRequest) -> ScenarioProgram:
        program = ScenarioProgram(
            scenario_id=scenario.scenario_id,
            raw=scenario.raw,
            queries=list(scenario.queries),
            program_instruction_count=scenario.program_instruction_count,
            target_instruction_count=scenario.target_instruction_count,
            generation_mode=scenario.generation_mode,
        )
        if scenario.program_instruction_count < 1 or scenario.target_instruction_count < 1:
            self._issue(program, "invalid_budget", "Instruction counts must be positive integers")
            return program
        if scenario.target_instruction_count > scenario.program_instruction_count:
            self._issue(program, "invalid_budget", "Target instruction count cannot exceed total program instruction count")
            return program

        if scenario.generation_mode == "llm":
            return self._generate_with_llm(program)
        return self._generate_rule_based(program)

    def _generate_rule_based(self, program: ScenarioProgram) -> ScenarioProgram:
        self._progress("llm", "complete", "LLM generation disabled; using XML rule-based generation", status="skipped")
        if not program.queries:
            self._issue(program, "resolution_error", "At least one instruction query is required in rule-based mode")
            return program
        self._progress("retrieval", "start", "Resolving XML instruction variants")
        program.generation_trace.append("Resolved XML instruction variants for rule-based generation")
        resolved_targets = self._resolve_targets(program, program.queries)
        if not resolved_targets:
            self._progress("retrieval", "complete", "Instruction resolution failed", status="error")
            return program
        self._progress(
            "retrieval", "complete", f"Resolved {len(resolved_targets)} XML instruction target(s)",
            status="ok", targets=[target.canonical_query for target in resolved_targets],
        )

        required_target_count = len(resolved_targets) * program.target_instruction_count
        # RET is always executable and part of the user-visible program budget.
        if required_target_count + 1 > program.program_instruction_count:
            self._issue(
                program,
                "invalid_budget",
                f"Budget {program.program_instruction_count} cannot hold {required_target_count} target instances plus RET",
            )
            return program

        target_statements: list[dict[str, Any]] = []
        for target in resolved_targets:
            # Use one XML-instantiated legal form repeatedly for the requested
            # occurrence budget. Candidate diversification belongs behind a
            # compile-filter; otherwise later salts can produce invalid immediates.
            candidate = self._instantiator.instantiate_profile(target.profile, 1)[0]
            for _ in range(program.target_instruction_count):
                target_statements.append({
                    "instruction": candidate.instruction,
                    "target_key": target.key,
                    "target_query": target.canonical_query,
                    "xml_id": target.key,
                    "kind": "target",
                })
                for diag in candidate.diagnostics:
                    self._issue(program, "generation_warning", diag, severity="medium", location=target.canonical_query)

        self._progress("generator", "start", "Instantiating legal XML assembly templates")
        self._rng.shuffle(target_statements)
        program.statement_metadata.extend(target_statements)
        filler_count = program.program_instruction_count - len(target_statements) - 1
        program.statement_metadata.extend({"instruction": "nop", "kind": "filler"} for _ in range(filler_count))
        self._rng.shuffle(program.statement_metadata)
        program.statement_metadata.append({"instruction": "ret", "kind": "terminator"})
        program.generation_trace.append(
            f"Generated {len(target_statements)} target instances and {filler_count} legal filler instructions"
        )
        self._build_file(program)
        self._progress(
            "generator", "complete", f"Generated {program.test_file['filename']}" if program.test_file else "Assembly generation failed",
            status="ok" if program.test_file else "error", actual_instruction_count=len(program.statement_metadata),
        )
        return program

    def _generate_with_llm(self, program: ScenarioProgram) -> ScenarioProgram:
        self._progress("llm", "start", "Calling LLM to extract requested instruction targets")
        if self._llm is None:
            self._issue(program, "llm_unavailable", "LLM generation was requested, but no LLM service is configured")
            return program
        program.generation_trace.append("LLM target extraction requested")
        target_queries = list(program.queries)
        if not target_queries:
            explicit_queries = self._extract_explicit_target_queries(program.raw)
            if explicit_queries:
                program.generation_trace.append(
                    "Explicit targets detected from user input: " + ", ".join(explicit_queries)
                )
                self._progress(
                    "llm", "progress", "Explicit instruction targets detected: " + ", ".join(explicit_queries),
                    explicit_targets=explicit_queries,
                )
            target_queries, error, trace = self._llm_target_queries(program.raw, explicit_queries)
            program.generation_trace.extend(trace)
            if error:
                self._issue(program, "llm_target_error", error, dimension="llm")
                self._progress("llm", "complete", error, status="error")
                return program
            if explicit_queries:
                missing = self._missing_explicit_targets(explicit_queries, target_queries)
                if missing:
                    program.generation_trace.append(
                        "LLM omitted explicit targets: " + ", ".join(missing)
                    )
                    self._progress(
                        "llm", "progress", "LLM omitted explicit targets; requesting target extraction repair: " + ", ".join(missing),
                        missing_targets=missing,
                    )
                    target_queries, error, repair_trace = self._llm_target_queries(
                        program.raw,
                        explicit_queries,
                        missing_targets=missing,
                    )
                    program.generation_trace.extend(repair_trace)
                    if error:
                        self._issue(program, "llm_target_omission", error, dimension="llm")
                        self._progress("llm", "complete", error, status="error")
                        return program
                    still_missing = self._missing_explicit_targets(explicit_queries, target_queries)
                    if still_missing:
                        message = "LLM target repair omitted explicit targets: " + ", ".join(still_missing)
                        self._issue(program, "llm_target_omission", message, dimension="llm")
                        self._progress("llm", "complete", message, status="error", missing_targets=still_missing)
                        return program
        if not target_queries:
            self._issue(program, "llm_target_error", "LLM did not return any ARM instruction targets")
            self._progress("llm", "complete", "LLM did not return any ARM instruction targets", status="error")
            return program
        self._progress("retrieval", "start", "Resolving LLM-selected XML instruction targets")
        resolved_targets = self._resolve_targets(program, target_queries)
        if not resolved_targets:
            self._progress("retrieval", "complete", "Instruction resolution failed", status="error")
            return program
        self._progress(
            "retrieval", "complete", f"Resolved {len(resolved_targets)} XML instruction target(s)",
            status="ok", targets=[target.canonical_query for target in resolved_targets],
        )
        required_target_count = len(resolved_targets) * program.target_instruction_count
        if required_target_count + 1 > program.program_instruction_count:
            self._issue(
                program, "invalid_budget",
                f"Budget {program.program_instruction_count} cannot hold {required_target_count} target instances plus RET",
            )
            return program

        target_info = []
        for target in resolved_targets:
            profile = target.profile
            encoding = next((item for item in profile.encodings if item is not None), None)
            target_info.append({
                "key": target.key,
                "query": target.canonical_query,
                "aliases": target.aliases,
                "xml_id": profile.xml_id,
                "mnemonic": profile.mnemonic,
                "template": encoding.assembly_template if encoding else "",
                "required_features": [feature.feature_name for feature in profile.feature_dependencies],
            })
        slots = self._build_slot_layout(program, resolved_targets)
        program.generation_trace.append(f"Server allocated {len(slots)} fixed assembly slots")
        target_slots = {target.canonical_query: program.target_instruction_count for target in resolved_targets}
        self._progress(
            "llm", "progress",
            (
                f"Server allocated {len(slots)} fixed assembly slots: "
                f"targets {', '.join(f'{query}={count}' for query, count in target_slots.items())}; "
                f"NOP={sum(slot.kind == 'filler' for slot in slots)}; RET=1"
            ),
            total_slots=len(slots), target_slots=target_slots,
            filler_slots=sum(slot.kind == "filler" for slot in slots), terminator_slots=1,
        )
        candidates, slot_ordered, error = self._request_llm_assembly(program, target_info, slots)
        if error:
            self._issue(program, "llm_output_error", error, dimension="llm")
            self._progress("llm", "complete", error, status="error")
            return program
        validation_errors = self._validate_llm_slots(candidates, slots, resolved_targets, enforce_slot_order=slot_ordered)
        if validation_errors:
            program.generation_trace.append("LLM assembly output needed one budget-correction retry")
            self._progress("llm", "progress", "LLM output failed slot validation; requesting one complete repair", validation_errors=validation_errors)
            candidates, slot_ordered, error = self._request_llm_assembly(
                program, target_info, slots, validation_errors=validation_errors,
            )
            if error:
                self._issue(program, "llm_budget_error", error, dimension="llm")
                self._progress("llm", "complete", error, status="error")
                return program
            validation_errors = self._validate_llm_slots(candidates, slots, resolved_targets, enforce_slot_order=slot_ordered)
            if validation_errors:
                self._issue(
                    program,
                    "llm_budget_error",
                    "LLM assembly output still violates the fixed program specification: " + "; ".join(validation_errors[:3]),
                    dimension="llm",
                )
                self._progress("llm", "complete", "LLM repair still violates the fixed program specification", status="error", validation_errors=validation_errors)
                return program

        candidates = self._arrange_candidates_for_slots(candidates, slots, resolved_targets)
        for slot, item in zip(slots, candidates, strict=True):
            target = next((entry for entry in resolved_targets if entry.key == slot.target_key), None)
            program.statement_metadata.append({
                "instruction": item.line.strip(),
                "target_key": slot.target_key,
                "target_query": target.canonical_query if target else None,
                "kind": slot.kind,
            })
        program.generation_trace.append(f"LLM returned a validated {len(program.statement_metadata)}-instruction program")
        self._progress("llm", "complete", f"LLM returned a validated {len(program.statement_metadata)}-instruction program", status="ok")
        self._progress("generator", "start", "Writing validated assembly program")
        self._build_file(program)
        self._progress(
            "generator", "complete", f"Generated {program.test_file['filename']}" if program.test_file else "Assembly generation failed",
            status="ok" if program.test_file else "error", actual_instruction_count=len(program.statement_metadata),
        )
        return program

    def _build_slot_layout(
        self,
        program: ScenarioProgram,
        targets: list[CanonicalTarget],
    ) -> list[ProgramSlot]:
        slots = [
            ProgramSlot(index=-1, kind="target", target_key=target.key)
            for target in targets
            for _ in range(program.target_instruction_count)
        ]
        filler_count = program.program_instruction_count - len(slots) - 1
        slots.extend(ProgramSlot(index=-1, kind="filler") for _ in range(filler_count))
        self._rng.shuffle(slots)
        slots.append(ProgramSlot(index=-1, kind="terminator"))
        return [ProgramSlot(index=index, kind=slot.kind, target_key=slot.target_key) for index, slot in enumerate(slots)]

    def _request_llm_assembly(
        self,
        program: ScenarioProgram,
        target_info: list[dict[str, Any]],
        slots: list[ProgramSlot],
        validation_errors: list[str] | None = None,
    ) -> tuple[list[LlmAssemblySlot], bool, str | None]:
        repair = validation_errors is not None
        system_prompt = "You fill server-owned AArch64 assembly slots. Return strict JSON only, without Markdown."
        request = {
            "user_request": program.raw,
            "targets": target_info,
            "slots": [slot.__dict__ for slot in slots],
            "required_response": {
                "slots": [{"index": 0, "line": "assembly instruction", "target_key": "ABS or null"}],
            },
            "rules": [
                "Return exactly one object containing slots.",
                "Return every slot exactly once, in ascending index order.",
                "For target slots, use the given target_key and its instruction mnemonic.",
                "For filler slots, use exactly nop with target_key null.",
                "For the terminator slot, use exactly ret with target_key null.",
                "Do not emit directives, labels, comments, non-ASCII characters, prose, or extra slots.",
            ],
        }
        if repair:
            request["previous_validation_errors"] = validation_errors
            request["instruction"] = "Return the complete corrected slot program; do not return a patch."

        payload, error = self._invoke_llm_json("assembly_budget_repair" if repair else "assembly_generation", system_prompt, json.dumps(request, ensure_ascii=False))
        if error:
            return [], False, error
        try:
            llm_program = LlmAssemblyProgram.model_validate(payload)
        except ValidationError as exc:
            return [], False, f"LLM assembly response failed schema validation: {exc.errors()[0]['msg']}"

        if llm_program.slots is not None:
            return llm_program.slots, True, None
        if llm_program.statements is not None:
            # Compatibility with the previous response contract. It is still
            # validated against the fixed layout and is never silently trimmed.
            return [
                LlmAssemblySlot(index=index, **statement.model_dump())
                for index, statement in enumerate(llm_program.statements)
            ], False, None
        return [], False, "LLM assembly response must contain slots or statements"

    @staticmethod
    def _validate_llm_slots(
        candidates: list[LlmAssemblySlot],
        slots: list[ProgramSlot],
        targets: list[CanonicalTarget],
        enforce_slot_order: bool,
    ) -> list[str]:
        errors: list[str] = []
        if len(candidates) != len(slots):
            errors.append(f"expected {len(slots)} instructions, received {len(candidates)}")
            return errors

        alias_to_key = {alias: target.key for target in targets for alias in target.aliases}
        target_by_key = {target.key: target for target in targets}
        expected_counts = {target.key: 0 for target in targets}
        filler_count = 0
        terminator_count = 0
        for position, candidate in enumerate(candidates):
            slot = slots[position] if enforce_slot_order else None
            if slot is not None and candidate.index != slot.index:
                errors.append(f"slot {slot.index} is missing or out of order")
                continue
            line = candidate.line.strip()
            if not line.isascii() or not line or line.startswith((".", "//", ";", "#")) or line.endswith(":"):
                errors.append(f"instruction {position} contains an invalid assembly statement")
                continue
            reported_key = candidate.target_key or alias_to_key.get(candidate.target_query or "")
            head = line.split(None, 1)[0].lower()
            if reported_key is not None:
                target = target_by_key.get(reported_key)
                if target is None:
                    errors.append(f"instruction {position} uses unknown target key {reported_key}")
                elif head != target.profile.mnemonic.lower():
                    errors.append(f"instruction {position} tagged {reported_key} must use mnemonic {target.profile.mnemonic.lower()}")
                else:
                    expected_counts[reported_key] += 1
            elif line.lower() == "nop":
                filler_count += 1
            elif line.lower() == "ret":
                terminator_count += 1
                if position != len(candidates) - 1 and enforce_slot_order:
                    errors.append("terminator ret must be the final slot")
            else:
                errors.append(f"instruction {position} is neither a target, nop filler, nor ret terminator")

            if slot is not None:
                if slot.kind == "target" and reported_key != slot.target_key:
                    errors.append(f"slot {slot.index} must be tagged as target {slot.target_key}")
                elif slot.kind == "filler" and (reported_key is not None or line.lower() != "nop"):
                    errors.append(f"slot {slot.index} must be filler nop with no target key")
                elif slot.kind == "terminator" and (reported_key is not None or line.lower() != "ret"):
                    errors.append(f"slot {slot.index} must be final ret with no target key")
        for key, count in expected_counts.items():
            expected = sum(1 for slot in slots if slot.target_key == key)
            if count != expected:
                errors.append(f"target {key} appears {count} times; expected {expected}")
        expected_fillers = sum(1 for slot in slots if slot.kind == "filler")
        if filler_count != expected_fillers:
            errors.append(f"nop filler count is {filler_count}; expected {expected_fillers}")
        if terminator_count != 1:
            errors.append(f"ret terminator count is {terminator_count}; expected 1")
        return errors

    @staticmethod
    def _arrange_candidates_for_slots(
        candidates: list[LlmAssemblySlot],
        slots: list[ProgramSlot],
        targets: list[CanonicalTarget],
    ) -> list[LlmAssemblySlot]:
        """Place a validated legacy statement list into the server-owned layout."""
        alias_to_key = {alias: target.key for target in targets for alias in target.aliases}
        grouped: dict[str | None, list[LlmAssemblySlot]] = {target.key: [] for target in targets}
        grouped[None] = []
        terminators: list[LlmAssemblySlot] = []
        for candidate in candidates:
            line = candidate.line.strip().lower()
            key = candidate.target_key or alias_to_key.get(candidate.target_query or "")
            if key is not None:
                grouped[key].append(candidate)
            elif line == "ret":
                terminators.append(candidate)
            else:
                grouped[None].append(candidate)
        ordered: list[LlmAssemblySlot] = []
        for slot in slots:
            if slot.kind == "target":
                item = grouped[slot.target_key].pop(0)
            elif slot.kind == "terminator":
                item = terminators.pop(0)
            else:
                item = grouped[None].pop(0)
            ordered.append(item.model_copy(update={"index": slot.index}))
        return ordered

    def _llm_target_queries(
        self,
        raw: str,
        explicit_targets: list[str] | None = None,
        missing_targets: list[str] | None = None,
    ) -> tuple[list[str], str | None, list[str]]:
        """Extract target queries with one protocol-correction retry."""
        explicit_targets = explicit_targets or []
        repair = missing_targets is not None
        system_prompt = (
            "Extract only AArch64 instruction families explicitly requested by the user. "
            "Do not invent scalar, vector, or SVE variants. When explicit_targets is provided, "
            "include every listed target exactly once. Return strict JSON only."
        )
        example_targets = explicit_targets or ["<instruction>"]
        initial_prompt = json.dumps({
            "user_request": raw,
            "explicit_targets": explicit_targets,
            "required_response": {"target_queries": example_targets},
            "rules": [
                "Return exactly one JSON object.",
                "Use the key target_queries containing one or more non-empty strings.",
                "Include every explicit_targets entry exactly once when supplied.",
                "Do not add unrelated instruction families.",
                "Do not return a top-level array, Markdown, prose, targets, or instructions.",
            ],
        }, ensure_ascii=False)
        if repair:
            retry_prompt = json.dumps({
                "user_request": raw,
                "explicit_targets": explicit_targets,
                "previous_missing_targets": missing_targets,
                "instruction": "Return the complete corrected target set. Every explicit target is mandatory.",
                "required_response": {"target_queries": example_targets},
            }, ensure_ascii=False)
        else:
            retry_prompt = json.dumps({
                "user_request": raw,
                "explicit_targets": explicit_targets,
                "instruction": "The previous response did not match the JSON protocol. Return only the complete required object.",
                "required_response": {"target_queries": example_targets},
            }, ensure_ascii=False)
        trace: list[str] = []
        last_error = "LLM did not return a valid target plan"

        for attempt, prompt in enumerate((initial_prompt, retry_prompt), 1):
            payload, error = self._invoke_llm_json("target_extraction_repair" if repair else "target_extraction", system_prompt, prompt)
            if error:
                last_error = error
            else:
                try:
                    normalized, normalized_from = self._normalize_target_plan_payload(payload)
                    plan = LlmTargetPlan.model_validate(normalized)
                    queries = [query.strip() for query in plan.target_queries if query.strip()]
                    if not queries:
                        raise LlmProtocolError("target_queries must contain at least one non-empty string")
                    if normalized_from:
                        trace.append(f"Normalized LLM target response from {normalized_from}")
                    trace.append("LLM returned target queries: " + ", ".join(queries))
                    return queries, None, trace
                except (LlmProtocolError, ValidationError) as exc:
                    last_error = f"LLM target response failed schema validation: {self._protocol_error_message(exc)}"

            if attempt == 1:
                trace.append(
                    "LLM target repair response needed one protocol-correction retry"
                    if repair else "LLM target response needed one protocol-correction retry"
                )

        return [], last_error, trace

    def _extract_explicit_target_queries(self, raw: str) -> list[str]:
        """Find user-written mnemonics from the XML-backed SQLite vocabulary."""
        if self._known_mnemonics is None:
            with self._sqlite.session() as session:
                self._known_mnemonics = tuple(sorted({
                    row[0].upper()
                    for row in session.query(InstructionModel.mnemonic).distinct().all()
                    if row[0]
                }, key=len, reverse=True))

        matches: list[tuple[int, str]] = []
        for mnemonic in self._known_mnemonics:
            pattern = re.compile(rf"(?<![A-Za-z0-9_.]){re.escape(mnemonic)}(?![A-Za-z0-9_.])", re.IGNORECASE)
            for match in pattern.finditer(raw):
                suffix = raw[match.end():match.end() + 24]
                hint_match = re.match(rf"\s+({'|'.join(_EXPLICIT_HINTS)})(?![A-Za-z0-9_])", suffix, re.IGNORECASE)
                hint = f" {hint_match.group(1).lower()}" if hint_match else ""
                matches.append((match.start(), mnemonic + hint))

        result: list[str] = []
        seen: set[str] = set()
        for _, query in sorted(matches, key=lambda item: item[0]):
            key = query.lower()
            if key not in seen:
                seen.add(key)
                result.append(query)
        return result

    def _missing_explicit_targets(self, explicit_targets: list[str], llm_targets: list[str]) -> list[str]:
        """Compare target sets by resolved XML identity so aliases do not look missing."""
        llm_keys = {
            resolution.selected_xml_id or query.strip().upper()
            for query in llm_targets
            for resolution in [self._resolver.resolve(query)]
        }
        missing: list[str] = []
        for query in explicit_targets:
            resolution = self._resolver.resolve(query)
            key = resolution.selected_xml_id or query.strip().upper()
            if key not in llm_keys:
                missing.append(query)
        return missing

    @staticmethod
    def _normalize_target_plan_payload(payload: Any) -> tuple[dict[str, list[str]], str | None]:
        """Normalize supported legacy target-plan shapes to the canonical schema."""
        source: str | None = None
        values: Any
        if isinstance(payload, list):
            values = payload
            source = "top-level array"
        elif isinstance(payload, dict):
            if isinstance(payload.get("target_queries"), list):
                values = payload["target_queries"]
            elif isinstance(payload.get("targets"), list):
                values = payload["targets"]
                source = "targets array"
            elif isinstance(payload.get("instructions"), list):
                values = payload["instructions"]
                source = "instructions array"
            else:
                raise LlmProtocolError("expected target_queries, targets, or instructions string array")
        else:
            raise LlmProtocolError("top-level JSON value must be an object or string array")

        if not 1 <= len(values) <= 16:
            raise LlmProtocolError("target array must contain between 1 and 16 items")
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise LlmProtocolError("target array items must be non-empty strings")
        return {"target_queries": [value.strip() for value in values]}, source

    @staticmethod
    def _protocol_error_message(exc: Exception) -> str:
        if isinstance(exc, ValidationError):
            return exc.errors()[0]["msg"]
        return str(exc)

    def _invoke_llm_json(self, stage: str, system_prompt: str, user_prompt: str) -> tuple[Any, str | None]:
        try:
            from langchain_core.messages import HumanMessage, SystemMessage

            response = self._llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
            content = getattr(response, "content", None)
            if not isinstance(content, str) or not content.strip():
                return None, f"LLM {stage} response has no text content"
            text = content.strip()
            if text.startswith("```"):
                parts = text.split("\n", 1)
                if len(parts) != 2 or "```" not in parts[1]:
                    return None, f"LLM {stage} response contains an incomplete code fence"
                text = parts[1].rsplit("```", 1)[0].strip()
            return json.loads(text), None
        except json.JSONDecodeError as exc:
            logger.warning("scenario.llm_json_invalid", stage=stage, error=str(exc), traceback=traceback.format_exc())
            return None, f"LLM {stage} response is not valid JSON: {exc.msg}"
        except Exception as exc:
            logger.exception("scenario.llm_call_failed", stage=stage)
            return None, f"LLM {stage} call failed: {type(exc).__name__}: {str(exc)[:160]}"

    def _resolve_targets(self, program: ScenarioProgram, queries: list[str]) -> list[CanonicalTarget]:
        targets_by_key: dict[str, CanonicalTarget] = {}
        for query in queries:
            resolution = self._resolver.resolve(query)
            profile = self._profile_from_resolution(resolution)
            if not profile:
                self._issue(program, "resolution_error", f"Could not resolve instruction query: {query}", location=query)
                continue
            existing = targets_by_key.get(profile.xml_id)
            if existing:
                if query not in existing.aliases:
                    existing.aliases.append(query)
                    program.generation_trace.append(
                        f"Merged LLM alias {query} into canonical target {existing.key}"
                    )
                continue
            candidate = self._instantiator.instantiate_profile(profile, 1)[0]
            for feature in profile.feature_dependencies:
                if feature.feature_name not in program.required_features:
                    program.required_features.append(feature.feature_name)
            target = CanonicalTarget(
                key=profile.xml_id,
                canonical_query=query,
                aliases=[query],
                profile=profile,
                resolution=resolution,
            )
            targets_by_key[target.key] = target
            resolved = self._resolution_dict(query, resolution, profile, candidate.instruction)
            resolved.update({"target_key": target.key, "aliases": target.aliases})
            program.resolved.append(resolved)
        program.targets = list(targets_by_key.values())
        program.queries = [target.canonical_query for target in program.targets]
        return program.targets

    def _build_file(self, program: ScenarioProgram) -> None:
        if not program.statement_metadata:
            return
        if not _ASSEMBLY_SYMBOL_RE.fullmatch(program.scenario_id):
            program.scenario_id = make_assembly_symbol(program.raw, prefix="scenario")
        lines = ["    .text", "    .align 2", f"    .global {program.scenario_id}", f"{program.scenario_id}:"]
        lines.extend(f"    {statement['instruction']}" for statement in program.statement_metadata)
        content = "\n".join(lines) + "\n"
        program.generated_status = "PASS"
        program.test_file = {
            "file_id": f"{program.scenario_id}_program",
            "filename": f"{program.scenario_id}.S",
            "format": "s",
            "test_type": "scenario_assembly",
            "content": content,
            "status": "pass",
            "description": f"{program.generation_mode} scenario program for: {program.raw}",
            "issue_count": 0,
            "required_features": program.required_features,
        }

    def static_review(self, program: ScenarioProgram) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        if not program.test_file:
            return [{"type": "generation_error", "severity": "high", "description": "No scenario assembly file was generated", "location": program.scenario_id, "dimension": "generator"}]
        if not _ASSEMBLY_SYMBOL_RE.fullmatch(program.scenario_id):
            issues.append({"type": "invalid_assembly_symbol", "severity": "high", "description": f"Assembly symbol is not ASCII-safe: {program.scenario_id}", "location": program.scenario_id, "dimension": "syntax"})
        if len(program.statement_metadata) != program.program_instruction_count:
            issues.append({"type": "budget_mismatch", "severity": "high", "description": f"Expected {program.program_instruction_count} instructions, generated {len(program.statement_metadata)}", "location": program.test_file["filename"], "dimension": "budget"})
        counts = program._target_counts()
        for target in program.targets:
            if counts.get(target.key, 0) != program.target_instruction_count:
                issues.append({"type": "target_count_mismatch", "severity": "high", "description": f"Target {target.canonical_query} ({target.key}) appears {counts.get(target.key, 0)} times; expected {program.target_instruction_count}", "location": program.test_file["filename"], "dimension": "budget"})
        content = program.test_file.get("content", "")
        for line_number, line in enumerate(content.splitlines(), 1):
            if not line.isascii():
                issues.append({"type": "non_ascii_assembly", "severity": "high", "description": "Generated assembly contains non-ASCII text", "location": f"{program.test_file['filename']}:{line_number}", "dimension": "syntax"})
                break
        if "/*<" in content or "<" in content and ">" in content:
            issues.append({"type": "unresolved_placeholder", "severity": "high", "description": "Generated assembly still contains XML placeholders", "location": program.test_file["filename"], "dimension": "syntax"})
        if not content.strip():
            issues.append({"type": "empty_file", "severity": "high", "description": "Generated assembly file is empty", "location": program.test_file["filename"], "dimension": "syntax"})
        return issues

    @staticmethod
    def _issue(program: ScenarioProgram, issue_type: str, description: str, severity: str = "high", location: str = "", dimension: str = "generator") -> None:
        program.issues.append({"type": issue_type, "severity": severity, "description": description, "location": location or program.scenario_id, "dimension": dimension})

    @staticmethod
    def _overall_status(program: ScenarioProgram) -> str:
        if program.generated_status != "PASS" or program.static_review_status == "FAIL":
            return "FAILED"
        if program.compile_status == "PASS":
            return "COMPILED"
        if program.compile_status == "FAIL":
            return "FAILED"
        return "REVIEWED"

    def _profile_from_resolution(self, resolution: ResolutionResult) -> InstructionProfile | None:
        return self._analyzer.extract_profile(xml_id=resolution.selected_xml_id) if resolution.selected_xml_id else None

    @staticmethod
    def _resolution_dict(query: str, resolution: ResolutionResult, profile: InstructionProfile, instruction: str) -> dict[str, Any]:
        selected = resolution.candidates[0] if resolution.candidates else None
        return {"query": query, "xml_id": profile.xml_id, "mnemonic": profile.mnemonic, "instr_class": profile.instr_class, "features": [f.feature_name for f in profile.feature_dependencies], "assembly": instruction, "matched_hints": selected.matched_hints if selected else [], "why_matched": selected.why_matched if selected else []}
