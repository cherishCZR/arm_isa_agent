from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class BitfieldValue(BaseModel):
    """编码图单个位域的值."""

    name: str = Field(description="位域名 (如 sf, opc, Rd, imm19)")
    hibit: int = Field(description="最高位编号 (从 31 向下)")
    width: int = Field(default=1, description="位宽")
    values: list[str] = Field(default_factory=list, description="位值列表，空字符串表示可变位 (colspan)")
    is_fixed: bool = Field(default=False, description="是否固定值位域 (有 settings 属性)")
    fixed_count: int = Field(default=0, description="固定位数")
    psbits: str = Field(default="", description="伪代码中的覆盖值：x=不关心, xx=未设置")


class Encoding(BaseModel):
    """单条指令编码."""

    name: str = Field(description="编码名 (如 ADR_only_pcreladdr)")
    label: str = Field(default="", description="编码标签 (如 32-bit, 64-bit)")
    bitdiffs: str = Field(default="", description="位区分条件 (如 sf==0 && N==0)")
    assembly_template: str = Field(description="汇编模板文本 (纯文本 + 操作数占位符)")
    assembly_template_raw: str = Field(default="", description="汇编模板原始 XML 文本")
    docvars: dict[str, str] = Field(default_factory=dict, description="编码级别 docvars")
    bitfields: list[BitfieldValue] = Field(default_factory=list, description="编码级别位域覆盖值")
    arch_variants: list[ArchVariant] = Field(default_factory=list, description="架构变体")
    equivalent_to: str = Field(default="", description="别名等价的指令 (alias only)")
    alias_condition: str = Field(default="", description="别名条件 (如 Unconditionally)")
    operand_symbols: list[str] = Field(default_factory=list, description="汇编模板中出现的操作数符号")
    bit_pattern: str = Field(default="", description="32位位模式 (0/1/? 序列)")
    bit_pattern_mask: str = Field(default="", description="位模式掩码 (1=固定, 0=可变)")

    # -- iclass 级编码图（每个 iclass 的 regdiagram）--
    regdiagram_bitfields: list[BitfieldValue] = Field(
        default_factory=list, description="iclass 级编码图位域 (来自 regdiagram)"
    )
    regdiagram_form: str = Field(default="32", description="编码图位宽 (32|64)")
    iclass_name: str = Field(default="", description="所属 iclass 名 (如 Scalar/Vector)")


class Operand(BaseModel):
    """操作数定义."""

    symbol: str = Field(description="操作数符号 (如 <Xd>, <label>, <cond>)")
    symbol_link: str = Field(default="", description="符号链接 ID")
    description: str = Field(description="操作数文字描述")
    encoded_in: str = Field(default="", description="编码字段名 (如 Rd, immhi:immlo)")
    operand_type: str = Field(default="register", description="操作数类型推断")
    value_table: list[dict[str, str]] = Field(default_factory=list, description="值表 (如条件码表)")
    encoding_name: str = Field(default="", description="所属编码名 (enclist)")
    register_width: int = Field(default=0, description="寄存器位宽 (0=非寄存器/未知)")
    register_class: str = Field(default="", description="寄存器类字母 (W/X/B/H/S/D/Q/V/Z)")


class Pseudocode(BaseModel):
    """伪代码段."""

    name: str = Field(description="伪代码段名 (如 A64.dpimm.pcreladdr.ADR_only_pcreladdr)")
    section_type: str = Field(description="段类型: Decode / Execute / Operation / Library / Functions")
    body: str = Field(description="伪代码文本 (含内联交叉引用)")
    body_plain: str = Field(default="", description="伪代码纯文本 (去除链接标记)")


class SharedPseudocodeFunction(BaseModel):
    """共享伪代码函数."""

    name: str = Field(description="函数全限定名")
    signature: str = Field(default="", description="函数签名")
    body: str = Field(description="函数体纯文本")
    link_id: str = Field(default="", description="交叉引用链接 ID")


class ArchVariant(BaseModel):
    """架构特性变体."""

    feature: str = Field(description="Feature 名称 (如 FEAT_FP, FEAT_SME2)")
    name: str = Field(default="", description="人类可读版本名 (如 ARMv8.0, ARMv9.3)")


class DocVar(BaseModel):
    """文档元数据."""

    key: str
    value: str


class Constraint(BaseModel):
    """指令约束 (CONSTRAINED UNPREDICTABLE 等)."""

    constraint_type: str = Field(default="", description="约束类型: FEATURE_GATE | CONSTRAINED_UNPREDICTABLE | DECODE_FALLBACK")
    condition: str = Field(default="", description="约束条件表达式 (如 wback && n == t && n != 31)")
    description: str = Field(default="", description="约束文字描述 (如 Unpredictable_WBOVERLAPLD → WBSUPPRESS/UNKNOWN/UNDEF/NOP)")

    # -- encoding 关联字段 --
    encoding_name: str = Field(default="", description="适用的 encoding 名（空=所有 encoding）")
    source_section: str = Field(default="", description="约束来源: 伪代码段名")


class Instruction(BaseModel):
    """完整的 ARM 指令模型."""

    # -- 基本标识 --
    xml_id: str = Field(description="XML id 属性 (如 ADR, B_cond)")
    title: str = Field(description="指令标题 (如 ADR -- A64)")
    mnemonic: str = Field(default="", description="助记符 (来自 docvar mnemonic)")
    instruction_type: str = Field(default="instruction", description="文件类型: instruction | alias | pseudocode")

    # -- 别名信息 --
    is_alias: bool = Field(default=False)
    alias_of: str = Field(default="")  # aliasto refiform
    alias_of_id: str = Field(default="")  # aliasto iformid

    # -- 文档元数据 --
    docvars: dict[str, str] = Field(default_factory=dict)
    instr_class: str = Field(default="")

    # -- 描述信息 --
    brief: str = Field(default="", description="一句话摘要")
    description: str = Field(default="", description="详细描述文本")

    # -- 操作属性 --
    is_predicated: bool = Field(default=False)
    uses_dit: bool = Field(default=False)
    uses_dit_condition: str = Field(default="")
    sm_policy: str = Field(default="")

    # -- 编码信息 --
    encodings: list[Encoding] = Field(default_factory=list)

    # -- 编码图信息 (仅保留 form 用于数据库兼容；实际图在 Encoding 内) --
    regdiagram_form: str = Field(default="32", description="首个 iclass 的编码图位宽 (32|64)")

    # -- 操作数 --
    operands: list[Operand] = Field(default_factory=list)

    # -- 伪代码 --
    pseudocode_list: list[Pseudocode] = Field(default_factory=list)

    # -- 架构特性 --
    arch_variants: list[ArchVariant] = Field(default_factory=list)

    # -- 约束 --
    constraints: list[Constraint] = Field(default_factory=list)

    # -- Operational Notes --
    operational_notes: str = Field(default="")

    # -- 异常 --
    exceptions: list[str] = Field(default_factory=list)

    # -- 源文件 --
    source_file: str = Field(default="", description="来源 XML 文件名")
