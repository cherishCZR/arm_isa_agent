"""Encoding 约束提取器。

从指令伪代码（Decode / Postdecode 段）中提取五类 encoding 约束：

1. **FEATURE_GATE** (特性门控)
   - if !IsFeatureImplemented(FEAT_XXX) then EndOfDecode(Decode_NOP/UNDEF)
   - 支持复合条件：&& / || / 括号分组
   - 支持编码字段 + 特性组合：sz == '1' && !IsFeatureImplemented(FEAT_X)

2. **ENCODING_UNDEF** (编码位约束 → UNDEF)
   - if imm3 IN {'101', '110', '111'} then EndOfDecode(Decode_UNDEF);
   - if shift == '11' then EndOfDecode(Decode_UNDEF);
   - if sf == '0' && imm6<5> == '1' then EndOfDecode(Decode_UNDEF);
   - case sz:L of when '11' EndOfDecode(Decode_UNDEF);   ← NEW
   - EndOfDecode(Decode_UNDEF);  (always undefined)       ← NEW

3. **CONSTRAINED_UNPREDICTABLE** (受约束的不可预测行为)
   - c = ConstrainUnpredictable(Unpredictable_XXX)

4. **DECODE_FALLBACK** (otherwise 兜底)
   - otherwise EndOfDecode(Decode_NOP);
   - 多编码指令的非匹配分支

5. **encoding 级字段约束** (纯字段检查，不含 IsFeatureImplemented)
   - 归类为 ENCODING_UNDEF
"""

from __future__ import annotations

import re
from typing import ClassVar, Pattern

from arm_isa_agent.core.models.instruction import Constraint, Pseudocode


_EFFECT_LABEL: dict[str, str] = {
    "Decode_NOP": "NOP",
    "Decode_UNDEF": "UNDEFINED",
    "Decode_OK": "OK",
}


