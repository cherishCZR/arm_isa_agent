"""ARM ISA XML 解析器。

从 ARM 官方 XML 文件中提取结构化指令信息。
支持解析：
    - 指令类型 XML (type="instruction")
    - 别名类型 XML (type="alias")
    - 共享伪代码 XML (type="pseudocode")

提取六大类数据：
    - Instruction  : 指令标识、描述、操作属性
    - Encoding     : 编码变体、汇编模板、位模式
    - Operands     : 操作数符号、类型、值表
    - Constraints  : 约束条件（CONSTRAINED UNPREDICTABLE + Encoding 约束）
    - Feature      : 架构特性变体（ArchVariant）
    - Operation    : 伪代码段（Decode / Execute / Operation）
    - Shared Pseudocode : 共享伪代码函数
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import structlog
from lxml import etree

from arm_isa_agent.core.constants import REGISTER_CLASS_WIDTH
from arm_isa_agent.core.models.instruction import (
    ArchVariant,
    BitfieldValue,
    Constraint,
    Encoding,
    Instruction,
    Operand,
    Pseudocode,
    SharedPseudocodeFunction,
)
from arm_isa_agent.etl.constraint_extractor import EncodingConstraintExtractor

logger = structlog.get_logger(__name__)


# ── 安全 XMLParser（跳过外部 DTD 加载）────────────────────────

def _make_safe_parser() -> etree.XMLParser:
    """创建安全的 lxml XMLParser。

    ARM XML 文件引用外部 DTD (iform-p.dtd / sharedps.dtd)，
    若按默认设置解析会因找不到 DTD 而抛 XMLSyntaxError。
    此 parser 禁用外部实体解析和网络访问。
    """
    return etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        load_dtd=False,
        dtd_validation=False,
    )


# ── 解析结果容器 ──────────────────────────────────────────────

@dataclass
class ParseResult:
    """单文件解析结果。"""
    filepath: Path
    instruction: Instruction | None = None
    error: str | None = None
    error_type: str = ""  # "syntax" | "validation" | "unexpected"

    @property
    def ok(self) -> bool:
        return self.instruction is not None


# ── 解析器 ────────────────────────────────────────────────────

class XMLInstructionParser:
    """ARM ISA XML 指令解析器。

    用法:
        result = XMLInstructionParser.parse_file(Path("adc.xml"))
        if result.ok:
            print(result.instruction.mnemonic)
    """

    # ----------------------------------------------------------------
    # 公开 API
    # ----------------------------------------------------------------

    @classmethod
    def parse_file(cls, filepath: Path) -> ParseResult:
        """解析单个指令 XML 文件。

        Returns:
            ParseResult，包含 Instruction 或错误信息。
        """
        try:
            parser = _make_safe_parser()
            tree = etree.parse(str(filepath), parser)
            root = tree.getroot()
            instruction = cls._parse_instructionsection(root, filepath.name)
            return ParseResult(filepath=filepath, instruction=instruction)
        except etree.XMLSyntaxError as e:
            logger.error("xml.syntax_error", file=filepath.name, error=str(e)[:200])
            return ParseResult(filepath=filepath, error=str(e), error_type="syntax")
        except ValueError as e:
            logger.error("xml.value_error", file=filepath.name, error=str(e)[:200])
            return ParseResult(filepath=filepath, error=str(e), error_type="validation")
        except Exception as e:
            logger.error("xml.unexpected_error", file=filepath.name, error=str(e)[:200])
            return ParseResult(filepath=filepath, error=str(e), error_type="unexpected")

    @classmethod
    def parse_shared_pseudocode(cls, filepath: Path) -> tuple[list[SharedPseudocodeFunction], list[str]]:
        """解析共享伪代码 XML 文件。

        Returns:
            (functions, errors) —— 成功解析的函数列表和错误信息列表。
        """
        functions: list[SharedPseudocodeFunction] = []
        errors: list[str] = []

        try:
            parser = _make_safe_parser()
            tree = etree.parse(str(filepath), parser)
            root = tree.getroot()

            for ps_section in root.findall("ps_section"):
                for ps_elem in ps_section.findall("ps"):
                    try:
                        func = cls._parse_shared_ps_element(ps_elem)
                        functions.append(func)
                    except Exception as e:
                        errors.append(f"{ps_elem.get('name', '?')}: {e}")

            logger.info("xml.shared_ps_parsed", count=len(functions), errors=len(errors))
        except Exception as e:
            logger.error("xml.shared_ps_parse_error", error=str(e)[:200])
            errors.append(f"file-level: {e}")

        return functions, errors

    # ----------------------------------------------------------------
    # 顶层 <instructionsection>
    # ----------------------------------------------------------------

    @classmethod
    def _parse_instructionsection(cls, root: etree._Element, source_file: str) -> Instruction:
        xml_id = root.get("id", "")
        title = root.get("title", "")
        inst_type = root.get("type", "instruction")

        # docvars
        docvars = cls._parse_docvars(root.find("docvars"))
        mnemonic = docvars.get("mnemonic", "")
        instr_class = docvars.get("instr-class", "")

        # 描述
        desc_elem = root.find("desc")
        brief, description = cls._parse_description(desc_elem)

        # 别名
        is_alias = inst_type == "alias"
        alias_of, alias_of_id = "", ""
        if is_alias:
            aliasto_elem = root.find("aliasto")
            if aliasto_elem is not None:
                alias_of = aliasto_elem.get("refiform", "")
                alias_of_id = aliasto_elem.get("iformid", "")

        # 操作属性
        is_predicated, uses_dit, uses_dit_condition, sm_policy = cls._parse_operational_attrs(desc_elem)

        # 编码类（含 arch_variants, encodings, regdiagram, iclass 级伪代码）
        encodings, regdiagram_form, all_arch_variants, iclass_pseudocode = \
            cls._parse_classes(root.find("classes"))

        # 从汇编模板构建 操作数符号 → 寄存器类字母 的映射（用于操作数类型推断）
        symbol_register_class_map = cls._build_symbol_register_class_map(encodings)

        # 顶层伪代码（Execute / Operation 段）
        top_pseudocode = []
        for ps_section in root.findall("ps_section"):
            cls._extract_pseudocode_from_section(ps_section, top_pseudocode)

        # 合并伪代码：iclass 级别 Decode + 顶层 Execute/Operation
        pseudocode_list = iclass_pseudocode + top_pseudocode

        # 去重 arch_variants
        deduped_variants = cls._dedup_arch_variants(all_arch_variants)

        # 操作数
        operands = cls._parse_explanations(root.find("explanations"), symbol_register_class_map)

        # 约束──先解析 XML 中显式的 <constrained_unpredictables>，再从伪代码提取 encoding 约束
        constraints = cls._parse_constraints(root.find("constrained_unpredictables"))
        constraints += cls._extract_encoding_constraints(pseudocode_list, xml_id)

        # ── 伪代码 → encoding 名称映射 ──
        # 伪代码名最后一段（如 ABS_asisdmisc_R）匹配 encoding.name
        ps_to_enc = cls._build_pseudocode_encoding_map(pseudocode_list, encodings)

        # 将 constraint 的 source_section → encoding_name 关联
        for c in constraints:
            if c.source_section and c.source_section in ps_to_enc:
                c.encoding_name = ps_to_enc[c.source_section]

        # 操作备注
        operational_notes = cls._parse_operational_notes(root.find("operationalnotes"))

        return Instruction(
            xml_id=xml_id,
            title=title,
            mnemonic=mnemonic,
            instruction_type=inst_type,
            is_alias=is_alias,
            alias_of=alias_of,
            alias_of_id=alias_of_id,
            docvars=docvars,
            instr_class=instr_class,
            brief=brief,
            description=description,
            is_predicated=is_predicated,
            uses_dit=uses_dit,
            uses_dit_condition=uses_dit_condition,
            sm_policy=sm_policy,
            encodings=encodings,
            regdiagram_form=regdiagram_form,
            operands=operands,
            pseudocode_list=pseudocode_list,
            arch_variants=deduped_variants,
            constraints=constraints,
            operational_notes=operational_notes,
            source_file=source_file,
        )

    # ----------------------------------------------------------------
    # docvars
    # ----------------------------------------------------------------

    @staticmethod
    def _parse_docvars(docvars_elem: etree._Element | None) -> dict[str, str]:
        if docvars_elem is None:
            return {}
        result: dict[str, str] = {}
        for dv in docvars_elem.findall("docvar"):
            key = dv.get("key", "")
            value = dv.get("value", "")
            if key:
                result[key] = value
        return result

    # ----------------------------------------------------------------
    # 描述
    # ----------------------------------------------------------------

    @classmethod
    def _parse_description(cls, desc_elem: etree._Element | None) -> tuple[str, str]:
        if desc_elem is None:
            return "", ""

        brief = ""
        brief_elem = desc_elem.find("brief")
        if brief_elem is not None:
            parts = [cls._get_text(p) for p in brief_elem.findall("para")]
            brief = " ".join(parts).strip()

        description = ""
        authored_elem = desc_elem.find("authored")
        if authored_elem is not None:
            parts = [cls._get_text(p) for p in authored_elem.findall("para")]
            description = "\n\n".join(parts)

        return brief, description

    @classmethod
    def _parse_operational_attrs(cls, desc_elem: etree._Element | None) -> tuple[bool, bool, str, str]:
        is_predicated = False
        uses_dit = False
        uses_dit_condition = ""
        sm_policy = ""

        if desc_elem is None:
            return is_predicated, uses_dit, uses_dit_condition, sm_policy

        pred_elem = desc_elem.find("predicated")
        if pred_elem is not None and pred_elem.text:
            is_predicated = pred_elem.text.strip().lower() == "true"

        dit_elem = desc_elem.find("uses_dit")
        if dit_elem is not None:
            uses_dit = (dit_elem.text or "").strip() == "True"
            uses_dit_condition = dit_elem.get("condition", "")

        sm_elem = desc_elem.find("sm_policy")
        if sm_elem is not None and sm_elem.text:
            sm_policy = sm_elem.text.strip()

        return is_predicated, uses_dit, uses_dit_condition, sm_policy

    # ----------------------------------------------------------------
    # classes → iclass
    # ----------------------------------------------------------------

    @classmethod
    def _parse_classes(cls, classes_elem: etree._Element | None) -> tuple[
        list[Encoding], str, list[ArchVariant], list[Pseudocode],
    ]:
        encodings: list[Encoding] = []
        regdiagram_form = "32"
        all_arch_variants: list[ArchVariant] = []
        pseudocode_list: list[Pseudocode] = []

        if classes_elem is None:
            return encodings, regdiagram_form, all_arch_variants, pseudocode_list

        for iclass_elem in classes_elem.findall("iclass"):
            iclass_name = iclass_elem.get("name", "")
            # arch_variants（iclass 级别）
            ic_arch_elem = iclass_elem.find("arch_variants")
            if ic_arch_elem is not None:
                for av in ic_arch_elem.findall("arch_variant"):
                    all_arch_variants.append(ArchVariant(
                        feature=av.get("feature", ""),
                        name=av.get("name", ""),
                    ))

            # regdiagram —— 每个 iclass 独立解析，归属到该 iclass 下的每个 encoding
            iclass_regdiagram_bitfields: list[BitfieldValue] = []
            iclass_regdiagram_form = "32"
            regdiag = iclass_elem.find("regdiagram")
            if regdiag is not None:
                iclass_regdiagram_form = regdiag.get("form", "32")
                for box in regdiag.findall("box"):
                    iclass_regdiagram_bitfields.append(cls._parse_bitfield_box(box))

            # 用首个 iclass 的 form 作为顶层 regdiagram_form（数据库兼容）
            if not iclass_regdiagram_bitfields and regdiagram_form == "32":
                pass  # 保留默认值
            elif iclass_regdiagram_bitfields and regdiagram_form == "32":
                regdiagram_form = iclass_regdiagram_form

            # encoding
            for enc_elem in iclass_elem.findall("encoding"):
                enc = cls._parse_encoding(enc_elem)
                if enc:
                    # 将 iclass 级的 regdiagram 和 name 赋值给该 encoding
                    enc.regdiagram_bitfields = iclass_regdiagram_bitfields
                    enc.regdiagram_form = iclass_regdiagram_form
                    enc.iclass_name = iclass_name
                    encodings.append(enc)

            # iclass 级伪代码（Decode）
            cls._extract_pseudocode_sections(iclass_elem, pseudocode_list)

        return encodings, regdiagram_form, all_arch_variants, pseudocode_list

    # ----------------------------------------------------------------
    # regdiagram / encoding bitfield boxes
    # ----------------------------------------------------------------

    @classmethod
    def _parse_bitfield_box(cls, box: etree._Element) -> BitfieldValue:
        name = box.get("name", "")
        try:
            hibit = int(box.get("hibit", "0"))
        except ValueError:
            hibit = 0
        try:
            width = int(box.get("width", "1"))
        except ValueError:
            width = 1
        settings = box.get("settings")
        psbits = box.get("psbits", "")
        is_fixed = settings is not None
        fixed_count = cls._safe_int(settings) if settings else 0

        values: list[str] = []
        for c in box.findall("c"):
            colspan_str = c.get("colspan")
            if colspan_str:
                try:
                    for _ in range(int(colspan_str)):
                        values.append("")
                except ValueError:
                    values.append("")
            else:
                values.append((c.text or "").strip())

        return BitfieldValue(
            name=name,
            hibit=hibit,
            width=width,
            values=values,
            is_fixed=is_fixed,
            fixed_count=fixed_count,
            psbits=psbits,
        )

    # ----------------------------------------------------------------
    # encoding
    # ----------------------------------------------------------------

    @classmethod
    def _parse_encoding(cls, enc_elem: etree._Element) -> Encoding | None:
        name = enc_elem.get("name", "")
        label = enc_elem.get("label", "")
        bitdiffs = enc_elem.get("bitdiffs", "")

        # 汇编模板
        asm_elem = enc_elem.find("asmtemplate")
        asm_template_raw = ""
        asm_template = ""
        operand_symbols: list[str] = []
        if asm_elem is not None:
            asm_template_raw = cls._element_to_string(asm_elem)
            asm_template, operand_symbols = cls._extract_asm_template(asm_elem)

        # docvars
        docvars = cls._parse_docvars(enc_elem.find("docvars"))

        # encoding 级 bitfield boxes（覆盖值）
        bitfields = [cls._parse_bitfield_box(b) for b in enc_elem.findall("box")]

        # encoding 级 arch_variants
        enc_arch_variants: list[ArchVariant] = []
        av_elem = enc_elem.find("arch_variants")
        if av_elem is not None:
            for av in av_elem.findall("arch_variant"):
                enc_arch_variants.append(ArchVariant(
                    feature=av.get("feature", ""),
                    name=av.get("name", ""),
                ))

        # 别名等价指令
        equivalent_to = ""
        alias_condition = ""
        equiv_elem = enc_elem.find("equivalent_to")
        if equiv_elem is not None:
            equiv_asm = equiv_elem.find("asmtemplate")
            if equiv_asm is not None:
                equivalent_to = cls._get_text(equiv_asm)
            alias_cond_elem = equiv_elem.find("aliascond")
            if alias_cond_elem is not None:
                alias_condition = (alias_cond_elem.text or "").strip()

        # 计算位模式
        bit_pattern, bit_pattern_mask = cls._compute_bit_pattern(bitfields)

        return Encoding(
            name=name,
            label=label,
            bitdiffs=bitdiffs,
            assembly_template=asm_template,
            assembly_template_raw=asm_template_raw,
            docvars=docvars,
            bitfields=bitfields,
            arch_variants=enc_arch_variants,
            equivalent_to=equivalent_to,
            alias_condition=alias_condition,
            operand_symbols=operand_symbols,
            bit_pattern=bit_pattern,
            bit_pattern_mask=bit_pattern_mask,
        )

    @classmethod
    def _extract_asm_template(cls, asm_elem: etree._Element) -> tuple[str, list[str]]:
        parts: list[str] = []
        symbols: list[str] = []

        for child in asm_elem.iter():
            tag = etree.QName(child).localname if hasattr(child, "tag") else ""
            if tag == "text" and child.text:
                parts.append(child.text)
            elif tag == "a" and child.text:
                symbol = child.text.strip()
                parts.append(symbol)
                symbols.append(symbol)

        return "".join(parts), symbols

    # ----------------------------------------------------------------
    # 伪代码
    # ----------------------------------------------------------------

    @classmethod
    def _extract_pseudocode_sections(cls, parent: etree._Element, result_list: list[Pseudocode]) -> None:
        for ps_section in parent.findall("ps_section"):
            cls._extract_pseudocode_from_section(ps_section, result_list)

    @classmethod
    def _extract_pseudocode_from_section(cls, ps_section: etree._Element, result_list: list[Pseudocode]) -> None:
        for ps_elem in ps_section.findall("ps"):
            name = ps_elem.get("name", "")
            secttype = ps_elem.get("secttype", "")

            for pstext in ps_elem.findall("pstext"):
                section = pstext.get("section", secttype)
                body = cls._extract_text_with_links(pstext)
                body_plain = cls._get_text(pstext)

                result_list.append(Pseudocode(
                    name=name,
                    section_type=section,
                    body=body,
                    body_plain=body_plain,
                ))

    # ----------------------------------------------------------------
    # 操作数
    # ----------------------------------------------------------------

    @classmethod
    def _parse_explanations(
        cls,
        explanations_elem: etree._Element | None,
        symbol_register_class_map: dict[str, str] | None = None,
    ) -> list[Operand]:
        if explanations_elem is None:
            return []

        reg_map = symbol_register_class_map or {}
        operands: list[Operand] = []
        for expl in explanations_elem.findall("explanation"):
            enclist = expl.get("enclist", "")

            symbol_elem = expl.find("symbol")
            symbol = ""
            symbol_link = ""
            if symbol_elem is not None:
                symbol = (symbol_elem.text or "").strip()
                symbol_link = symbol_elem.get("link", "")

            description = ""
            encoded_in = ""
            value_table: list[dict[str, str]] = []

            # account 形式
            account_elem = expl.find("account")
            if account_elem is not None:
                encoded_in = account_elem.get("encodedin", "")
                intro = account_elem.find("intro")
                if intro is not None:
                    parts = [cls._get_text(p) for p in intro.findall("para")]
                    description = " ".join(parts).strip()

            # definition 形式（含值表）
            def_elem = expl.find("definition")
            if def_elem is not None:
                encoded_in = def_elem.get("encodedin", "")
                intro = def_elem.find("intro")
                if intro is not None:
                    description = cls._get_text(intro).strip()
                table = def_elem.find("table")
                if table is not None:
                    value_table = cls._parse_value_table(table)

            # 从汇编模板上下文获取寄存器类字母
            register_class = reg_map.get(symbol, "")
            register_width = REGISTER_CLASS_WIDTH.get(register_class, 0)

            # 推断操作数类型（利用寄存器类上下文和 encoded_in）
            operand_type = cls._infer_operand_type(symbol, register_class, encoded_in)

            operands.append(Operand(
                symbol=symbol,
                symbol_link=symbol_link,
                description=description,
                encoded_in=encoded_in,
                operand_type=operand_type,
                value_table=value_table,
                encoding_name=enclist,
                register_width=register_width,
                register_class=register_class,
            ))

        return operands

    @classmethod
    def _parse_value_table(cls, table: etree._Element) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        tgroup = table.find("tgroup")
        if tgroup is None:
            return result

        # 列标题
        thead = tgroup.find("thead")
        col_keys: list[str] = []
        if thead is not None:
            for entry in thead.iter("{*}entry"):
                col_keys.append(entry.get("class", ""))

        # 数据行
        tbody = tgroup.find("tbody")
        if tbody is not None:
            for row in tbody.findall("row"):
                entries = row.findall("{*}entry")
                row_data: dict[str, str] = {}
                for i, entry in enumerate(entries):
                    key = col_keys[i] if i < len(col_keys) else f"col{i}"
                    row_data[key] = (entry.text or "").strip()
                result.append(row_data)

        return result

    # ----------------------------------------------------------------
    # 约束
    # ----------------------------------------------------------------

    @classmethod
    def _parse_constraints(cls, constraints_elem: etree._Element | None) -> list[Constraint]:
        if constraints_elem is None:
            return []

        constraints: list[Constraint] = []
        for cu_case in constraints_elem.findall("cu_case"):
            condition = ""
            cu_cause = cu_case.find("cu_cause")
            if cu_cause is not None:
                pstext = cu_cause.find("pstext")
                if pstext is not None:
                    condition = cls._get_text(pstext)

            constraint_type = ""
            description = ""
            cu_type = cu_case.find("cu_type")
            if cu_type is not None:
                constraint_type = cu_type.get("constraint", "")
                description = (cu_type.text or "").strip()

            constraints.append(Constraint(
                constraint_type=constraint_type,
                condition=condition,
                description=description,
            ))

        return constraints

    # ----------------------------------------------------------------
    # encoding 级约束提取
    # ----------------------------------------------------------------

    @staticmethod
    def _extract_encoding_constraints(
        pseudocode_list: list[Pseudocode],
        xml_id: str = "",
    ) -> list[Constraint]:
        """从伪代码中提取 encoding 级约束。

        委托给 EncodingConstraintExtractor 进行模式匹配和结构化提取。
        """
        if not pseudocode_list:
            return []
        return EncodingConstraintExtractor.extract_from_pseudocode(
            pseudocode_list, instruction_xml_id=xml_id,
        )

    @staticmethod
    def _build_pseudocode_encoding_map(
        pseudocode_list: list[Pseudocode],
        encodings: list[Encoding],
    ) -> dict[str, str]:
        """构建 伪代码名 → encoding.name 的映射。

        匹配规则：伪代码名最后一段（最后一个 ``.`` 之后）== encoding.name。

        Examples:
            Pseudocode: ``A64.simd_dp.asisdmisc.ABS_asisdmisc_R``
            Encoding:   ``ABS_asisdmisc_R``  →  匹配

            Pseudocode: ``A64.simd_dp.asimdmisc.ABS_asimdmisc_R``
            Encoding:   ``ABS_asimdmisc_R``  →  匹配
        """
        enc_names: set[str] = {e.name for e in encodings}
        mapping: dict[str, str] = {}
        for ps in pseudocode_list:
            last_seg = ps.name.split(".")[-1] if "." in ps.name else ps.name
            if last_seg in enc_names:
                mapping[ps.name] = last_seg
        return mapping

    # ----------------------------------------------------------------
    # 操作备注
    # ----------------------------------------------------------------

    @classmethod
    def _parse_operational_notes(cls, notes_elem: etree._Element | None) -> str:
        if notes_elem is None:
            return ""
        parts: list[str] = []
        for onote in notes_elem.findall("operationalnote"):
            content = onote.find("operationalnote_content")
            if content is not None:
                parts.append(cls._get_text(content))
        return "\n\n".join(parts)

    # ----------------------------------------------------------------
    # 共享伪代码
    # ----------------------------------------------------------------

    @classmethod
    def _parse_shared_ps_element(cls, ps_elem: etree._Element) -> SharedPseudocodeFunction:
        name = ps_elem.get("name", "")
        secttype = ps_elem.get("secttype", "Library")
        link_id = ps_elem.get("mylink", "")

        body_parts: list[str] = []
        first_line = ""
        for pstext in ps_elem.findall("pstext"):
            text_content = cls._extract_text_content(pstext)
            body_parts.append(text_content)
            if not first_line:
                first_line = cls._extract_first_signature(pstext)

        full_body = "\n".join(body_parts)

        return SharedPseudocodeFunction(
            name=name,
            signature=first_line,
            body=full_body,
            link_id=link_id,
        )

    # ----------------------------------------------------------------
    # 文本提取工具
    # ----------------------------------------------------------------

    @staticmethod
    def _get_text(elem: etree._Element) -> str:
        """递归提取所有文本（不含标签）。"""
        return "".join(str(t) for t in elem.itertext()).strip()

    @classmethod
    def _extract_text_with_links(cls, pstext: etree._Element) -> str:
        """提取文本但保留交叉引用 <a> 标记。"""
        result = etree.tostring(pstext, encoding="unicode", method="text")
        if not result:
            result = cls._get_text(pstext)
        return result.strip()

    @classmethod
    def _extract_text_content(cls, pstext: etree._Element) -> str:
        return cls._get_text(pstext)

    @classmethod
    def _extract_first_signature(cls, pstext: etree._Element) -> str:
        text = cls._get_text(pstext)
        lines = text.split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                return stripped
        return lines[0].strip() if lines else ""

    @staticmethod
    def _element_to_string(elem: etree._Element) -> str:
        return etree.tostring(elem, encoding="unicode").strip()

    # ----------------------------------------------------------------
    # 辅助方法
    # ----------------------------------------------------------------

    @staticmethod
    def _safe_int(value: str | None) -> int:
        """安全地转换字符串为 int，失败返回 0。"""
        if value is None:
            return 0
        try:
            return int(value)
        except ValueError:
            return 0

    @staticmethod
    def _dedup_arch_variants(variants: list[ArchVariant]) -> list[ArchVariant]:
        seen: set[str] = set()
        result: list[ArchVariant] = []
        for av in variants:
            if av.feature not in seen:
                seen.add(av.feature)
                result.append(av)
        return result

    @staticmethod
    def _build_symbol_register_class_map(encodings: list[Encoding]) -> dict[str, str]:
        """从所有 encoding 的汇编模板中提取 操作数符号 → 寄存器类字母 的映射。

        示例：
            "ABS  D<d>, D<n>"  →  {"<d>": "D", "<n>": "D"}
            "ABS  <Vd>.<T>, <Vn>.<T>"  →  {"<Vd>": "V", "<Vn>": "V"}

        策略：
            1. 查找符号前一字符（如 D<d> 中的 D）
            2. 若符号名首字符为已知寄存器类字母（如 <Vd> 中的 V），取之
        """
        mapping: dict[str, str] = {}
        for enc in encodings:
            template = enc.assembly_template
            for sym in enc.operand_symbols:
                # 策略 1：汇编模板中符号前紧邻的字母
                escaped = re.escape(sym)
                m = re.search(rf"([A-Z]){escaped}", template)
                if m:
                    first_char = m.group(1)
                    if first_char in REGISTER_CLASS_WIDTH:
                        mapping[sym] = first_char
                        continue

                # 策略 2：符号名本身的首字符
                inner = sym.strip("<>")
                if inner and inner[0] in REGISTER_CLASS_WIDTH:
                    mapping[sym] = inner[0]

        return mapping

    @staticmethod
    def _infer_operand_type(symbol: str, register_class: str = "", encoded_in: str = "") -> str:
        """根据操作数符号、寄存器类上下文和编码字段推断类型。

        Args:
            symbol: 操作数符号 (如 <d>, <Xd>, <label>)
            register_class: 汇编模板中该符号前的寄存器类字母 (如 D/X/V)
            encoded_in: 编码字段名 (如 size:Q，用于检测 arrangement)
        """
        if not symbol:
            return "unknown"
        sym = symbol.strip("<>")

        # ── 排列说明符（arrangement）──
        # <T> 类型由 size:Q 等组合字段编码决定
        if sym in ("T",) and (":" in encoded_in):
            return "arrangement"

        # ── 基于汇编模板上下文确定寄存器 ──
        if register_class and register_class in REGISTER_CLASS_WIDTH:
            return "register"

        # ── 基于符号名推断 ──
        # 寄存器名（补上 X 类字母）
        if re.match(r"[WSBVQZX]d|[WSBVQZX]n|[WSBVQZX]m|[WSBVQZX]a|[WSBVQZX]t", sym):
            return "register"
        if re.match(r"[SDHB]\d+", sym):
            return "register"
        if re.match(r"[VZ]\w+\.", sym):
            return "register"
        if re.match(r"[PVZ]\d+", sym):
            return "register"

        # 条件码
        if sym in ("cond",):
            return "condition"

        # 立即数
        if "imm" in sym.lower() or sym.startswith("#"):
            return "immediate"

        # 标签
        if "label" in sym.lower():
            return "label"

        # 内存寻址
        if "[" in sym:
            return "memory"

        # 移位
        if "shift" in sym.lower() or "lsl" in sym.lower() or "extend" in sym.lower():
            return "shift"

        # 向量排列（如 2s, 4s, 8b 等）
        if re.search(r"\d[sd]\b", sym, re.IGNORECASE):
            return "vector_arrangement"
        if re.match(r"\{.*\}", sym):
            return "register_list"

        return "unknown"

    # ----------------------------------------------------------------
    # 位模式计算
    # ----------------------------------------------------------------

    @classmethod
    def _compute_bit_pattern(cls, bitfields: list[BitfieldValue]) -> tuple[str, str]:
        """从 encoding 级别 bitfields 计算位模式和掩码。

        Returns:
            (pattern, mask) —— pattern 中 0/1 为固定位，? 为可变位；
            mask 中 1 为固定位，0 为可变位。
        """
        if not bitfields:
            return "", ""

        pattern = ["?"] * 32
        mask = ["0"] * 32

        for bf in bitfields:
            hibit = bf.hibit
            width = bf.width
            for i in range(width):
                bit_pos = hibit - i
                if bit_pos < 0 or bit_pos >= 32:
                    continue
                if i < len(bf.values) and bf.values[i]:
                    val = bf.values[i]
                    if val in ("0", "1"):
                        pattern[bit_pos] = val
                        mask[bit_pos] = "1"

        return "".join(pattern), "".join(mask)
