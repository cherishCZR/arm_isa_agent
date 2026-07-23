"""SQLite 客户端 —— 连接管理和基础操作."""

from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Generator, Optional

import structlog
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session

from arm_isa_agent.kb.sqlite.models import (
    Base,
    ConstraintModel,
    EncodingModel,
    FeatureModel,
    InstructionIndexModel,
    InstructionModel,
    OperandModel,
    PseudocodeModel,
    SharedPseudocodeModel,
    create_db_engine,
    init_db,
)

logger = structlog.get_logger(__name__)


class SQLiteClient:
    """SQLite 数据库客户端."""

    def __init__(self, db_path: str, echo: bool = False) -> None:
        self.db_path = db_path
        self.engine: Optional[Engine] = None
        self._echo = echo

    def initialize(self) -> None:
        """初始化数据库连接并创建表."""
        self.engine, self.SessionLocal = create_db_engine(self.db_path, echo=self._echo)
        init_db(self.engine)
        logger.info("sqlite.initialized", db_path=self.db_path)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """获取数据库会话上下文管理器."""
        if self.engine is None:
            raise RuntimeError("SQLiteClient not initialized. Call initialize() first.")
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def truncate_all(self) -> None:
        """清空并重建所有表 (支持 schema 变更)."""
        with self.session() as session:
            session.execute(text("PRAGMA foreign_keys = OFF"))
            session.commit()
        Base.metadata.drop_all(bind=self.engine)
        # init_db 会同时 create_all 和建自定义索引
        init_db(self.engine)
        logger.info("sqlite.truncated_and_recreated")

    def insert_instruction(self, inst_data: dict) -> int:
        """插入一条指令记录，返回自增 ID."""
        with self.session() as session:
            inst = InstructionModel(**inst_data)
            session.add(inst)
            session.flush()
            inst_id = inst.id
        return inst_id

    def insert_encoding(self, enc_data: dict) -> int:
        with self.session() as session:
            enc = EncodingModel(**enc_data)
            session.add(enc)
            session.flush()
            return enc.id

    def insert_operand(self, op_data: dict) -> int:
        with self.session() as session:
            op = OperandModel(**op_data)
            session.add(op)
            session.flush()
            return op.id

    def insert_pseudocode(self, ps_data: dict) -> int:
        with self.session() as session:
            ps = PseudocodeModel(**ps_data)
            session.add(ps)
            session.flush()
            return ps.id

    def insert_constraint(self, c_data: dict) -> int:
        with self.session() as session:
            c = ConstraintModel(**c_data)
            session.add(c)
            session.flush()
            return c.id

    def get_or_create_feature(self, feature_name: str, display_name: str = "") -> int:
        """获取或创建 feature 记录，返回 ID."""
        with self.session() as session:
            feat = session.query(FeatureModel).filter_by(feature_name=feature_name).first()
            if feat is None:
                feat = FeatureModel(feature_name=feature_name, display_name=display_name)
                session.add(feat)
                session.flush()
            return feat.id

    def link_instruction_feature(self, instruction_id: int, feature_id: int, level: str = "iclass") -> None:
        """关联指令和 feature."""
        from sqlalchemy import text

        with self.session() as session:
            session.execute(
                text(
                    "INSERT OR IGNORE INTO instruction_features (instruction_id, feature_id, feature_level) "
                    "VALUES (:iid, :fid, :level)"
                ),
                {"iid": instruction_id, "fid": feature_id, "level": level},
            )

    def insert_index_entry(self, idx_data: dict) -> None:
        with self.session() as session:
            idx = InstructionIndexModel(**idx_data)
            session.add(idx)

    def insert_shared_pseudocode(self, sp_data: dict) -> int:
        with self.session() as session:
            sp = SharedPseudocodeModel(**sp_data)
            session.add(sp)
            session.flush()
            return sp.id

    def get_stats(self) -> dict:
        """获取数据库统计信息."""
        with self.session() as session:
            from sqlalchemy import func as sqlfunc

            return {
                "instructions": session.query(sqlfunc.count(InstructionModel.id)).scalar(),
                "encodings": session.query(sqlfunc.count(EncodingModel.id)).scalar(),
                "operands": session.query(sqlfunc.count(OperandModel.id)).scalar(),
                "pseudocode": session.query(sqlfunc.count(PseudocodeModel.id)).scalar(),
                "constraints": session.query(sqlfunc.count(ConstraintModel.id)).scalar(),
                "features": session.query(sqlfunc.count(FeatureModel.id)).scalar(),
                "shared_pseudocode": session.query(sqlfunc.count(SharedPseudocodeModel.id)).scalar(),
                "instruction_index": session.query(sqlfunc.count(InstructionIndexModel.id)).scalar(),
            }
