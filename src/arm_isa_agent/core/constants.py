from __future__ import annotations

from enum import Enum


class InstructionClass(str, Enum):
    """指令类别枚举，对应 XML docvar instr-class 的值."""

    GENERAL = "general"
    FPSIMD = "fpsimd"
    ADVSIMD = "advsimd"
    SVE = "sve"
    MORTLACH2 = "mortlach2"  # SME
    UNKNOWN = "unknown"


class OperandType(str, Enum):
    """操作数类型."""

    REGISTER = "register"
    IMMEDIATE = "immediate"
    LABEL = "label"
    MEMORY = "memory"
    CONDITION = "condition"
    SHIFT = "shift"
    OPTION = "option"
    ARRANGEMENT = "arrangement"
    VECTOR_ARRANGE = "vector_arrangement"
    REGISTER_LIST = "register_list"
    UNKNOWN = "unknown"


# ── 寄存器类 → 位宽映射 ────────────────────────────────────────────
# 用于从汇编模板中推断操作数的寄存器位宽。
#   通用寄存器: W=32-bit, X=64-bit (SP 由 WSP/SP 前缀区分)
#   SIMD&FP:    B=8, H=16, S=32, D=64, Q=128, V=128
#   SVE:        Z=128
REGISTER_CLASS_WIDTH: dict[str, int] = {
    "W": 32,
    "X": 64,
    "B": 8,
    "H": 16,
    "S": 32,
    "D": 64,
    "Q": 128,
    "V": 128,
    "Z": 128,
}


class EncodingForm(str, Enum):
    """编码位宽."""

    BIT32 = "32"
    BIT64 = "64"


class PseudocodeSection(str, Enum):
    """伪代码段类型."""

    DECODE = "Decode"
    EXECUTE = "Execute"
    OPERATION = "Operation"
    FUNCTIONS = "Functions"
    LIBRARY = "Library"
    NOHEADING = "noheading"


class FeatureLevel(str, Enum):
    """Feature 作用级别."""

    SECTION = "section"
    ICLASS = "iclass"
    ENCODING = "encoding"


class InstructionType(str, Enum):
    """指令文件类型."""

    INSTRUCTION = "instruction"
    ALIAS = "alias"
    PSEUDOCODE = "pseudocode"


ISA_XML_DIR = "ISA_A64_xml_A_profile-2025-03/ISA_A64_xml_A_profile-2025-03"
SHARED_PS_FILE = "shared_pseudocode.xml"
INDEX_FILE = "../index.xml"
FPSIMD_INDEX_FILE = "../fpsimdindex.xml"
