"""Resolve user instruction queries to concrete XML instruction entries."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from arm_isa_agent.kb.sqlite.models import InstructionModel


_HINT_SYNONYMS: dict[str, set[str]] = {
    "imm": {"imm", "immediate", "addsub_imm", "#", "literal"},
    "shift": {"shift", "shifted", "addsub_shift", "lsl", "lsr", "asr", "ror"},
    "extend": {"extend", "extended", "uxt", "sxt", "addsub_ext"},
    "sve": {"sve", "_z_", " z", " p", "feat_sve"},
    "sve2": {"sve2", "feat_sve2"},
    "simd": {"simd", "advsimd", "fpsimd", "vector"},
    "base": {"base", "general"},
    "alias": {"alias"},
    "branch": {"branch", "cond", "b.cond", "label"},
    "load": {"load", "ldr", "ldp", "ld1", "memory", "["},
    "store": {"store", "str", "stp", "st1", "memory", "["},
    "sme": {"sme", "za", "zt0", "feat_sme"},
    "mops": {"mops", "feat_mops"},
    "ls64": {"ls64", "feat_ls64"},
}


@dataclass
class ResolutionCandidate:
    mnemonic: str
    xml_id: str
    title: str
    instr_class: str
    features: list[str] = field(default_factory=list)
    rank_score: float = 0.0
    matched_hints: list[str] = field(default_factory=list)
    why_matched: list[str] = field(default_factory=list)


@dataclass
class ResolutionResult:
    query: str
    base_mnemonic: str
    hints: list[str]
    selected_xml_id: str = ""
    candidates: list[ResolutionCandidate] = field(default_factory=list)

    @property
    def found(self) -> bool:
        return bool(self.selected_xml_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "base_mnemonic": self.base_mnemonic,
            "hints": self.hints,
            "selected_xml_id": self.selected_xml_id,
            "candidates": [c.__dict__ for c in self.candidates],
        }


class InstructionResolver:
    """Resolve mnemonic plus optional variant hints to an XML id."""

    def __init__(self, sqlite_client: Any) -> None:
        self._sqlite = sqlite_client

    def resolve(self, query: str, mode: str = "best", limit: int = 8) -> ResolutionResult:
        base, hints = self._parse_query(query)
        if not base:
            return ResolutionResult(query=query, base_mnemonic="", hints=hints)

        with self._sqlite.session() as session:
            exact_xml = session.query(InstructionModel).filter(InstructionModel.xml_id.ilike(base)).first()
            if exact_xml is not None:
                cand = self._candidate_from_model(exact_xml, hints, exact_bonus=True)
                return ResolutionResult(
                    query=query,
                    base_mnemonic=exact_xml.mnemonic,
                    hints=hints,
                    selected_xml_id=exact_xml.xml_id,
                    candidates=[cand],
                )

            rows = session.query(InstructionModel).filter(InstructionModel.mnemonic.ilike(base)).all()
            if not rows:
                rows = session.query(InstructionModel).filter(InstructionModel.xml_id.ilike(f"%{base}%")).limit(50).all()

            candidates = [self._candidate_from_model(row, hints) for row in rows]
            candidates.sort(key=lambda c: c.rank_score, reverse=True)
            if mode == "all_variants":
                selected = candidates[0].xml_id if candidates else ""
                return ResolutionResult(query=query, base_mnemonic=base.upper(), hints=hints, selected_xml_id=selected, candidates=candidates)

            limited = candidates[:limit]
            selected = limited[0].xml_id if limited else ""
            return ResolutionResult(query=query, base_mnemonic=base.upper(), hints=hints, selected_xml_id=selected, candidates=limited)

    @staticmethod
    def _parse_query(query: str) -> tuple[str, list[str]]:
        cleaned = " ".join(query.strip().split())
        if not cleaned:
            return "", []
        parts = cleaned.split(" ")
        base = parts[0].strip().upper()
        hints = [p.strip().lower() for p in parts[1:] if p.strip()]
        return base, hints

    def _candidate_from_model(self, inst: InstructionModel, hints: list[str], exact_bonus: bool = False) -> ResolutionCandidate:
        features = [f.feature_name for f in inst.features] if inst.features else []
        enc_text = " ".join(
            " ".join([
                e.name or "",
                e.label or "",
                e.assembly_template or "",
                e.bitdiffs or "",
            ])
            for e in inst.encodings
        )
        op_text = " ".join(
            " ".join([
                o.symbol or "",
                o.description or "",
                o.operand_type or "",
                o.register_class or "",
                o.encoded_in or "",
            ])
            for o in inst.operands
        )
        text = " ".join([
            inst.mnemonic or "",
            inst.xml_id or "",
            inst.title or "",
            inst.instr_class or "",
            inst.brief or "",
            " ".join(features),
            enc_text,
            op_text,
        ]).lower()

        score = 10.0
        why = ["mnemonic/xml candidate"]
        matched: list[str] = []
        if exact_bonus:
            score += 100
            why.append("exact xml_id match")
        if not inst.is_alias:
            score += 1.5
        if hints:
            for hint in hints:
                hint_score, hint_why = self._score_hint(hint, text, inst)
                score += hint_score
                if hint_score > 0:
                    matched.append(hint)
                    why.extend(hint_why)
        else:
            # Prefer general/base forms for plain mnemonics.
            cls = (inst.instr_class or "").lower()
            xml_id = (inst.xml_id or "").lower()
            if cls in {"general", "base"}:
                score += 2
                why.append("plain mnemonic prefers base/general")
            if "addsub_imm" in xml_id:
                score += 3
                why.append("plain mnemonic prefers immediate form")
            elif "addsub_shift" in xml_id:
                score += 2
                why.append("plain mnemonic accepts shifted-register form")
            elif "addsub_ext" in xml_id or "extend" in xml_id:
                score -= 3
                why.append("plain mnemonic avoids extended-register form")
            if "advsimd" in xml_id:
                score -= 1
            if "sve" in cls:
                score -= 2

        return ResolutionCandidate(
            mnemonic=inst.mnemonic,
            xml_id=inst.xml_id,
            title=inst.title,
            instr_class=inst.instr_class,
            features=features,
            rank_score=round(score, 3),
            matched_hints=matched,
            why_matched=why[:8],
        )

    @staticmethod
    def _score_hint(hint: str, text: str, inst: InstructionModel) -> tuple[float, list[str]]:
        synonyms = _HINT_SYNONYMS.get(hint, {hint})
        score = 0.0
        why: list[str] = []
        xml_id = (inst.xml_id or "").lower()
        instr_class = (inst.instr_class or "").lower()
        for token in synonyms:
            if token in text:
                score += 4.0
                why.append(f"hint {hint} matched token {token}")
                break
        if hint == "imm" and ("imm" in xml_id or any("imm" in (e.assembly_template or "").lower() for e in inst.encodings)):
            score += 5
            why.append("immediate form match")
        if hint == "shift" and ("shift" in xml_id or any(s in text for s in ["lsl", "lsr", "asr", "ror"])):
            score += 5
            why.append("shifted form match")
            if "shift" in xml_id:
                score += 8
                why.append("xml_id contains shift")
            if "ext" in xml_id or "extend" in xml_id:
                score -= 3
        if hint == "sve" and ("sve" in instr_class or any(f.feature_name == "FEAT_SVE" for f in inst.features)):
            score += 8
            why.append("SVE class/feature match")
        if hint == "sve2" and any("SVE2" in f.feature_name for f in inst.features):
            score += 8
            why.append("SVE2 feature match")
        if hint == "simd" and ("simd" in instr_class or "advsimd" in xml_id or "fpsimd" in xml_id):
            score += 8
            why.append("SIMD/FP class match")
        if hint == "alias" and inst.is_alias:
            score += 8
            why.append("alias match")
        return score, why
