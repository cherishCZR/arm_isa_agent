"""Unit tests for XML Parser."""

from __future__ import annotations

import pytest
from arm_isa_agent.etl.xml_parser import XMLInstructionParser


class TestXMLInstructionParser:

    def test_parse_adr(self, sample_xml_files):
        """测试解析 ADR 指令 (简单单编码指令)."""
        result = XMLInstructionParser.parse_file(sample_xml_files["adr"])
        assert result.ok
        inst = result.instruction

        assert inst.xml_id == "ADR"
        assert inst.mnemonic == "ADR"
        assert inst.instruction_type == "instruction"
        assert inst.instr_class == "general"
        assert "PC-relative" in inst.brief

        # 编码
        assert len(inst.encodings) == 1
        enc = inst.encodings[0]
        assert enc.name == "ADR_only_pcreladdr"
        assert "ADR" in enc.assembly_template
        assert "<Xd>" in enc.assembly_template
        assert "<label>" in enc.assembly_template

        # 编码图 —— 移至 encoding 级别
        assert len(inst.encodings[0].regdiagram_bitfields) > 0
        rd_field = [bf for bf in inst.encodings[0].regdiagram_bitfields if bf.name == "Rd"]
        assert len(rd_field) > 0

        # 操作数
        assert len(inst.operands) > 0
        symbols = [op.symbol for op in inst.operands]
        assert "<Xd>" in symbols or any("Xd" in s for s in symbols)

        # 寄存器操作数应有位宽和类
        xd_ops = [op for op in inst.operands if "Xd" in op.symbol]
        assert len(xd_ops) > 0
        assert xd_ops[0].operand_type == "register"
        assert xd_ops[0].register_width == 64
        assert xd_ops[0].register_class == "X"

        # 伪代码
        assert len(inst.pseudocode_list) > 0
        sections = [ps.section_type for ps in inst.pseudocode_list]
        assert "Decode" in sections or "Execute" in sections

    def test_parse_b_cond(self, sample_xml_files):
        """测试解析 B.cond 指令 (含值表条件码)."""
        result = XMLInstructionParser.parse_file(sample_xml_files["b_cond"])
        assert result.ok
        inst = result.instruction

        assert inst.xml_id == "B_cond"
        assert inst.mnemonic == "B"

        # 操作数 —— 检查 cond 值表
        cond_ops = [op for op in inst.operands if "cond" in op.symbol.lower()]
        assert len(cond_ops) > 0
        cond_op = cond_ops[0]
        assert cond_op.operand_type == "condition"
        assert len(cond_op.value_table) > 0
        # EQ = 0000
        eq_entry = [r for r in cond_op.value_table if r.get("symbol", "") == "EQ"]
        assert len(eq_entry) > 0

    def test_parse_alias(self, sample_xml_files):
        """测试解析别名指令 ASR (immediate)."""
        result = XMLInstructionParser.parse_file(sample_xml_files["asr_sbfm"])
        assert result.ok
        inst = result.instruction

        assert inst.instruction_type == "alias"
        assert inst.is_alias is True
        assert inst.alias_of == "sbfm.xml"
        assert inst.alias_of_id == "SBFM"
        assert inst.mnemonic == "SBFM"

        # 应该有多个 encoding (32-bit + 64-bit)
        assert len(inst.encodings) == 2

        # 32-bit encoding
        enc_32 = [e for e in inst.encodings if e.label == "32-bit"]
        assert len(enc_32) == 1

        # 64-bit encoding
        enc_64 = [e for e in inst.encodings if e.label == "64-bit"]
        assert len(enc_64) == 1

        # bitdiffs
        assert enc_32[0].bitdiffs != ""

    def test_parse_ldr_lit_fpsimd(self, sample_xml_files):
        """测试解析多编码指令 LDR (literal, SIMD&FP)."""
        result = XMLInstructionParser.parse_file(sample_xml_files["ldr_lit_fpsimd"])
        assert result.ok
        inst = result.instruction

        assert inst.instr_class == "fpsimd"
        assert inst.mnemonic == "LDR"

        # 3 个 encoding
        assert len(inst.encodings) == 3

        labels = [e.label for e in inst.encodings]
        assert "32-bit" in labels
        assert "64-bit" in labels
        assert "128-bit" in labels

        # 架构变体
        assert len(inst.arch_variants) > 0
        features = [av.feature for av in inst.arch_variants]
        assert "FEAT_FP" in features

    def test_parse_add_za_zzw(self, sample_xml_files):
        """测试解析 SME 多 iclass 指令."""
        result = XMLInstructionParser.parse_file(sample_xml_files["add_za_zzw"])
        assert result.ok
        inst = result.instruction

        assert inst.instr_class == "mortlach2"  # SME

        # SME2 特性
        features = [av.feature for av in inst.arch_variants]
        assert "FEAT_SME2" in features

        # 应有操作属性
        assert inst.uses_dit is True

        # 多个 iclass → 每个 encoding 应有独立 regdiagram
        assert len(inst.encodings) == 2
        for enc in inst.encodings:
            assert len(enc.regdiagram_bitfields) > 0, (
                f"Encoding '{enc.name}' should have regdiagram_bitfields"
            )

    def test_parse_shared_pseudocode(self, sample_xml_files):
        """测试解析共享伪代码文件."""
        funcs, errors = XMLInstructionParser.parse_shared_pseudocode(sample_xml_files["shared_ps"])
        assert len(funcs) > 0

