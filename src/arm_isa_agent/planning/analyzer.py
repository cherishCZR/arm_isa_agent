"""InstructionAnalyzer — extract test-relevant metadata from SQLite instruction data.

Design:
- Queries the SQLite knowledge base via the injected client.
- Builds a comprehensive InstructionProfile that captures all aspects
  relevant to test planning: encodings, operands, immediates, constraints,
  features, pseudocode sections, and architecture characteristics.
- The profile is then consumed by the LLM to generate a test strategy.
"""

from __future__ import annotations

import re
from typing import Any

import structlog

from arm_isa_agent.planning.models import (
    ConstraintSummary,
    EncodingSummary,
    FeatureDependency,
    ImmediateRange,
    InstructionProfile,
    OperandSummary,
)

logger = structlog.get_logger(__name__)

# Regex to extract immediate name and bit width from encoded_in fields
# Examples: "imm12" → (12), "immhi:immlo" → special composite
_IMM_BIT_PATTERN = re.compile(r"imm(\d+)|imm(\d*)")


class InstructionAnalyzer:
    """Analyzes instruction metadata and builds a test-relevant profile.

    Usage:
        analyzer = InstructionAnalyzer(sqlite_client)
        profile = analyzer.extract_profile("ADD", "ADD_shifted_imm")
        strategy = analyzer.recommend_test_dimensions(profile)
    """

    def __init__(self, sqlite_client: Any = None) -> None:
        self._sqlite = sqlite_client

    def set_sqlite(self, sqlite_client: Any) -> None:
        self._sqlite = sqlite_client

    # ── Public API ───────────────────────────────────────────

    def extract_profile(
        self,
        mnemonic: str = "",
        xml_id: str = "",
    ) -> InstructionProfile | None:
        """Build a full InstructionProfile from SQLite data.

        Args:
            mnemonic: Instruction mnemonic to look up.
            xml_id: Exact XML id (optional, used for disambiguation).

        Returns:
            InstructionProfile or None if not found.
        """
        if self._sqlite is None:
            logger.error("analyzer.no_sqlite_client")
            return None

        data = self._query_instruction_dict(mnemonic, xml_id)
        if data is None:
            logger.warning("analyzer.instruction_not_found", mnemonic=mnemonic, xml_id=xml_id)
            return None

        return self._build_profile_from_orm_dict(data)

    def extract_profile_from_data(self, instruction_data: dict[str, Any]) -> InstructionProfile:
        """Build profile from pre-fetched instruction JSON data (avoids second DB call)."""
        return self._build_profile_from_dict(instruction_data)

    @staticmethod
    def recommend_test_dimensions(profile: InstructionProfile) -> list:
        """Recommend test dimensions based on instruction profile (rule-based, no LLM)."""
        dims: list[dict[str, Any]] = []

        # Normal operations: always needed
        dims.append({
            "name": "Normal Operation",
            "priority": "high",
            "coverage_pct": 25.0,
            "focus": ["Basic encoding with typical register values"],
            "rationale": "Core functional verification",
            "suggested_count": 2,
        })

        # Boundary values: if there are immediate operands
        if profile.immediate_ranges:
            dims.append({
                "name": "Boundary Values",
                "priority": "high",
                "coverage_pct": 20.0,
                "focus": [f"Min/max for {i.operand_symbol} (0-{i.max_value})" for i in profile.immediate_ranges[:3]],
                "rationale": f"{len(profile.immediate_ranges)} immediate field(s) found",
                "suggested_count": max(1, len(profile.immediate_ranges)),
            })

        # Register constraints: if has special registers or multiple register ops
        if profile.has_special_register or profile.gp_register_count >= 3:
            dims.append({
                "name": "Register Constraints",
                "priority": "high",
                "coverage_pct": 15.0,
                "focus": InstructionAnalyzer._infer_register_focus(profile),
                "rationale": "Register overlap, SP/XZR, or width constraints detected",
                "suggested_count": 2,
            })

        # Encoding coverage: multiple encodings
        if profile.encoding_count > 1:
            dims.append({
                "name": "Encoding Coverage",
                "priority": "high" if profile.encoding_count > 2 else "medium",
                "coverage_pct": 15.0,
                "focus": [f"Encoding: {e.name} ({e.label})" for e in profile.encodings],
                "rationale": f"{profile.encoding_count} encoding variants to cover",
                "suggested_count": min(profile.encoding_count, 4),
            })
        elif profile.has_32bit_encoding and profile.has_64bit_encoding:
            dims.append({
                "name": "Width Variants",
                "priority": "medium",
                "coverage_pct": 10.0,
                "focus": ["32-bit (W registers)", "64-bit (X registers)"],
                "rationale": "Both 32-bit and 64-bit forms available",
                "suggested_count": 2,
            })

        # CONSTRAINED_UNPREDICTABLE
        if profile.constrained_unpredictable:
            dims.append({
                "name": "Constrained Unpredictable",
                "priority": "high",
                "coverage_pct": 15.0,
                "focus": [c.description[:100] for c in profile.constrained_unpredictable[:3]],
                "rationale": f"{len(profile.constrained_unpredictable)} constrained-unpredictable conditions",
                "suggested_count": max(1, min(len(profile.constrained_unpredictable), 3)),
            })

        # Feature gates
        if profile.feature_gates:
            dims.append({
                "name": "Feature Dependency",
                "priority": "medium",
                "coverage_pct": 10.0,
                "focus": [f"Feature: {c.description[:80]}" for c in profile.feature_gates[:3]],
                "rationale": f"{len(profile.feature_gates)} feature-gated conditions",
                "suggested_count": 1,
            })

        # Shift/Extend
        if profile.has_shift_extend:
            dims.append({
                "name": "Shift/Extend Coverage",
                "priority": "medium",
                "coverage_pct": 10.0,
                "focus": [
                    "LSL with various shift amounts",
                    "Other shift types: LSR, ASR, ROR",
                    "Zero extend (UXTB/UXTH/UXTW/UXTX)",
                    "Sign extend (SXTB/SXTH/SXTW/SXTX)",
                ],
                "rationale": "Instruction supports shift/extend modifiers",
                "suggested_count": 2,
            })

        # Flag effects
        if profile.affects_flags:
            dims.append({
                "name": "Flag Effects (NZCV)",
                "priority": "medium",
                "coverage_pct": 10.0,
                "focus": [
                    "N flag: negative result",
                    "Z flag: zero result",
                    "C flag: carry out",
                    "V flag: signed overflow",
                ],
                "rationale": "Instruction modifies NZCV flags",
                "suggested_count": 2,
            })

        # SIMD / SVE special
        if profile.simd_register_count > 0 or profile.sv_register_count > 0:
            dims.append({
                "name": "Vector/SIMD-Specific" if profile.simd_register_count > 0 else "SVE-Specific",
                "priority": "high",
                "coverage_pct": 10.0,
                "focus": (
                    ["Element sizes: 8B/16B, 4H/8H, 2S/4S, 2D"]
                    if profile.simd_register_count > 0
                    else ["Predicate masks (P registers)", "Element size variants", "Governing predicate effects"]
                ),
                "rationale": "SIMD/SVE vector operations require element-level coverage",
                "suggested_count": 2,
            })

        return InstructionAnalyzer._normalize_coverage(dims)

    # ── Internal Methods ─────────────────────────────────────

    def _query_instruction_dict(self, mnemonic: str, xml_id: str = "") -> dict[str, Any] | None:
        """Query instruction from SQLite and eagerly load all relationships into a dict.

        This avoids the DetachedInstanceError that occurs when accessing
        relationships outside the SQLAlchemy session.

        Supports variant hints in the mnemonic, e.g. "ADDP SVE" will search for
        the ADDP instruction whose instr_class/xml_id best matches "SVE".
        """
        from arm_isa_agent.kb.sqlite.models import InstructionModel

        base_mnemonic = mnemonic
        variant_hints: list[str] = []
        if " " in mnemonic and not xml_id:
            parts = mnemonic.split()
            base_mnemonic = parts[0]
            variant_hints = [p for p in parts[1:] if p]

        with self._sqlite.session() as session:
            query = session.query(InstructionModel)

            if xml_id:
                inst = query.filter(InstructionModel.xml_id == xml_id).first()
            elif base_mnemonic:
                # Prefer non-alias instructions
                candidates = query.filter(
                    InstructionModel.mnemonic.ilike(base_mnemonic),
                    InstructionModel.is_alias == False,  # noqa: E712
                ).all()
                if not candidates:
                    candidates = query.filter(InstructionModel.mnemonic.ilike(base_mnemonic)).all()
                if not candidates:
                    inst = query.filter(InstructionModel.xml_id.ilike(f"%{base_mnemonic}%")).first()
                    if inst is None:
                        return None
                else:
                    inst = self._select_best_candidate(candidates, variant_hints)
            else:
                return None

            if inst is None:
                return None

            # Eagerly extract all relationship data within the session
            return self._orm_instance_to_dict(inst)

    def _build_profile_from_orm_dict(self, data: dict[str, Any]) -> InstructionProfile:
        """Build InstructionProfile from eagerly-loaded ORM dict."""
        # ---- Encodings ----
        encodings: list[EncodingSummary] = []
        has_32bit = False
        has_64bit = False
        has_shift = False

        for enc in data.get("encodings", []):
            template = enc.get("assembly_template", "")
            es = EncodingSummary(
                name=enc.get("name", ""),
                label=enc.get("label", ""),
                assembly_template=template,
                bitdiffs=enc.get("bitdiffs", ""),
                bit_pattern=enc.get("bit_pattern", ""),
                has_shift_extend=self._template_has_shift(template),
            )
            encodings.append(es)
            lbl = (enc.get("label", "") + enc.get("name", "")).lower()
            if "32" in lbl:
                has_32bit = True
            if "64" in lbl:
                has_64bit = True
            if es.has_shift_extend:
                has_shift = True

        # ---- Operands ----
        operands: list[OperandSummary] = []
        gp_count = 0
        simd_count = 0
        sv_count = 0
        has_special = False
        reg_widths: list[int] = []
        imm_ranges: list[ImmediateRange] = []
        affects_flags = False

        for op_data in data.get("operands", []):
            op = OperandSummary(
                symbol=op_data.get("symbol", ""),
                description=op_data.get("description", ""),
                operand_type=op_data.get("operand_type", "register"),
                register_class=op_data.get("register_class", ""),
                register_width=op_data.get("register_width", 0),
                encoded_in=op_data.get("encoded_in", ""),
            )
            operands.append(op)

            if op.operand_type == "register":
                rc = op.register_class.upper()
                if rc in ("W", "X"):
                    gp_count += 1
                elif rc in ("B", "H", "S", "D", "Q", "V"):
                    simd_count += 1
                elif rc == "Z":
                    sv_count += 1
                if op.register_width and op.register_width not in reg_widths:
                    reg_widths.append(op.register_width)

            desc_lower = (op.description + " " + op.symbol).lower()
            if re.search(r"\b(sp|wsp|xzr|wzr|pc)\b", desc_lower):
                has_special = True

            if op.operand_type == "immediate":
                imm_range = self._parse_immediate_from_summary(op)
                if imm_range:
                    imm_ranges.append(imm_range)

        mnemonic = data.get("mnemonic", "")
        if "flags" in mnemonic.upper() or mnemonic.upper().endswith("S"):
            affects_flags = True

        for ps in data.get("pseudocode_list", []):
            body = (ps.get("body_plain", "") or ps.get("body", ""))[:200]
            if any(kw in body.lower() for kw in ["pstate.", "nzcv", "conditionholds", "pstate"]):
                affects_flags = True
                break

        # ---- Constraints by type ----
        cu_constraints: list[ConstraintSummary] = []
        fg_constraints: list[ConstraintSummary] = []
        eu_constraints: list[ConstraintSummary] = []

        for c in data.get("constraints", []):
            cs = ConstraintSummary(
                constraint_type=c.get("constraint_type", ""),
                condition=c.get("condition", ""),
                description=c.get("description", ""),
            )
            ct = (c.get("constraint_type", "") or "").upper()
            if "UNPREDICTABLE" in ct:
                cu_constraints.append(cs)
            elif "FEATURE_GATE" in ct or "FEATURE" in ct:
                fg_constraints.append(cs)
            elif "UNDEF" in ct:
                eu_constraints.append(cs)

        # ---- Features ----
        features: list[FeatureDependency] = []
        arch_versions: list[str] = []

        for f in data.get("features", []):
            fd = FeatureDependency(
                feature_name=f.get("feature_name", ""),
                display_name=f.get("display_name", ""),
            )
            features.append(fd)
            dn = f.get("display_name", "").strip()
            if dn and dn not in arch_versions:
                arch_versions.append(dn)

        ps_sections: list[str] = list({
            ps.get("section_type", "") for ps in data.get("pseudocode_list", [])
            if ps.get("section_type")
        })

        if len(encodings) == 1:
            bd = encodings[0].bitdiffs.lower()
            if "sf==0" in bd or "sf == 0" in bd:
                has_32bit = True
            if "sf==1" in bd or "sf == 1" in bd:
                has_64bit = True

        return InstructionProfile(
            xml_id=data.get("xml_id", ""),
            mnemonic=data.get("mnemonic", ""),
            title=data.get("title", ""),
            instr_class=data.get("instr_class", ""),
            is_alias=bool(data.get("is_alias", False)),
            alias_of=data.get("alias_of") or "",
            brief=data.get("brief", ""),
            description_preview=(data.get("description") or "")[:500],
            encoding_count=len(encodings),
            encodings=encodings,
            operand_count=len(operands),
            operands=operands,
            immediate_ranges=imm_ranges,
            gp_register_count=gp_count,
            simd_register_count=simd_count,
            sv_register_count=sv_count,
            has_special_register=has_special,
            register_widths=sorted(reg_widths),
            has_shift_extend=has_shift,
            constrained_unpredictable=cu_constraints,
            feature_gates=fg_constraints,
            encoding_undefined=eu_constraints,
            feature_dependencies=features,
            architecture_versions=sorted(arch_versions),
            has_32bit_encoding=has_32bit,
            has_64bit_encoding=has_64bit,
            pseudocode_section_types=ps_sections,
            affects_flags=affects_flags,
            is_predicated=bool(data.get("is_predicated", False)),
            uses_dit=bool(data.get("uses_dit", False)),
        )

    def _build_profile_from_dict(self, data: dict[str, Any]) -> InstructionProfile:
        """Build profile from JSON dict (from query_instruction tool output)."""
        # This handles the case where we already have query results as JSON
        found = data.get("found", False)
        if not found:
            return InstructionProfile(xml_id="unknown", mnemonic="unknown")

        enc_summaries: list[EncodingSummary] = []
        has_32 = False
        has_64 = False
        has_shift = False

        for enc in data.get("encodings", []):
            template = enc.get("assembly_template", "")
            es = EncodingSummary(
                name=enc.get("name", ""),
                label=enc.get("label", ""),
                assembly_template=template,
                bitdiffs=enc.get("bitdiffs", ""),
                bit_pattern=enc.get("bit_pattern", ""),
                has_shift_extend=self._template_has_shift(template),
            )
            enc_summaries.append(es)
            lbl = (enc.get("label", "") + enc.get("name", "")).lower()
            if "32" in lbl:
                has_32 = True
            if "64" in lbl:
                has_64 = True
            if es.has_shift_extend:
                has_shift = True

        ops: list[OperandSummary] = []
        gp = simd = sv_ops = 0
        has_sp = False
        widths: list[int] = []
        imm_ranges: list[ImmediateRange] = []

        for op in data.get("operands", []):
            os = OperandSummary(**{k: op.get(k, "") for k in OperandSummary.model_fields})
            ops.append(os)
            if os.operand_type == "register":
                rc = os.register_class.upper()
                if rc in ("W", "X"):
                    gp += 1
                elif rc in ("B", "H", "S", "D", "Q", "V"):
                    simd += 1
                elif rc == "Z":
                    sv_ops += 1
            if os.register_width and os.register_width not in widths:
                widths.append(os.register_width)
            if re.search(r"\b(sp|wsp|xzr|wzr|pc)\b", (os.description + " " + os.symbol).lower()):
                has_sp = True

        cu_list = data.get("constraints_by_type", {}).get("CONSTRAINED_UNPREDICTABLE", [])
        fg_list = data.get("constraints_by_type", {}).get("FEATURE_GATE", [])
        eu_list = data.get("constraints_by_type", {}).get("ENCODING_UNDEF", [])

        return InstructionProfile(
            xml_id=data.get("xml_id", ""),
            mnemonic=data.get("mnemonic", ""),
            title=data.get("title", ""),
            instr_class=data.get("instr_class", ""),
            is_alias=data.get("is_alias", False),
            alias_of=data.get("alias_of") or "",
            brief=data.get("brief", ""),
            description_preview=(data.get("description", "") or "")[:500],
            encoding_count=len(enc_summaries),
            encodings=enc_summaries,
            operand_count=len(ops),
            operands=ops,
            immediate_ranges=imm_ranges,
            gp_register_count=gp,
            simd_register_count=simd,
            sv_register_count=sv_ops,
            has_special_register=has_sp,
            register_widths=sorted(widths),
            has_shift_extend=has_shift,
            constrained_unpredictable=[ConstraintSummary(**c) for c in cu_list[:5]],
            feature_gates=[ConstraintSummary(**c) for c in fg_list[:5]],
            encoding_undefined=[ConstraintSummary(**c) for c in eu_list[:5]],
            feature_dependencies=[FeatureDependency(feature_name=f, display_name="")
                                  for f in data.get("features", [])],
            architecture_versions=[],
            has_32bit_encoding=has_32,
            has_64bit_encoding=has_64,
            pseudocode_section_types=[],
            affects_flags=data.get("mnemonic", "").upper().endswith("S"),
            is_predicated=data.get("is_predicated", False),
            uses_dit=data.get("uses_dit", False),
        )

    # ── Helper Methods ───────────────────────────────────────

    @staticmethod
    def _select_best_candidate(candidates: list[Any], hints: list[str]) -> Any:
        """Pick the candidate whose metadata best matches the variant hints.

        Hints are typically extra words from the user query, e.g. "SVE" in
        "ADDP SVE".  We score each candidate by checking whether the hint
        appears in its instr_class, xml_id, or title, with an exact match on
        instr_class weighted more heavily.
        """
        if not hints or len(candidates) == 1:
            return candidates[0]

        best = candidates[0]
        best_score = -1
        for cand in candidates:
            score = 0
            text = " ".join([
                (cand.instr_class or "").lower(),
                (cand.xml_id or "").lower(),
                (cand.title or "").lower(),
            ])
            instr_class_lower = (cand.instr_class or "").lower()
            for hint in hints:
                hint_lower = hint.lower()
                if hint_lower in text:
                    score += 1
                if hint_lower == instr_class_lower:
                    score += 3
                # xml_id often contains the variant suffix, e.g. addp_z_p_zz
                if hint_lower in (cand.xml_id or "").lower():
                    score += 2
            if score > best_score:
                best_score = score
                best = cand
        return best

    @staticmethod
    def _orm_instance_to_dict(inst: Any) -> dict[str, Any]:
        """Convert an InstructionModel instance into a serializable dict."""
        return {
            "xml_id": inst.xml_id,
            "mnemonic": inst.mnemonic,
            "title": inst.title,
            "instr_class": inst.instr_class,
            "is_alias": inst.is_alias,
            "alias_of": inst.alias_of,
            "brief": inst.brief,
            "description": inst.description,
            "is_predicated": inst.is_predicated,
            "uses_dit": inst.uses_dit,
            "sm_policy": inst.sm_policy,
            "operational_notes": inst.operational_notes,
            "source_file": inst.source_file,
            "regdiagram_form": inst.regdiagram_form,
            "encodings": [
                {
                    "name": e.name,
                    "label": e.label,
                    "assembly_template": e.assembly_template,
                    "bitdiffs": e.bitdiffs,
                    "bit_pattern": e.bit_pattern,
                }
                for e in inst.encodings
            ],
            "operands": [
                {
                    "symbol": o.symbol,
                    "description": o.description or "",
                    "operand_type": o.operand_type or "register",
                    "register_class": o.register_class or "",
                    "register_width": o.register_width or 0,
                    "encoded_in": o.encoded_in or "",
                }
                for o in inst.operands
            ],
            "pseudocode_list": [
                {
                    "body_plain": ps.body_plain or "",
                    "body": ps.body or "",
                    "section_type": ps.section_type or "",
                }
                for ps in inst.pseudocode_list
            ],
            "constraints": [
                {
                    "constraint_type": c.constraint_type or "",
                    "condition": c.condition or "",
                    "description": c.description or "",
                }
                for c in inst.constraints
            ],
            "features": [
                {
                    "feature_name": f.feature_name,
                    "display_name": f.display_name or "",
                }
                for f in inst.features
            ],
        }

    @staticmethod
    def _parse_immediate_from_summary(op: OperandSummary) -> ImmediateRange | None:
        """Extract immediate value range from an OperandSummary."""
        if not op.encoded_in:
            return None

        match = re.search(r"imm(\d+)", op.encoded_in)
        if not match:
            match = re.search(r"(\d+)-bit", op.description)
            if not match:
                return None
            bit_width = int(match.group(1))
        else:
            bit_width = int(match.group(1))

        max_val = (1 << bit_width) - 1
        return ImmediateRange(
            operand_symbol=op.symbol,
            encoded_field=op.encoded_in,
            bit_width=bit_width,
            min_value=0,
            max_value=max_val,
            signed=bool(re.search(r"signed|2'?s[ -]?complement", op.description, re.I)),
        )

    def _parse_immediate_range(self, operand: Any) -> ImmediateRange | None:
        """Extract immediate value range from operand metadata."""
        encoded_in = operand.encoded_in if hasattr(operand, "encoded_in") else operand.get("encoded_in", "")
        if not encoded_in:
            return None

        # Parse bit width from field name like "imm12" or "immhi:immlo"
        match = re.search(r"imm(\d+)", encoded_in)
        if not match:
            # Try to infer from operand description
            desc = operand.description if hasattr(operand, "description") else operand.get("description", "")
            match = re.search(r"(\d+)-bit", desc)
            if not match:
                return None
            bit_width = int(match.group(1))
        else:
            bit_width = int(match.group(1))

        max_val = (1 << bit_width) - 1
        sym = (operand.symbol if hasattr(operand, "symbol") else operand.get("symbol", ""))
        return ImmediateRange(
            operand_symbol=sym,
            encoded_field=encoded_in,
            bit_width=bit_width,
            min_value=0,
            max_value=max_val,
            signed=bool(re.search(r"signed|2'?s[ -]?complement",
                                   (operand.description if hasattr(operand, "description")
                                    else operand.get("description", "")), re.I)),
        )

    @staticmethod
    def _template_has_shift(template: str) -> bool:
        tl = template.lower()
        return any(kw in tl for kw in ["lsl", "lsr", "asr", "ror", "uxt", "sxt"])

    @staticmethod
    def _infer_register_focus(profile: InstructionProfile) -> list[str]:
        focus: list[str] = []
        if profile.has_special_register:
            focus.append("SP/XZR/WZR usage: ensure correct behavior (zero vs stack)")  # noqa: RUF001
        if profile.gp_register_count >= 2:
            focus.append("Source/dest overlap: same register as source and destination")
        if 32 in profile.register_widths and 64 in profile.register_widths:
            focus.append("Mixed 32/64-bit register width: W vs X register variants")
        if not focus:
            focus.append("Register value propagation between source and destination")
        return focus

    @staticmethod
    def _normalize_coverage(dims: list[dict[str, Any]]) -> list:
        """Normalize coverage percentages to sum to 100%."""
        total = sum(d.get("coverage_pct", 0) for d in dims)
        if total > 0 and abs(total - 100) > 0.01:
            scale = 100.0 / total
            for d in dims:
                d["coverage_pct"] = round(d["coverage_pct"] * scale, 1)
        return dims
