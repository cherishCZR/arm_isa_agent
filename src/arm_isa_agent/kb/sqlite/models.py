"""SQLAlchemy ORM 模型 —— 对应 SQLite 7 张核心表."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker


class Base(DeclarativeBase):
    pass


# ── 多对多关联表 ──────────────────────────────────────────────────

instruction_feature_association = Table(
    "instruction_features",
    Base.metadata,
    Column("instruction_id", Integer, ForeignKey("instructions.id", ondelete="CASCADE"), primary_key=True),
    Column("feature_id", Integer, ForeignKey("features.id", ondelete="CASCADE"), primary_key=True),
    Column("feature_level", String(32), default="iclass"),
)


# ── ORM 模型 ──────────────────────────────────────────────────────


class InstructionModel(Base):
    __tablename__ = "instructions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    xml_id: Mapped[str] = mapped_column(String(128), unique=True, index=True, comment="XML id")
    title: Mapped[str] = mapped_column(String(256), comment="完整标题")
    mnemonic: Mapped[str] = mapped_column(String(64), index=True, comment="助记符")
    instr_class: Mapped[str] = mapped_column(String(32), index=True, default="", comment="指令分类")
    instruction_type: Mapped[str] = mapped_column(String(32), default="instruction", comment="类型: instruction/alias/pseudocode")

    # 别名
    is_alias: Mapped[bool] = mapped_column(Boolean, default=False)
    alias_of: Mapped[str] = mapped_column(String(128), default="")
    alias_of_id: Mapped[str] = mapped_column(String(128), default="")

    # 描述
    brief: Mapped[str] = mapped_column(Text, default="")
    description: Mapped[str] = mapped_column(Text, default="")

    # 操作属性
    is_predicated: Mapped[bool] = mapped_column(Boolean, default=False)
    uses_dit: Mapped[bool] = mapped_column(Boolean, default=False)
    uses_dit_condition: Mapped[str] = mapped_column(String(256), default="")
    sm_policy: Mapped[str] = mapped_column(String(32), default="")

    # 编码图
    regdiagram_form: Mapped[str] = mapped_column(String(8), default="32")

    # 其他
    operational_notes: Mapped[str] = mapped_column(Text, default="")
    source_file: Mapped[str] = mapped_column(String(256), index=True, default="")

    # 文档元数据
    docvars_json: Mapped[str] = mapped_column(Text, default="{}", comment="JSON: docvar 键值对")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关系
    encodings: Mapped[list["EncodingModel"]] = relationship("EncodingModel", back_populates="instruction", cascade="all, delete-orphan")
    operands: Mapped[list["OperandModel"]] = relationship("OperandModel", back_populates="instruction", cascade="all, delete-orphan")
    pseudocode_list: Mapped[list["PseudocodeModel"]] = relationship("PseudocodeModel", back_populates="instruction", cascade="all, delete-orphan")
    constraints: Mapped[list["ConstraintModel"]] = relationship("ConstraintModel", back_populates="instruction", cascade="all, delete-orphan")
    features: Mapped[list["FeatureModel"]] = relationship("FeatureModel", secondary=instruction_feature_association, back_populates="instructions")
    classification: Mapped["InstructionClassificationModel | None"] = relationship(
        "InstructionClassificationModel", back_populates="instruction", cascade="all, delete-orphan", uselist=False,
    )
    facets: Mapped[list["InstructionFacetModel"]] = relationship(
        "InstructionFacetModel", back_populates="instruction", cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Instruction(id={self.id}, mnemonic='{self.mnemonic}')>"


class EncodingModel(Base):
    __tablename__ = "encodings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    instruction_id: Mapped[int] = mapped_column(Integer, ForeignKey("instructions.id", ondelete="CASCADE"), index=True)

    name: Mapped[str] = mapped_column(String(256), index=True, comment="编码名")
    label: Mapped[str] = mapped_column(String(64), default="")
    bitdiffs: Mapped[str] = mapped_column(Text, default="")
    assembly_template: Mapped[str] = mapped_column(Text, default="")
    assembly_template_raw: Mapped[str] = mapped_column(Text, default="")
    bitfields_json: Mapped[str] = mapped_column(Text, default="[]", comment="JSON: BitfieldValue 列表")
    docvars_json: Mapped[str] = mapped_column(Text, default="{}", comment="JSON: docvars")
    arch_variants_json: Mapped[str] = mapped_column(Text, default="[]", comment="JSON: ArchVariant 列表")
    equivalent_to: Mapped[str] = mapped_column(Text, default="")
    alias_condition: Mapped[str] = mapped_column(String(128), default="")
    operand_symbols_json: Mapped[str] = mapped_column(Text, default="[]", comment="JSON: 操作数符号列表")

    # 位模式 (计算得到，用于按位模式搜索)
    bit_pattern: Mapped[str] = mapped_column(String(64), default="", index=True, comment="32位位模式串 0/1/?")
    bit_pattern_mask: Mapped[str] = mapped_column(String(64), default="", comment="位模式掩码")

    instruction: Mapped["InstructionModel"] = relationship("InstructionModel", back_populates="encodings")

    def __repr__(self) -> str:
        return f"<Encoding(id={self.id}, name='{self.name}')>"


class OperandModel(Base):
    __tablename__ = "operands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    instruction_id: Mapped[int] = mapped_column(Integer, ForeignKey("instructions.id", ondelete="CASCADE"), index=True)

    symbol: Mapped[str] = mapped_column(String(128), comment="操作数符号")
    symbol_link: Mapped[str] = mapped_column(String(128), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    encoded_in: Mapped[str] = mapped_column(String(128), default="")
    operand_type: Mapped[str] = mapped_column(String(32), default="register")
    value_table_json: Mapped[str] = mapped_column(Text, default="[]", comment="JSON: 值表")
    encoding_name: Mapped[str] = mapped_column(String(128), default="", comment="所属 encoding 名 (enclist)")
    register_width: Mapped[int] = mapped_column(Integer, default=0, comment="寄存器位宽 (0=非寄存器/未知)")
    register_class: Mapped[str] = mapped_column(String(8), default="", comment="寄存器类 (W/X/B/H/S/D/Q/V/Z)")

    instruction: Mapped["InstructionModel"] = relationship("InstructionModel", back_populates="operands")

    def __repr__(self) -> str:
        return f"<Operand(id={self.id}, symbol='{self.symbol}')>"


class PseudocodeModel(Base):
    __tablename__ = "pseudocode"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    instruction_id: Mapped[int] = mapped_column(Integer, ForeignKey("instructions.id", ondelete="CASCADE"), index=True)

    name: Mapped[str] = mapped_column(String(256))
    section_type: Mapped[str] = mapped_column(String(32), index=True, comment="Decode/Execute/Operation/Library")
    body: Mapped[str] = mapped_column(Text, default="", comment="伪代码文本 (含交叉引用)")
    body_plain: Mapped[str] = mapped_column(Text, default="", comment="纯文本 (移除链接)")

    instruction: Mapped["InstructionModel"] = relationship("InstructionModel", back_populates="pseudocode_list")

    def __repr__(self) -> str:
        return f"<Pseudocode(id={self.id}, section='{self.section_type}')>"


class FeatureModel(Base):
    __tablename__ = "features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    feature_name: Mapped[str] = mapped_column(String(128), unique=True, index=True, comment="如 FEAT_FP")
    display_name: Mapped[str] = mapped_column(String(256), default="", comment="如 ARMv8.0")
    description: Mapped[str] = mapped_column(Text, default="")

    instructions: Mapped[list["InstructionModel"]] = relationship("InstructionModel", secondary=instruction_feature_association, back_populates="features")

    def __repr__(self) -> str:
        return f"<Feature(feature_name='{self.feature_name}')>"


class ConstraintModel(Base):
    __tablename__ = "constraints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    instruction_id: Mapped[int] = mapped_column(Integer, ForeignKey("instructions.id", ondelete="CASCADE"), index=True)

    constraint_type: Mapped[str] = mapped_column(String(64), default="", index=True)
    condition: Mapped[str] = mapped_column(Text, default="")
    description: Mapped[str] = mapped_column(Text, default="")

    # encoding 级别关联
    encoding_name: Mapped[str] = mapped_column(String(256), default="")
    source_section: Mapped[str] = mapped_column(String(128), default="")

    instruction: Mapped["InstructionModel"] = relationship("InstructionModel", back_populates="constraints")

    def __repr__(self) -> str:
        return f"<Constraint(id={self.id}, type='{self.constraint_type}')>"


class InstructionClassificationModel(Base):
    """One exhaustive primary taxonomy assignment per XML instruction variant."""

    __tablename__ = "instruction_variant_classifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    instruction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("instructions.id", ondelete="CASCADE"), unique=True, index=True,
    )
    primary_category: Mapped[str] = mapped_column(String(96), index=True)
    subcategory: Mapped[str] = mapped_column(String(96), index=True, default="general")
    classifier_source: Mapped[str] = mapped_column(String(32), default="xml_rule")
    taxonomy_version: Mapped[str] = mapped_column(String(32), default="arm-a64-2025-03")
    classified_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    instruction: Mapped["InstructionModel"] = relationship("InstructionModel", back_populates="classification")


class InstructionFacetModel(Base):
    """Non-exclusive filters attached to an XML instruction variant."""

    __tablename__ = "instruction_variant_facets"
    __table_args__ = (UniqueConstraint("instruction_id", "facet_type", "facet_value", name="uq_instruction_facet"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    instruction_id: Mapped[int] = mapped_column(Integer, ForeignKey("instructions.id", ondelete="CASCADE"), index=True)
    facet_type: Mapped[str] = mapped_column(String(48), index=True)
    facet_value: Mapped[str] = mapped_column(String(128), index=True)

    instruction: Mapped["InstructionModel"] = relationship("InstructionModel", back_populates="facets")


class SharedPseudocodeModel(Base):
    """共享伪代码函数存储（独立于单条指令）."""

    __tablename__ = "shared_pseudocode"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    function_name: Mapped[str] = mapped_column(String(256), index=True, comment="函数名 (如 UInt, SignExtend)")
    full_name: Mapped[str] = mapped_column(String(512), unique=True, index=True, comment="全限定名")
    signature: Mapped[str] = mapped_column(Text, default="")
    body: Mapped[str] = mapped_column(Text, default="")
    link_id: Mapped[str] = mapped_column(String(256), default="", comment="交叉引用链接 ID")
    section_type: Mapped[str] = mapped_column(String(32), default="Library")

    def __repr__(self) -> str:
        return f"<SharedPseudocode(function='{self.function_name}')>"


class InstructionIndexModel(Base):
    """指令索引表 (来自 index.xml / fpsimdindex.xml)."""

    __tablename__ = "instruction_index"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    index_id: Mapped[str] = mapped_column(String(128), index=True, comment="索引 ID (如 ABS, ADC)")
    heading: Mapped[str] = mapped_column(String(256), comment="标题 (如 ABS)")
    iformfile: Mapped[str] = mapped_column(String(256), comment="对应 XML 文件名 (如 abs.xml)")
    summary: Mapped[str] = mapped_column(Text, default="")
    index_type: Mapped[str] = mapped_column(String(32), default="base", comment="base | fpsimd")

    def __repr__(self) -> str:
        return f"<InstructionIndex(index_id='{self.index_id}')>"


# ── 数据库工厂函数 ─────────────────────────────────────────────────


def create_db_engine(db_path: str, echo: bool = False) -> tuple["Engine", "sessionmaker[Session]"]:
    """创建 SQLite 引擎和会话工厂."""
    engine = create_engine(
        f"sqlite:///{db_path}",
        echo=echo,
        connect_args={"check_same_thread": False, "timeout": 30},
        # 启用 WAL 模式以支持并发
        # poolclass=StaticPool,
    )
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return engine, SessionLocal


def init_db(engine: "Engine") -> None:
    """创建所有表."""
    Base.metadata.create_all(bind=engine)
    # 针对 SQLite 的特殊索引优化
    _create_custom_indexes(engine)


def _create_custom_indexes(engine: "Engine") -> None:
    """创建额外的性能索引."""
    from sqlalchemy import text

    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_encodings_instruction_id ON encodings(instruction_id);",
        "CREATE INDEX IF NOT EXISTS idx_operands_instruction_id ON operands(instruction_id);",
        "CREATE INDEX IF NOT EXISTS idx_pseudocode_instruction_id ON pseudocode(instruction_id);",
        "CREATE INDEX IF NOT EXISTS idx_constraints_instruction_id ON constraints(instruction_id);",
        "CREATE INDEX IF NOT EXISTS idx_instructions_mnemonic_class ON instructions(mnemonic, instr_class);",
        "CREATE INDEX IF NOT EXISTS idx_instructions_source_file ON instructions(source_file);",
        "CREATE INDEX IF NOT EXISTS idx_variant_classification_category ON instruction_variant_classifications(primary_category, subcategory);",
        "CREATE INDEX IF NOT EXISTS idx_variant_facets_type_value ON instruction_variant_facets(facet_type, facet_value);",
    ]

    with engine.connect() as conn:
        for idx_sql in indexes:
            conn.execute(text(idx_sql))
        conn.commit()
