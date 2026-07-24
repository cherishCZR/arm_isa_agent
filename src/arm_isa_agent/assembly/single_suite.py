"""XML-driven compile-only scenario suites for single-instruction verification."""

from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Any, Callable

from arm_isa_agent.assembly.instantiator import AssemblyInstantiator
from arm_isa_agent.assembly.scenario import make_assembly_symbol
from arm_isa_agent.compile.verifier import CompileVerifier
from arm_isa_agent.planning.analyzer import InstructionAnalyzer
from arm_isa_agent.planning.models import InstructionProfile
from arm_isa_agent.resolution.resolver import InstructionResolver
from arm_isa_agent.verification.models import CompileSummary


@dataclass(frozen=True)
class ScenarioSpec:
    category: str
    format: str
    reason: str
    varied_operands: bool = False


@dataclass
class SingleInstructionSuite:
    query: str
    profile: InstructionProfile | None = None
    resolved: dict[str, Any] = field(default_factory=dict)
    test_files: list[dict[str, Any]] = field(default_factory=list)
    scenario_plan: list[dict[str, Any]] = field(default_factory=list)
    issues: list[dict[str, Any]] = field(default_factory=list)
    trace: list[str] = field(default_factory=list)
    compile_summary: CompileSummary = field(default_factory=CompileSummary)


