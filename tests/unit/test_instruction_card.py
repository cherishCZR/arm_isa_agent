"""Unit tests for Instruction Card Builder."""

from __future__ import annotations

from arm_isa_agent.etl.instruction_card_builder import InstructionCardBuilder
from arm_isa_agent.etl.xml_parser import XMLInstructionParser


class TestInstructionCardBuilder:

    def test_build_adr_card(self, sample_xml_files):
        """测试为 ADR 生成 Card."""
        inst = XMLInstructionParser.parse_file(sample_xml_files["adr"])
        assert inst is not None

        card = InstructionCardBuilder.build(inst)

        # 基本结构
        assert "## ADR" in card
        assert "**Summary**" in card
        assert "**Description**" in card
        assert "### Encoding" in card or "### Encoding Variant" in card
        assert "### Operands" in card
        assert "### Pseudocode" in card
        assert "`adr.xml`" in card

    def test_build_alias_card(self, sample_xml_files):
        """测试为别名生成 Card."""
        inst = XMLInstructionParser.parse_file(sample_xml_files["asr_sbfm"])
        assert inst is not None

        card = InstructionCardBuilder.build(inst)

        assert "[ALIAS]" in card
        assert "**Alias of**" in card
        assert "sbfm.xml" in card

    def test_build_card_metadata(self, sample_xml_files):
        """测试 Card 元数据."""
        inst = XMLInstructionParser.parse_file(sample_xml_files["adr"])
        assert inst is not None

        meta = InstructionCardBuilder.build_card_metadata(inst)

        assert meta["xml_id"] == "ADR"
        assert meta["mnemonic"] == "ADR"
        assert meta["instr_class"] == "general"
        assert meta["encoding_count"] == 1
        assert meta["operand_count"] > 0

    def test_build_b_cond_card_with_value_table(self, sample_xml_files):
        """测试含值表的 Card."""
        inst = XMLInstructionParser.parse_file(sample_xml_files["b_cond"])
        assert inst is not None

        card = InstructionCardBuilder.build(inst)

        # 值表检查
        assert "EQ" in card
        assert "NE" in card
        assert "0000" in card