class EncodingConstraintExtractor:
    """从伪代码文本中提取 encoding 级别的约束。"""

    # ── 约束模式定义 ──────────────────────────────────────────────

    # 1. if/elsif ... then EndOfDecode(Decode_UNDEF/NOP) ─ 通用捕获
    #    覆盖：Feature Gate、纯编码位约束、混合约束
    #    关键设计：
    #      - (?<![=;])  避免匹配三元表达式中的 if (= if、; if)
    #      - (?:if|elsif) 同时支持 if 和 elsif
    #      - (?:(?!\bthen\b).)+?  非贪婪匹配条件部分，但不跨越 then 关键字
    #      - DOTALL  允许条件跨行（如 bfdot_z_zzz 的 \n 续行条件）
    #      - \s*     then 和 EndOfDecode 之间可能是空格或换行
    IF_THEN_END_OF_DECODE: ClassVar[Pattern[str]] = re.compile(
        r"(?<![=;])\s*(?:if|elsif)\b\s+"
        r"(?P<condition>(?:(?!\bthen\b).)+?)\s+then\s*"
        r"EndOfDecode\((?P<effect>Decode_\w+)\)\s*;?",
        re.MULTILINE | re.DOTALL,
    )

    # 2. ConstrainUnpredictable 模式（含前提条件）：
    #    if (condition) then
    #        c = ConstrainUnpredictable(Unpredictable_XXX);
    CONSTRAIN_UNPREDICTABLE: ClassVar[Pattern[str]] = re.compile(
        r"(?<![=;])\s*if\s+(?P<condition>[^;]+?)\s+then\s*"
        r"\n?\s*c\s*=\s*ConstrainUnpredictable\((?P<unpred>Unpredictable_\w+)\)",
        re.MULTILINE,
    )

    # 3. 独立 ConstrainUnpredictable（无条件）：
    #    ConstrainUnpredictable(Unpredictable_XXX)
    CONSTRAIN_UNPREDICTABLE_BARE: ClassVar[Pattern[str]] = re.compile(
        r"ConstrainUnpredictable\((?P<unpred>Unpredictable_\w+)\)",
        re.MULTILINE,
    )

    # 4. 可能结果断言：
    #    assert c IN {Constraint_XXX, ...};
    CONSTRAINT_ASSERT: ClassVar[Pattern[str]] = re.compile(
        r"assert\s+c\s+IN\s+\{(?P<effects>[^}]+)\}",
        re.MULTILINE,
    )

    # 5. case 分支效果：
    #    when Constraint_WBSUPPRESS wback = FALSE;
    CONSTRAINT_CASE: ClassVar[Pattern[str]] = re.compile(
        r"when\s+(?P<effect>Constraint_\w+)\s+(?P<action>.+?);",
        re.MULTILINE,
    )

    # 6. otherwise → Decode_NOP/UNDEF（多编码指令的兜底分支）
    OTHERWISE_DECODE: ClassVar[Pattern[str]] = re.compile(
        r"otherwise\s+EndOfDecode\((?P<effect>Decode_\w+)\)",
        re.MULTILINE,
    )

    # 7. case <field> of ... when '<value>' EndOfDecode(Decode_UNDEF/NOP)
    #    case sz:L of
    #        when '11' EndOfDecode(Decode_UNDEF);
    #    → constraint_type="ENCODING_UNDEF", condition="sz:L == '11'"
    CASE_WHEN_END_OF_DECODE: ClassVar[Pattern[str]] = re.compile(
        r"\bwhen\s+'(?P<value>[^']+)'\s+EndOfDecode\((?P<effect>Decode_\w+)\)\s*;?",
        re.MULTILINE,
    )

    # 8. 无条件裸 EndOfDecode（始终 UNDEF/NOP 的指令）
    #    EndOfDecode(Decode_UNDEF);
    #    → constraint_type="ENCODING_UNDEF", condition="(always undefined)"
    BARE_END_OF_DECODE: ClassVar[Pattern[str]] = re.compile(
        r"^EndOfDecode\((?P<effect>Decode_\w+)\)\s*;?$",
        re.MULTILINE,
    )

    # ── 公开 API ─────────────────────────────────────────────────

    @classmethod
    def extract_from_pseudocode(
        cls,
        pseudocode_list: list[Pseudocode],
        instruction_xml_id: str = "",
    ) -> list[Constraint]:
        """从伪代码列表中提取 encoding 约束。

        Args:
            pseudocode_list: Pseudocode 对象列表
            instruction_xml_id: 指令 XML ID（用于日志）

        Returns:
            Constraint 对象列表
        """
        constraints: list[Constraint] = []

        # 只分析 Decode / Postdecode 段
        decode_sections = [
            ps for ps in pseudocode_list
            if ps.section_type.lower() in ("decode", "postdecode")
        ]

        for ps in decode_sections:
            body = ps.body_plain or ps.body
            if not body:
                continue

            # ── 解析伪代码中的变量赋值（如 tsize = tszh:tszl）──
            var_map = cls._parse_variable_assignments(body)

            # ── 提取所有约束（先收集到临时列表，再统一做变量解析）──
            section_constraints: list[Constraint] = []

            # 1. if/elsif ... then EndOfDecode(...) 约束 ──
            cls._extract_if_then_decode_constraints(body, instruction_xml_id, section_constraints)

            # 2. case <field> of ... when 'XX' EndOfDecode(...) ──
            cls._extract_case_when_decode_constraints(body, instruction_xml_id, section_constraints)

            # 3. ConstrainUnpredictable 约束 ──
            cls._extract_constrained_unpredictable(body, instruction_xml_id, section_constraints)

            # 4. otherwise 兜底 ──
            cls._extract_bare_decode_fallbacks(body, instruction_xml_id, section_constraints)

            # 5. 无条件裸 EndOfDecode ──
            cls._extract_bare_end_of_decode(body, instruction_xml_id, section_constraints)

            # ── 变量解析 + 标记来源 ──
            for c in section_constraints:
                if var_map:
                    c.condition = cls._resolve_variables(c.condition, var_map)
                c.source_section = ps.name  # 记录该约束来自哪个伪代码段

            constraints.extend(section_constraints)

        constraints = cls._deduplicate(constraints)

        # ── 条件取反：从"何时 UNDEF"转为"何时有效" ──
        for c in constraints:
            c.condition, c.description = cls._invert_condition_and_description(
                c.condition, c.description, c.constraint_type,
            )

        return constraints

    # ── 私有提取方法 ──────────────────────────────────────────────

    @classmethod
    def _extract_if_then_decode_constraints(
        cls,
        body: str,
        xml_id: str,
        constraints: list[Constraint],
    ) -> None:
        """提取所有 if/elsif ... then EndOfDecode(Decode_UNDEF/NOP) 模式。

        分类规则：
            - 条件含 IsFeatureImplemented → FEATURE_GATE
            - 条件不含 IsFeatureImplemented → ENCODING_UNDEF

        Examples:
            FEATURE_GATE:
                if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
                    EndOfDecode(Decode_UNDEF);
                if sz == '1' && !IsFeatureImplemented(FEAT_SME_I16I64) then EndOfDecode(Decode_UNDEF);

            ENCODING_UNDEF:
                if imm3 IN {'101', '110', '111'} then EndOfDecode(Decode_UNDEF);
                if sf == '0' && imm6<5> == '1' then EndOfDecode(Decode_UNDEF);
                if shift == '11' then EndOfDecode(Decode_UNDEF);
                if !(tsize IN {'001', '010', '100'}) then EndOfDecode(Decode_UNDEF);
        """
        for m in cls.IF_THEN_END_OF_DECODE.finditer(body):
            condition = cls._clean_condition(m.group("condition"))
            effect = m.group("effect")
            effect_label = _EFFECT_LABEL.get(effect, effect)

            # 分类
            if "IsFeatureImplemented" in condition:
                constraint_type = "FEATURE_GATE"
                # 提取特性名用于可读描述
                features = re.findall(r"FEAT_\w+", condition)
                feat_list = ", ".join(features)
                description = f"When {feat_list} not implemented → {effect_label}"
            else:
                constraint_type = "ENCODING_UNDEF"
                description = f"Reserved encoding: {condition} → {effect_label}"

            constraints.append(Constraint(
                constraint_type=constraint_type,
                condition=condition,
                description=description,
            ))

    @classmethod
    def _extract_constrained_unpredictable(
        cls,
        body: str,
        xml_id: str,
        constraints: list[Constraint],
    ) -> None:
        r"""提取 ConstrainUnpredictable 约束。

        Example:
            输入:
                if wback && n == t && n != 31 then
                    c = ConstrainUnpredictable(Unpredictable_WBOVERLAPLD);
                    assert c IN {Constraint_WBSUPPRESS, Constraint_UNKNOWN,
                                 Constraint_UNDEF, Constraint_NOP};
                    case c of
                        when Constraint_WBSUPPRESS wback = FALSE;
                        when Constraint_UNKNOWN    wb_unknown = TRUE;
                        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
                        when Constraint_NOP        EndOfDecode(Decode_NOP);

            输出:
                constraint_type="CONSTRAINED_UNPREDICTABLE"
                condition="wback && n == t && n != 31"
                description="Unpredictable_WBOVERLAPLD → WBSUPPRESS/UNKNOWN/UNDEF/NOP"
        """
        for m in cls.CONSTRAIN_UNPREDICTABLE.finditer(body):
            condition = cls._clean_condition(m.group("condition"))
            unpred = m.group("unpred")

            # 尝试提取可能结果
            effects_desc = ""
            search_start = m.end()
            tail = body[search_start:search_start + 500]

            assert_m = cls.CONSTRAINT_ASSERT.search(tail)
            if assert_m:
                effects_text = assert_m.group("effects")
                effects = [e.strip() for e in effects_text.split(",")]
                effects_desc = " → " + "/".join(
                    e.replace("Constraint_", "") for e in effects
                )

                # 尝试提取 case 分支的行为描述
                case_descriptions: list[str] = []
                for case_m in cls.CONSTRAINT_CASE.finditer(tail):
                    effect_name = case_m.group("effect").replace("Constraint_", "")
                    action = case_m.group("action").strip()
                    case_descriptions.append(f"{effect_name}={action}")
                if case_descriptions:
                    effects_desc += " [" + "; ".join(case_descriptions) + "]"

            constraints.append(Constraint(
                constraint_type="CONSTRAINED_UNPREDICTABLE",
                condition=condition,
                description=f"{unpred}{effects_desc}",
            ))

    @classmethod
    def _extract_bare_decode_fallbacks(
        cls,
        body: str,
        xml_id: str,
        constraints: list[Constraint],
    ) -> None:
        """提取无条件 Decode fallback（如 HINT 的 otherwise 分支）。

        Example:
            输入: otherwise EndOfDecode(Decode_NOP);
            输出: constraint_type="DECODE_FALLBACK"
                  condition="otherwise (non-matching encodings)"
                  description="Non-matching encodings → NOP"
        """
        for m in cls.OTHERWISE_DECODE.finditer(body):
            effect = m.group("effect")
            effect_label = _EFFECT_LABEL.get(effect, effect)
            constraints.append(Constraint(
                constraint_type="DECODE_FALLBACK",
                condition="otherwise (non-matching encodings)",
                description=f"Non-matching encodings → {effect_label}",
            ))

    @classmethod
    def _extract_case_when_decode_constraints(
        cls,
        body: str,
        xml_id: str,
        constraints: list[Constraint],
    ) -> None:
        r"""提取 case/when → EndOfDecode 编码字段约束。

        Examples:
            case sz:L of
                when '11' EndOfDecode(Decode_UNDEF);

            → constraint_type="ENCODING_UNDEF"
              condition="sz:L == '11'"
              description="Reserved encoding: sz:L == '11' → UNDEFINED"
        """
        for m in cls.CASE_WHEN_END_OF_DECODE.finditer(body):
            value = m.group("value")
            effect = m.group("effect")
            effect_label = _EFFECT_LABEL.get(effect, effect)

            # 查找所属的 case block 以获取字段名
            body_before = body[:m.start()]
            field_match = re.search(
                r"case\s+(?P<field>\w+(?::\w+)*)\s+of\s*$",
                body_before, re.MULTILINE,
            )
            # 如果没匹配到（非锚点到行尾），尝试匹配整行（允许跨 inline 内容）
            if not field_match:
                # 查找最后出现的 "case <field> of" 在 when 之前
                all_cases = list(re.finditer(
                    r"case\s+(\w+(?::\w+)*)\s+of",
                    body_before, re.MULTILINE,
                ))
                if all_cases:
                    field_match = all_cases[-1]  # 取最近的

            if field_match:
                field = field_match.group("field")
            else:
                field = "?"  # fallback

            # 处理通配符值（如 '0x', '1x'）→ 用 NOT IN 语义
            if "x" in value:
                condition = f"{field} NOT IN compatible values"
            else:
                condition = f"{field} == '{value}'"

            description = f"Reserved encoding: {condition} → {effect_label}"

            constraints.append(Constraint(
                constraint_type="ENCODING_UNDEF",
                condition=condition,
                description=description,
            ))

    @classmethod
    def _extract_bare_end_of_decode(
        cls,
        body: str,
        xml_id: str,
        constraints: list[Constraint],
    ) -> None:
        r"""提取无条件的裸 EndOfDecode（始终 UNDEF/POKE 的指令）。

        Example:
            输入:
                // The imm16 field is ignored by hardware.
                EndOfDecode(Decode_UNDEF);

            输出: constraint_type="ENCODING_UNDEF"
                  condition="(always undefined)"
                  description="Instruction always → UNDEFINED"
        """
        for m in cls.BARE_END_OF_DECODE.finditer(body):
            effect = m.group("effect")
            effect_label = _EFFECT_LABEL.get(effect, effect)

            constraints.append(Constraint(
                constraint_type="ENCODING_UNDEF",
                condition=f"(always {effect_label.lower()})",
                description=f"Instruction unconditionally → {effect_label}",
            ))

    # ── 辅助方法 ─────────────────────────────────────────────────

    @staticmethod
    def _deduplicate(constraints: list[Constraint]) -> list[Constraint]:
        """去除重复约束（按 constraint_type + condition 去重），保持顺序。

        若同一约束出现在多个不同伪代码段中（source_section 不同），
        则标记为共享约束（清空 source_section），后续由 card builder 放到末尾公共区。
        """
        from collections import defaultdict

        source_counts: dict[tuple[str, str], set[str]] = defaultdict(set)
        for c in constraints:
            key = (c.constraint_type, c.condition.strip())
            if c.source_section:
                source_counts[key].add(c.source_section)

        seen: set[tuple[str, str]] = set()
        result: list[Constraint] = []
        for c in constraints:
            key = (c.constraint_type, c.condition.strip())
            if key not in seen:
                seen.add(key)
                result.append(c)

        # 多 section → 清空 source_section（标记为共享）
        for c in result:
            key = (c.constraint_type, c.condition.strip())
            sources = source_counts.get(key, set())
            if len(sources) > 1:
                c.source_section = ""

        return result

    @staticmethod
    def _clean_condition(condition: str) -> str:
        """清理约束条件文本（去除多余空白、换行、伪注释）。"""
        # 折叠空白
        cond = re.sub(r"\s+", " ", condition).strip()
        # 移除单行注释 //
        cond = re.sub(r"\s*//.*$", "", cond, flags=re.MULTILINE)
        # 紧凑化运算符
        cond = re.sub(r"\s*&&\s*", " && ", cond)
        cond = re.sub(r"\s*\|\|\s*", " || ", cond)
        cond = re.sub(r"\s*==\s*", " == ", cond)
        cond = re.sub(r"\s*!=\s*", " != ", cond)
        cond = re.sub(r"\s*<=\s*", " <= ", cond)
        cond = re.sub(r"\s*<\s+", " < ", cond)
        cond = re.sub(r"\s+\|\|\s+", " || ", cond)  # 持久化 ||
        return cond.strip()

    # ── 伪代码变量 → 编码字段名解析 ─────────────────────────────

    @staticmethod
    def _parse_variable_assignments(body: str) -> dict[str, str]:
        """解析伪代码中的 ``constant bits(N) VAR = field_expr;`` 赋值。

        只收集简单的字段拼接表达式（含 ``:``），忽略复杂表达式。

        Example:
            body: ``constant bits(4) tsize = tszh:tszl;``
            →   {"tsize": "tszh:tszl"}
        """
        var_map: dict[str, str] = {}
        for m in re.finditer(
            r"constant\s+bits\(\d+\)\s+(\w+)\s*=\s*([\w:]+)\s*;",
            body,
        ):
            var_name = m.group(1)
            field_expr = m.group(2)
            # 只解析字段拼接（含 ':'），忽略纯变量或复杂表达式
            if ":" in field_expr:
                var_map[var_name] = field_expr
        return var_map

    @staticmethod
    def _resolve_variables(condition: str, var_map: dict[str, str]) -> str:
        """将条件中的伪代码变量替换为对应的编码字段名。

        按变量名长度降序替换，避免部分匹配（如 esize 误匹配 size）。
        """
        for var in sorted(var_map, key=len, reverse=True):
            condition = re.sub(r"\b" + re.escape(var) + r"\b", var_map[var], condition)
        return condition

    # ── 条件取反工具 ────────────────────────────────────────────
    #  将伪代码中的"何时 UNDEF"条件取反为"何时有效"条件

    @staticmethod
    def _invert_condition_and_description(
        condition: str,
        description: str,
        constraint_type: str,
    ) -> tuple[str, str]:
        """将约束条件取反（UNDEF → 有效），同时更新描述。

        对 FEATURE_GATE / ENCODING_UNDEF / DECODE_FALLBACK 取反；
        CONSTRAINED_UNPREDICTABLE 保持原样（描述不可预测发生的条件）。
        """
        if constraint_type in ("FEATURE_GATE", "ENCODING_UNDEF", "DECODE_FALLBACK"):
            negated = EncodingConstraintExtractor._negate_expression(condition)
            # 更新描述
            if constraint_type == "FEATURE_GATE":
                new_desc = re.sub(r"When .+ not implemented → \w+",
                                  r"Required features satisfied → valid", description)
            elif constraint_type == "ENCODING_UNDEF":
                new_desc = re.sub(r"Reserved encoding: .+ → \w+",
                                  r"Valid encoding → instruction executes", description)
                new_desc = re.sub(r"Instruction unconditionally → \w+",
                                  r"Instruction never valid (always UNDEF)", new_desc)
            elif constraint_type == "DECODE_FALLBACK":
                new_desc = re.sub(r"Non-matching encodings → \w+",
                                  r"Matching encodings → valid", description)
            return negated, new_desc
        return condition, description

    @staticmethod
    def _negate_expression(expr: str) -> str:
        r"""对约束条件表达式做逻辑取反（De Morgan）。

        原子层替换：
            !IsFeatureImplemented(X)  ↔  IsFeatureImplemented(X)
            IN {…}                   ↔  NOT IN {…}
            !=                       ↔  ==
        运算符层替换（De Morgan）：
            &&                       ↔  ||

        特殊字符串（不取反）：
            ``(always …)``           → ``(never valid)``
            ``otherwise (...)``      → ``matching encodings``
        """
        s = expr.strip()

        # ── 特殊字符串处理 ──
        if s.startswith("(always "):
            return "(never valid)"
        if s.startswith("otherwise"):
            return "matching encodings"

        # ── 1. 处理 !(expr) 外层取反（!(A) → A，后续运算符交换会完成 De Morgan）──
        if s.startswith("!("):
            depth = 0
            end = -1
            for i, ch in enumerate(s):
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        end = i
                        break
            if end == len(s) - 1:
                # 纯 !(expr) 形式 — 剥离 !() 并对内部取反
                inner = s[2:end]
                # 内层直接走原子+运算符交换
                return EncodingConstraintExtractor._apply_de_morgan(inner)
            if end > 0:
                # 复合形式：!(A) || B  — 先剥 !(A)，整体取反
                after = s[end + 1:]
                inner = s[2:end]
                neg_inner = EncodingConstraintExtractor._apply_de_morgan(inner)
                # !(A) → neg(A), 然后整体取反
                return EncodingConstraintExtractor._apply_de_morgan(
                    f"({neg_inner}){after}"
                )

        # ── 2. 标准 De Morgan 变换 ──
        return EncodingConstraintExtractor._apply_de_morgan(s)

    @staticmethod
    def _apply_de_morgan(s: str) -> str:
        """De Morgan 变换：原子取反 + 运算符交换。"""
        # (a) !IsFeatureImplemented ↔ IsFeatureImplemented
        s = s.replace("!IsFeatureImplemented(", "__TAG_FEAT_NOT__")
        s = re.sub(r"(?<![!_])IsFeatureImplemented\(", "!IsFeatureImplemented(", s)
        s = s.replace("__TAG_FEAT_NOT__", "IsFeatureImplemented(")

        # (b) NOT IN ↔ IN（用临时标记防二次交换）
        s = s.replace(" NOT IN ", " __TAG_NOT_IN__ ")
        s = s.replace(" IN ", " NOT IN ")
        s = s.replace(" __TAG_NOT_IN__ ", " IN ")

        # 处理带 {  的 IN（可能前后无空格）
        s = re.sub(r"\bNOT IN\s*\{", "__TAG_NI__{", s)
        s = re.sub(r"\bIN\s*\{", "NOT IN{", s)
        s = s.replace("__TAG_NI__{", "IN{")

        # (c) != ↔ ==
        s = s.replace(" != ", " __TAG_NE__ ")
        s = s.replace(" == ", " != ")
        s = s.replace(" __TAG_NE__ ", " == ")

        # (d) && ↔ ||  (De Morgan 定理)
        s = s.replace(" && ", " __TAG_AND__ ")
        s = s.replace(" || ", " && ")
        s = s.replace(" __TAG_AND__ ", " || ")

        return s.strip()
