"""Instantiate ARM XML assembly templates into concrete assembly lines."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field

from arm_isa_agent.planning.models import EncodingSummary, InstructionProfile, OperandSummary


_PLACEHOLDER_RE = re.compile(r"<([^>]+)>")


@dataclass
class AssemblyCandidate:
    instruction: str
    encoding_name: str = ""
    xml_id: str = ""
    required_features: list[str] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)


class AssemblyInstantiator:
    """Generate concrete assembly statements from XML assembly templates."""

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def instantiate_profile(self, profile: InstructionProfile, count: int = 1) -> list[AssemblyCandidate]:
        encodings = profile.encodings or [EncodingSummary(name=profile.mnemonic, assembly_template=profile.mnemonic)]
        candidates: list[AssemblyCandidate] = []
        for idx in range(max(1, count)):
            enc = encodings[idx % len(encodings)]
            candidates.append(self.instantiate_encoding(profile, enc, idx))
        return candidates

    def instantiate_encoding(self, profile: InstructionProfile, encoding: EncodingSummary, salt: int = 0) -> AssemblyCandidate:
        template = encoding.assembly_template or profile.mnemonic
        diagnostics: list[str] = []
        op_by_symbol = {self._clean_symbol(op.symbol).lower(): op for op in profile.operands}
        template = self._normalize_register_fragments(template, op_by_symbol)

        def replace(match: re.Match[str]) -> str:
            raw = match.group(1)
            key = self._clean_symbol(raw).lower()
            op = op_by_symbol.get(key)
            template_owns_arrangement = bool(re.match(r"^\.(?:[0-9]+[A-Za-z]+|<[^>]+>)", template[match.end():]))
            value = self._value_for_placeholder(
                raw, op, profile, salt, template_owns_arrangement=template_owns_arrangement,
            )
            if match.start() > 0 and template[match.start() - 1] == "#" and value.startswith("#"):
                value = value[1:]
            if (
                ("shift" in raw.lower() or "extend" in raw.lower())
                and " #" in value
                and "#<" in template[match.end():match.end() + 8]
            ):
                value = value.split()[0]
            if value == "":
                diagnostics.append(f"unresolved placeholder <{raw}>")
                return f"/*<{raw}>*/"
            return value

        line = _PLACEHOLDER_RE.sub(replace, template)
        line = self._clean_optional_syntax(line)
        line = self._lower_mnemonic(line)
        return AssemblyCandidate(
            instruction=line,
            encoding_name=encoding.name,
            xml_id=profile.xml_id,
            required_features=[f.feature_name for f in profile.feature_dependencies],
            diagnostics=diagnostics,
        )

    def _normalize_register_fragments(self, template: str, op_by_symbol: dict[str, OperandSummary]) -> str:
        """Normalize XML's ``D<d>`` form into one bound register operand.

        In Arm XML, the leading register-family letter can be literal text while
        the register number is a placeholder.  Leaving the prefix in place
        after rendering ``<d>`` as ``d0`` produces invalid source such as
        ``Dd0``.  Remove it only when operand metadata confirms ownership.
        """
        def replace(match: re.Match[str]) -> str:
            family, symbol = match.group(1), match.group(2)
            operand = op_by_symbol.get(symbol.lower())
            if operand and operand.register_class.upper() == family.upper():
                return f"<{symbol}>"
            return match.group(0)

        return re.sub(r"([BHSQDVWXYZ])<([A-Za-z][A-Za-z0-9_]*)>", replace, template)

    @staticmethod
    def _clean_symbol(symbol: str) -> str:
        return symbol.strip().strip("<>").strip("{}").strip()

    def _value_for_placeholder(
        self,
        raw: str,
        op: OperandSummary | None,
        profile: InstructionProfile,
        salt: int,
        template_owns_arrangement: bool = False,
    ) -> str:
        raw_l = raw.lower()
        symbol = self._clean_symbol(raw)
        symbol_l = symbol.lower()
        desc = ((op.description if op else "") + " " + raw_l + " " + symbol_l).lower()
        reg_class = (op.register_class if op else "").upper()

        if "cond" in symbol_l:
            return self._pick(["eq", "ne", "lt", "ge"], salt)
        if symbol_l.startswith("t"):
            # XML uses <T>, <Ta>, and <Tb> as arrangement placeholders.  The
            # vector operand is rendered bare when the template supplies this
            # suffix, so this must include the lane count (for example 2D),
            # not merely an element letter.
            return self._pick(["2d", "4s"], salt)
        if "label" in symbol_l or (op and op.operand_type == "label"):
            return f".Ltarget_{salt}"
        if symbol_l in {"amount", "sh", "shift_amount"}:
            return self._pick(["0", "1"], salt)
        if "shift" in symbol_l:
            # Immediate add/sub encodings permit architectural 0/12 shifts.
            return self._pick(["lsl #0", "lsl #12"], salt)
        if "extend" in symbol_l:
            return self._pick(["uxtw #0", "sxtw #0"], salt)
        if "imm" in symbol_l or (op and op.operand_type == "immediate"):
            return self._immediate_value(symbol_l, desc, salt)
        if "index" in symbol_l:
            return str(salt % 2)
        if "prfop" in symbol_l:
            return "pldl1keep"
        if "option" in symbol_l:
            return "#0"

        if reg_class == "Z" or symbol_l.startswith("z") or "z register" in desc:
            return f"z{salt % 8}"
        if symbol_l == "pg":
            return f"p{salt % 4}"
        if reg_class == "P" or symbol_l.startswith("p") or "predicate" in desc:
            pred = f"p{salt % 4}"
            suffix = self._predicate_suffix(raw_l, desc)
            if "/" in raw_l or "governing" in desc:
                return pred + suffix + "/m"
            return pred + suffix
        if reg_class in {"B", "H", "S", "D", "Q", "V"} or any(symbol_l.startswith(p) for p in ["v", "b", "h", "s", "d", "q"]):
            return self._simd_register(reg_class, raw_l, desc, salt, bare_vector=template_owns_arrangement)
        if reg_class == "W" or symbol_l.startswith("w"):
            return f"w{salt % 16}"
        if reg_class == "X" or symbol_l.startswith("x"):
            return f"x{salt % 16}"
        if "base" in desc or "address" in desc or "memory" in desc or "[" in raw_l:
            return f"[x{(salt + 8) % 16}]"
        if op and op.operand_type == "memory":
            return f"[x{(salt + 8) % 16}]"

        # Mnemonic-specific fallbacks for common symbolic names.
        if symbol_l in {"rd", "rn", "rm", "ra", "rt", "rt2", "rs", "xd", "xn", "xm", "xa", "xt"}:
            return f"x{salt % 16}"
        if symbol_l in {"wd", "wn", "wm", "wa", "wt", "wt2", "ws"}:
            return f"w{salt % 16}"
        if symbol_l in {"zd", "zn", "zm", "za", "zt", "zdn"}:
            return f"z{salt % 8}"
        if symbol_l in {"pd", "pn", "pm", "pg"}:
            return f"p{salt % 4}"
        return f"x{salt % 16}"

    def _immediate_value(self, symbol_l: str, desc: str, salt: int) -> str:
        if "nzcv" in symbol_l:
            return "#0"
        if "imm12" in symbol_l:
            return self._pick(["#0", "#1", "#4095"], salt)
        if "imm6" in symbol_l:
            return self._pick(["#0", "#1", "#63"], salt)
        if "imm5" in symbol_l:
            return self._pick(["#0", "#1", "#31"], salt)
        if "imm4" in symbol_l:
            return self._pick(["#0", "#1", "#15"], salt)
        if "signed" in desc:
            return self._pick(["#0", "#1", "#-1"], salt)
        return self._pick(["#0", "#1"], salt)

    @staticmethod
    def _element_suffix(raw_l: str, desc: str) -> str:
        for suffix in [".b", ".h", ".s", ".d"]:
            if suffix in raw_l:
                return suffix
        if "byte" in desc:
            return ".b"
        if "half" in desc:
            return ".h"
        if "double" in desc:
            return ".d"
        return ".s"

    @staticmethod
    def _predicate_suffix(raw_l: str, desc: str) -> str:
        for suffix in [".b", ".h", ".s", ".d"]:
            if suffix in raw_l:
                return suffix
        if "byte" in desc:
            return ".b"
        if "half" in desc:
            return ".h"
        if "double" in desc:
            return ".d"
        return ".s"

    def _simd_register(self, reg_class: str, raw_l: str, desc: str, salt: int, bare_vector: bool = False) -> str:
        base = f"v{salt % 16}"
        if bare_vector and reg_class == "V":
            return base
        if ".16b" in raw_l or "16b" in desc:
            return base + ".16b"
        if ".8b" in raw_l or "8b" in desc:
            return base + ".8b"
        if ".8h" in raw_l or "8h" in desc:
            return base + ".8h"
        if ".4h" in raw_l or "4h" in desc:
            return base + ".4h"
        if ".4s" in raw_l or "4s" in desc:
            return base + ".4s"
        if ".2s" in raw_l or "2s" in desc:
            return base + ".2s"
        if ".2d" in raw_l or "2d" in desc:
            return base + ".2d"
        if reg_class in {"B", "H", "S", "D", "Q"}:
            return f"{reg_class.lower()}{salt % 16}"
        return base + ".4s"

    @staticmethod
    def _clean_optional_syntax(line: str) -> str:
        line = line.replace("{, ", ", ").replace("{,", ", ").replace("}", "")
        line = line.replace("{", "")
        line = re.sub(r"\s+", " ", line).strip()
        line = line.replace(" ,", ",")
        line = re.sub(r",\s*,", ",", line)
        line = line.replace("#lsl", "lsl").replace("#lsr", "lsr").replace("#asr", "asr")
        line = line.replace("/M", "/m").replace("/Z", "/z")
        return line

    @staticmethod
    def _lower_mnemonic(line: str) -> str:
        parts = line.split(" ", 1)
        if not parts:
            return line
        parts[0] = parts[0].lower()
        return " ".join(parts)

    def _pick(self, values: list[str], salt: int) -> str:
        if not values:
            return ""
        return values[salt % len(values)]
