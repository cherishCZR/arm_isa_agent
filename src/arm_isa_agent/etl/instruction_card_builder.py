"""Instruction Card 构建器。

将 Pydantic Instruction 模型转换为自包含的 Markdown 文档，
用作 RAG 检索的知识卡片。每张卡片包含指令的完整信息语义块。
"""

from __future__ import annotations

from typing import Any

from arm_isa_agent.core.models.instruction import Instruction


class InstructionCardBuilder:
    """构建 Markdown Instruction Card。

    Card 格式设计原则：
    1. 自包含 —— 每条 Card 可独立回答用户问题
    2. 结构化 —— 使用 Markdown 标题分层，方便 LLM 理解
    3. 语义分割 —— 每个语义块天然适合 Chunk/Embed
    """

    # ── 公开 API ─────────────────────────────────────────────────

    @staticmethod
    def _unwrap_instruction(instruction: Instruction | Any) -> Instruction:
        """Accept both an Instruction and XMLInstructionParser's ParseResult."""
        parsed_instruction = getattr(instruction, "instruction", None)
        if parsed_instruction is not None:
            return parsed_instruction
        return instruction

    @classmethod
    def build(cls, instruction: Instruction) -> str:
        """将 Instruction 转换为 Markdown Card。

        Args:
            instruction: 解析完成的 Instruction 对象

        Returns:
            完整的 Markdown 文本
        """
        instruction = cls._unwrap_instruction(instruction)
        parts: list[str] = []
        alias_tag = " `[ALIAS]`" if instruction.is_alias else ""

        # ── 1. 标题区 ──
        parts.append(f"## {instruction.mnemonic or instruction.xml_id}{alias_tag}")
        parts.append(f"_ARM A64 Instruction_{' (Alias of ' + instruction.alias_of + ')' if instruction.is_alias else ''}")
        parts.append("")

        # ── 2. 快速信息 ──
        meta: list[str] = []
        meta.append(f"**Title**: {instruction.title}")
        meta.append(f"**Class**: `{instruction.instr_class or 'N/A'}`")
        meta.append(f"**XML ID**: `{instruction.xml_id}`")
        parts.append(" | ".join(meta))
        parts.append("")

        # ── 3. 架构特性 ──
        if instruction.arch_variants:
            variants = ", ".join(
                f"`{av.feature}`" + (f" ({av.name})" if av.name else "")
                for av in instruction.arch_variants
            )
            parts.append(f"**Architecture**: {variants}")
            parts.append("")

        # ── 4. 摘要与描述 ──
        if instruction.brief:
            parts.append(f"**Summary**: {instruction.brief}")
            parts.append("")
        if instruction.description:
            parts.append(f"**Description**:")
            parts.append(instruction.description)
            parts.append("")

        # ── 5. 操作属性 ──
        attrs: list[str] = []
        if instruction.is_predicated:
            attrs.append("Predicated")
        if instruction.uses_dit:
            attrs.append(f"DIT-sensitive (condition: `{instruction.uses_dit_condition}`)"
                         if instruction.uses_dit_condition else "DIT-sensitive")
        if instruction.sm_policy:
            attrs.append(f"SM Policy: `{instruction.sm_policy}`")
        if attrs:
            parts.append(f"**Attributes**: {'; '.join(attrs)}")
            parts.append("")

        # ── 构建映射：伪代码名 → encoding.name / iclass_name ──
        ps_to_enc, ps_to_iclass, shared_ps = cls._classify_pseudocode(
            instruction.pseudocode_list, instruction.encodings,
        )

        # ── 构建集合：有专属伪代码/约束的 iclass ──
        # iclass_name → 有哪些 encoding 的伪代码（去重）
        iclass_has_ps: dict[str, bool] = {}
        for ps in instruction.pseudocode_list:
            ic = ps_to_iclass.get(ps.name)
            if ic:
                iclass_has_ps[ic] = True

        # ── 6. 编码变体（含各自的约束 + 伪代码）──
        # 统计 iclass name 出现次数，用于同 iclass 多 encoding 时消歧
        iclass_name_counts: dict[str, int] = {}
        for enc in instruction.encodings:
            if enc.iclass_name:
                iclass_name_counts[enc.iclass_name] = iclass_name_counts.get(enc.iclass_name, 0) + 1

        for enc in instruction.encodings:
            # Variant 标题优先用 iclass name（Scalar/Vector），回退 encoding name
            if enc.iclass_name:
                title = enc.iclass_name
                if iclass_name_counts[enc.iclass_name] > 1:
                    title = f"{enc.iclass_name} ({enc.name})"
            else:
                title = enc.name
            label_str = f" ({enc.label})" if enc.label else ""
            parts.append(f"### Encoding Variant: `{title}`{label_str}")

            if enc.bitdiffs:
                parts.append(f"- **Condition**: `{enc.bitdiffs}`")

            parts.append(f"- **Assembly**: `{enc.assembly_template}`")

            # 编码级固定值
            if enc.bitfields:
                fixed = []
                for bf in enc.bitfields:
                    bits_str = "".join(b for b in bf.values if b)
                    if bits_str:
                        fixed.append(f"`{bf.name}`=`{bits_str}`")
                if fixed:
                    parts.append(f"- **Fixed bits**: {', '.join(fixed)}")

            # 位模式
            if enc.bit_pattern:
                parts.append(f"- **Bit Pattern**: `{enc.bit_pattern}`")

            # 别名等价
            if enc.equivalent_to:
                parts.append(f"- **Alias of**: `{enc.equivalent_to}`")
                if enc.alias_condition:
                    parts.append(f"  Condition: {enc.alias_condition}")

            # ── 该变体的编码图（来自 iclass 级 regdiagram）──
            if enc.regdiagram_bitfields:
                parts.append(f"**Encoding Diagram ({enc.regdiagram_form}-bit)**:")
                parts.append("")
                parts.append("```text")
                parts.append(cls._render_diagram(enc.regdiagram_bitfields))
                parts.append("```")

            parts.append("")

            # ── 该变体的专属伪代码 ──
            enc_ps = [
                ps for ps in instruction.pseudocode_list
                if ps_to_enc.get(ps.name) == enc.name
            ]
            if enc_ps:
                cls._render_pseudocode_subsection(parts, enc_ps)

            # ── 该变体的专属约束 ──
            enc_constraints = [
                c for c in instruction.constraints
                if c.encoding_name == enc.name
            ]
            if enc_constraints:
                cls._render_constraints_subsection(parts, enc_constraints)

        # ── 7. 操作数 ──
        if instruction.operands:
            parts.append("### Operands")
            parts.append("")
            parts.append("| Symbol | Type | Field | Description |")
            parts.append("|---|---|---|---|")
            for op in instruction.operands:
                desc = op.description[:150].replace("\n", " ").replace("|", "\\|")

                # 类型显示：register 带位宽
                if op.operand_type == "register" and op.register_width:
                    type_str = f"register ({op.register_width}-bit)"
                else:
                    type_str = op.operand_type

                # 表格单元内需对 | 转义，否则会破坏 Markdown 表格的列分隔
                symbol = op.symbol.replace("|", "\\|")
                encoded_in = op.encoded_in.replace("|", "\\|")

                parts.append(
                    f"| `{symbol}` | `{type_str}` | "
                    f"`{encoded_in}` | {desc} |"
                )
            parts.append("")

            # 值表（仅展示有值表的操作数）
            for op in instruction.operands:
                if op.value_table:
                    keys = list(op.value_table[0].keys()) if op.value_table else []
                    if keys:
                        parts.append(f"**{op.symbol} Value Table**:")
                        parts.append("")
                        parts.append("| " + " | ".join(keys) + " |")
                        parts.append("|" + "|".join("---" for _ in keys) + "|")
                        for row in op.value_table:
                            vals = [str(row.get(k, "")).replace("|", "\\|") for k in keys]
                            parts.append("| " + " | ".join(vals) + " |")
                        parts.append("")

        # ── 8. 共有伪代码 ──
        parts.append("### Pseudocode")
        parts.append("")
        if shared_ps:
            cls._render_pseudocode_subsection(parts, shared_ps)
        elif not instruction.pseudocode_list:
            parts.append("No instruction-local pseudocode is present in this XML variant.")
            parts.append("")

        # ── 9. 共有约束 ──
        shared_constraints = [
            c for c in instruction.constraints if not c.encoding_name
        ]
        if shared_constraints:
            cls._render_constraints_subsection(parts, shared_constraints, is_shared=True)

        # ── 10. 操作备注 ──
        if instruction.operational_notes:
            notes = instruction.operational_notes
            if len(notes) > 1500:
                notes = notes[:1500] + "\n... (truncated)"
            parts.append("### Operational Notes")
            parts.append("")
            parts.append(notes)
            parts.append("")

        # ── 11. 元数据 ──
        parts.append("---")
        meta_items = []
        if instruction.docvars:
            for k, v in sorted(instruction.docvars.items()):
                if k in ("mnemonic", "instr-class"):
                    continue
                meta_items.append(f"{k}: `{v}`")
        meta_items.append(f"source: `{instruction.source_file}`")
        parts.append("<details><summary>Metadata</summary>\n\n" + "\n".join(
            f"- {item}" for item in meta_items
        ) + "\n</details>")

        return "\n".join(parts)

    # ── 元数据 ──────────────────────────────────────────────────

    @classmethod
    def build_card_metadata(cls, instruction: Instruction) -> dict[str, Any]:
        """构建 ChromaDB 兼容的元数据字典。"""
        instruction = cls._unwrap_instruction(instruction)
        return {
            "xml_id": instruction.xml_id,
            "mnemonic": instruction.mnemonic,
            "title": instruction.title,
            "instr_class": instruction.instr_class,
            "is_alias": instruction.is_alias,
            "alias_of": instruction.alias_of,
            "encoding_count": len(instruction.encodings),
            "operand_count": len(instruction.operands),
            "features": [av.feature for av in instruction.arch_variants],
            "source_file": instruction.source_file,
        }

    # ── 内部渲染 ──────────────────────────────────────────────────

    @staticmethod
    def _constraint_type_badge(ctype: str) -> str:
        """约束类型 → 可视化 badge。"""
        badges = {
            "FEATURE_GATE": "🔒 FEATURE_GATE",
            "ENCODING_UNDEF": "🚫 ENCODING_UNDEF",
            "CONSTRAINED_UNPREDICTABLE": "⚠ CONSTRAINED_UNPREDICTABLE",
            "DECODE_FALLBACK": "↩ DECODE_FALLBACK",
        }
        return badges.get(ctype, f"❓ {ctype}")

    # ── 伪代码 → encoding 分类 ───────────────────────────────────

    @staticmethod
    def _classify_pseudocode(
        pseudocode_list: list,
        encodings: list,
    ) -> tuple[dict[str, str], dict[str, str], list]:
        """将伪代码分类为「iclass 专属」vs「共有」。

        匹配规则：伪代码名最后一段（最后一个 ``.`` 之后）== encoding.name。

        Returns:
            (ps_name → enc_name, ps_name → iclass_name, shared_pseudocode_list)
        """
        enc_names: dict[str, str] = {}  # enc.name → iclass_name
        for enc in encodings:
            enc_names[enc.name] = enc.iclass_name or enc.name

        ps_to_enc: dict[str, str] = {}
        ps_to_iclass: dict[str, str] = {}
        shared: list = []

        for ps in pseudocode_list:
            last_seg = ps.name.split(".")[-1] if "." in ps.name else ps.name
            if last_seg in enc_names:
                ps_to_enc[ps.name] = last_seg
                ps_to_iclass[ps.name] = enc_names[last_seg]
            else:
                shared.append(ps)

        return ps_to_enc, ps_to_iclass, shared

    @classmethod
    def _render_pseudocode_subsection(
        cls,
        parts: list[str],
        pseudocode_list: list,
    ) -> None:
        """渲染伪代码子段（4级标题，缩进）。"""
        for ps in pseudocode_list:
            body = ps.body_plain or ps.body
            if len(body) > 3000:
                body = body[:3000] + "\n... (truncated)"

            parts.append(f"#### {ps.section_type} ({ps.name})")
            parts.append("")
            parts.append("```")
            parts.append(body)
            parts.append("```")
            parts.append("")

    @classmethod
    def _render_constraints_subsection(
        cls,
        parts: list[str],
        constraints: list,
        is_shared: bool = False,
    ) -> None:
        """渲染约束子段。"""
        if not constraints:
            return

        from collections import Counter

        type_counts = Counter(c.constraint_type for c in constraints)
        badges = {bt: cls._constraint_type_badge(bt) for bt in type_counts}
        summary_parts = []
        for bt, count in sorted(type_counts.items()):
            badge = badges.get(bt, bt)
            summary_parts.append(f"{count}× {badge}")
        summary = " / ".join(summary_parts)

        title = "### Encoding Constraints" if is_shared else "#### Constraints"
        parts.append(title)
        parts.append(f"_{summary}_")
        parts.append("")
        parts.append("| Type | Condition |")
        parts.append("|---|---|")
        for c in constraints:
            type_badge = cls._constraint_type_badge(c.constraint_type)
            cond = c.condition.replace("|", "\\|")
            parts.append(f"| {type_badge} | `{cond}` |")
        parts.append("")

    @classmethod
    def _render_diagram(cls, bitfields) -> str:
        """渲染编码图 ASCII 示意。

        Returns:
            多行文本：位编号行 + 分隔线 + 位值行
        """
        from arm_isa_agent.core.models.instruction import BitfieldValue

        if not bitfields:
            return "(empty)"

        sorted_fields = sorted(bitfields, key=lambda bf: bf.hibit, reverse=True)
        lines: list[str] = []

        # 位编号
        labels = []
        for bf in sorted_fields:
            if bf.width > 1:
                labels.append(f"{bf.hibit:2d} ")
            else:
                labels.append(f"{bf.hibit:2d}")
        # 用 | 分隔
        lines.append("| " + " ".join(labels) + " |")

        # 分隔
        lines.append("|" + "-" * (len(sorted_fields) * 3 + 2) + "|")

        # 位值
        values_parts = []
        for bf in sorted_fields:
            if bf.is_fixed and bf.values:
                vals = "".join(bf.values[:bf.width])
                vals = vals if vals else "?"
            elif bf.name:
                vals = bf.name
            else:
                vals = "?" * min(bf.width, 4)
            values_parts.append(vals.ljust(3))
        lines.append("| " + " ".join(values_parts) + " |")

        return "\n".join(lines)