class SingleInstructionSuiteGenerator:
    """Generate XML-applicable, exact-budget files for one instruction."""

    def __init__(
        self,
        sqlite_client: Any,
        seed: int | None = None,
        progress_callback: Callable[[str, str, str, dict[str, Any]], None] | None = None,
    ) -> None:
        self._resolver = InstructionResolver(sqlite_client)
        self._analyzer = InstructionAnalyzer(sqlite_client)
        self._instantiator = AssemblyInstantiator(seed=seed)
        self._compiler = CompileVerifier()
        self._rng = random.Random(seed)
        self._probe_cache: dict[tuple[str, str], bool] = {}
        self._progress_callback = progress_callback

    def _progress(self, stage: str, event: str, message: str, **snapshot: Any) -> None:
        if self._progress_callback is not None:
            self._progress_callback(stage, event, message, snapshot)

    def generate_and_verify(
        self,
        query: str,
        program_instruction_count: int,
        target_instruction_count: int,
    ) -> SingleInstructionSuite:
        suite = SingleInstructionSuite(query=query)
        self._progress("planner", "start", "Planning XML-derived single-instruction scenarios", program_instruction_count=program_instruction_count, target_instruction_count=target_instruction_count)
        self._progress("llm", "complete", "LLM generation disabled; using XML rule-based scenario generation", status="skipped")
        if program_instruction_count < 1 or target_instruction_count < 1:
            self._issue(suite, "invalid_budget", "Instruction counts must be positive integers", query)
            return suite
        if target_instruction_count >= program_instruction_count:
            self._issue(suite, "invalid_budget", "Total instruction budget must reserve at least one non-target instruction", query)
            return suite

        self._progress("retrieval", "start", "Resolving XML instruction variant")
        resolution = self._resolver.resolve(query)
        if not resolution.selected_xml_id:
            self._issue(suite, "resolution_error", f"Could not resolve instruction query: {query}", query)
            self._progress("retrieval", "complete", "Instruction resolution failed", status="error")
            return suite
        profile = self._analyzer.extract_profile(xml_id=resolution.selected_xml_id)
        if profile is None:
            self._issue(suite, "resolution_error", f"Could not load XML profile: {resolution.selected_xml_id}", query)
            self._progress("retrieval", "complete", "XML instruction profile could not be loaded", status="error")
            return suite

        suite.profile = profile
        candidate = self._instantiator.instantiate_profile(profile, 1)[0]
        suite.resolved = {
            "query": query,
            "xml_id": profile.xml_id,
            "mnemonic": profile.mnemonic,
            "instr_class": profile.instr_class,
            "features": [item.feature_name for item in profile.feature_dependencies],
            "assembly": candidate.instruction,
        }
        specs = self._plan(profile)
        suite.trace.append(f"Resolved {query} to {profile.xml_id}")
        suite.trace.append(f"Planned {len(specs)} XML-applicable compile-only scenarios")
        self._progress("retrieval", "complete", f"Resolved {query} to {profile.xml_id}", status="ok", xml_id=profile.xml_id)
        self._progress("planner", "complete", f"Planned {len(specs)} XML-applicable scenarios", status="ok", scenario_count=len(specs))
        self._progress("generator", "start", "Generating exact-budget scenario programs", scenario_count=len(specs))

        for index, spec in enumerate(specs, start=1):
            file_entry, plan_entry, issues = self._build_file(
                query, profile, spec, program_instruction_count, target_instruction_count,
            )
            suite.scenario_plan.append(plan_entry)
            suite.issues.extend(issues)
            if file_entry is not None:
                suite.test_files.append(file_entry)
            self._progress("generator", "progress", f"Generated scenario {index}/{len(specs)}: {spec.category}", scenario=spec.category, generated_files=len(suite.test_files))

        reviewable = [entry for entry in suite.test_files if entry["status"] == "pass"]
        self._progress("generator", "complete", f"Generated {len(suite.test_files)} scenario program file(s)", status="ok" if suite.test_files else "error")
        static_failed = sum(1 for entry in suite.test_files if entry["status"] == "fail")
        self._progress("reviewer", "start", "Reviewing instruction budgets and target occurrences")
        self._progress("reviewer", "complete", "Static review passed" if not static_failed else "Static review found issues", status="ok" if not static_failed else "error", issue_count=len(suite.issues))
        self._progress("compiler", "start", f"Compiling {len(reviewable)} generated file(s)")
        suite.compile_summary = self._compiler.verify_files(reviewable)
        self._progress(
            "compiler", "complete",
            f"Compile-only validation: {suite.compile_summary.passed}/{suite.compile_summary.total} files passed",
            status="ok" if suite.compile_summary.status == "PASS" else "error" if suite.compile_summary.status == "FAIL" else "skipped",
        )
        compile_by_id = {result.file_id: result for result in suite.compile_summary.results}
        for entry in suite.test_files:
            result = compile_by_id.get(entry["file_id"])
            if result and result.status != "PASS":
                entry["status"] = "fail"
                entry["issue_count"] += 1
                self._issue(suite, "compile_error", result.stderr or result.reason or "Compilation failed", entry["filename"], "compile")
        for plan in suite.scenario_plan:
            matching = next((entry for entry in suite.test_files if entry["file_id"] == plan.get("file_id")), None)
            if matching:
                result = compile_by_id.get(matching["file_id"])
                plan["status"] = "compiled" if result and result.status == "PASS" else "failed"
        return suite

    def _plan(self, profile: InstructionProfile) -> list[ScenarioSpec]:
        specs = [
            ScenarioSpec("normal_assembly", "s", "Baseline legal form instantiated from the selected XML encoding."),
        ]
        if profile.gp_register_count:
            specs.extend([
                ScenarioSpec("register_dependency_chain", "s", "Repeated scalar target instances preserve a controlled register data-flow form."),
                ScenarioSpec("register_aliasing", "s", "Uses the XML-instantiated legal scalar operand alias form."),
            ])
        if profile.immediate_ranges:
            specs.append(ScenarioSpec("immediate_boundary", "s", "XML profile exposes immediate fields; generated instances rotate legal boundary values.", True))
        if profile.has_shift_extend:
            specs.append(ScenarioSpec("shift_extend_boundary", "s", "XML encoding exposes shift or extend controls.", True))
        if profile.affects_flags:
            specs.append(ScenarioSpec("flags_dependency", "s", "XML profile marks NZCV effects."))
        if profile.simd_register_count:
            specs.append(ScenarioSpec("vector_register_variation", "s", "XML operands include SIMD/FP registers.", True))
        if profile.sv_register_count or any(f.feature_name in {"FEAT_SVE", "FEAT_SVE2", "FEAT_SME"} for f in profile.feature_dependencies):
            specs.append(ScenarioSpec("extension_register_variation", "s", "XML profile requires SVE, SVE2, or SME registers/features.", True))
        if self._supports_inline_asm(profile):
            specs.extend([
                ScenarioSpec("c_inline_asm", "c", "Scalar GPR XML form is wrapped in a compile-only C inline-asm translation unit."),
                ScenarioSpec("cpp_inline_asm", "cpp", "Scalar GPR XML form is wrapped in a compile-only C++ inline-asm translation unit."),
            ])
        return specs

    @staticmethod
    def _supports_inline_asm(profile: InstructionProfile) -> bool:
        forbidden = {"label", "memory"}
        return bool(profile.gp_register_count) and not profile.sv_register_count and not any(
            operand.operand_type in forbidden for operand in profile.operands
        )

    def _build_file(
        self,
        query: str,
        profile: InstructionProfile,
        spec: ScenarioSpec,
        total: int,
        target_count: int,
    ) -> tuple[dict[str, Any] | None, dict[str, Any], list[dict[str, Any]]]:
        base_id = make_assembly_symbol(f"{query}_{spec.category}", prefix="single")
        target_lines = self._target_lines(profile, target_count, spec)
        filler_count = total - target_count - (1 if spec.format == "s" else 0)
        instructions = [*target_lines, *("nop" for _ in range(filler_count))]
        if spec.format == "s":
            instructions.append("ret")
        issues = self._static_issues(base_id, instructions, total, target_count, spec.category)
        entry = {
            "file_id": base_id,
            "filename": f"{base_id}.{spec.format}",
            "format": spec.format,
            "test_type": spec.category,
            "content": self._render_asm(base_id, instructions) if spec.format == "s" else self._render_inline(spec.format, base_id, instructions),
            "status": "pass" if not issues else "fail",
            "description": spec.reason,
            "issue_count": len(issues),
            "required_features": [feature.feature_name for feature in profile.feature_dependencies],
            "scenario_id": spec.category,
            "scenario_reason": spec.reason,
            "budget": {"program_instruction_count": total, "target_instruction_count": target_count, "actual_instruction_count": len(instructions)},
        }
        plan = {
            "scenario_id": spec.category,
            "title": spec.category.replace("_", " "),
            "format": spec.format,
            "reason": spec.reason,
            "file_id": base_id,
            "status": "statically_reviewed" if not issues else "failed",
            "budget": entry["budget"],
        }
        for issue in issues:
            issue["location"] = entry["filename"]
        return entry, plan, issues

    def _target_lines(self, profile: InstructionProfile, count: int, spec: ScenarioSpec) -> list[str]:
        encoding = profile.encodings[0] if profile.encodings else None
        result: list[str] = []
        attempts = 0
        while len(result) < count and attempts < count * 12:
            attempts += 1
            # Dependency scenarios deliberately retain one legal form.  Every
            # other scenario receives independent seeded assignments so normal
            # tests do not collapse into identical instructions.
            salt = 0 if spec.category == "register_dependency_chain" else self._rng.randrange(0, 256)
            candidate = (
                self._instantiator.instantiate_encoding(profile, encoding, salt)
                if encoding is not None
                else self._instantiator.instantiate_profile(profile, 1)[0]
            )
            if self._probe_candidate(profile, candidate.instruction):
                result.append(candidate.instruction)
        if len(result) < count:
            fallback = self._instantiator.instantiate_profile(profile, 1)[0].instruction
            result.extend([fallback] * (count - len(result)))
        return result

    def _probe_candidate(self, profile: InstructionProfile, line: str) -> bool:
        key = (profile.xml_id, line)
        cached = self._probe_cache.get(key)
        if cached is not None:
            return cached
        probe = {
            "file_id": "template_probe",
            "filename": "template_probe.S",
            "format": "s",
            "content": f"    .text\nprobe:\n    {line}\n    ret\n",
            "required_features": [feature.feature_name for feature in profile.feature_dependencies],
        }
        self._probe_cache[key] = self._compiler.verify_file(probe).status == "PASS"
        return self._probe_cache[key]

    @staticmethod
    def _render_asm(symbol: str, instructions: list[str]) -> str:
        labels = sorted({token.rstrip(":") for line in instructions for token in line.split() if token.startswith(".Ltarget_")})
        lines = ["    .text", "    .align 2", f"    .global {symbol}", f"{symbol}:"]
        lines.extend(f"    {line}" for line in instructions)
        lines.extend(f"{label}:" for label in labels)
        return "\n".join(lines) + "\n"

    @staticmethod
    def _render_inline(fmt: str, symbol: str, instructions: list[str]) -> str:
        asm = "\n".join(f'        "{line.replace("\\", "\\\\").replace("\"", "\\\"")}\\n\\t"' for line in instructions)
        function = f"test_{symbol}"
        language_comment = "// C++ inline assembly scenario" if fmt == "cpp" else "/* C inline assembly scenario */"
        return (
            f"{language_comment}\n"
            f"void {function}(void) {{\n"
            "    __asm__ volatile(\n"
            f"{asm}\n"
            "        :\n        :\n        : \"cc\", \"memory\"\n"
            "    );\n"
            "}\n"
        )

    @staticmethod
    def _static_issues(symbol: str, instructions: list[str], total: int, target_count: int, category: str) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        if len(instructions) != total:
            issues.append({"type": "budget_mismatch", "severity": "high", "description": f"Expected {total} instructions, generated {len(instructions)}", "dimension": "budget"})
        if sum(line.split(None, 1)[0].lower() not in {"nop", "ret"} for line in instructions) != target_count:
            issues.append({"type": "target_count_mismatch", "severity": "high", "description": f"Expected {target_count} target instructions", "dimension": "budget"})
        if not symbol.isascii() or any(not line.isascii() for line in instructions):
            issues.append({"type": "non_ascii_assembly", "severity": "high", "description": "Generated source contains non-ASCII assembly text", "dimension": "syntax"})
        target_lines = [line for line in instructions if line.split(None, 1)[0].lower() not in {"nop", "ret"}]
        if category != "register_dependency_chain" and len(target_lines) >= 4 and len(set(target_lines)) < 4:
            issues.append({"type": "insufficient_operand_diversity", "severity": "high", "description": "Independent scenario generated fewer than four distinct target operand assignments", "dimension": "operand_diversity"})
        return issues

    @staticmethod
    def _issue(suite: SingleInstructionSuite, issue_type: str, description: str, location: str, dimension: str = "generator") -> None:
        suite.issues.append({"type": issue_type, "severity": "high", "description": description[:1000], "location": location, "dimension": dimension})
