"""ETL Pipeline 编排器。

单次遍历 XML → Pydantic 模型 → SQLite + Instruction Card (Markdown)。

职责：
    1. 扫描 XML 文件列表
    2. 调用 XMLInstructionParser 解析每个文件
    3. 写入 SQLite（结构化存储）
    4. 生成 Instruction Card（Markdown，用于 RAG）
    5. 输出统计与失败清单

用法:
    pipeline = ETLPipeline()
    stats = pipeline.run_full()          # 默认：SQLite + Card 都产出
    stats = pipeline.run_full(no_cards=True)  # 只写 SQLite
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import structlog
from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

from arm_isa_agent.core.config import Settings, get_settings
from arm_isa_agent.core.constants import SHARED_PS_FILE
from arm_isa_agent.core.models.instruction import Instruction
from arm_isa_agent.etl.instruction_card_builder import InstructionCardBuilder
from arm_isa_agent.etl.xml_parser import ParseResult, XMLInstructionParser
from arm_isa_agent.kb.sqlite.client import SQLiteClient

logger = structlog.get_logger(__name__)


# ── 统计容器 ──────────────────────────────────────────────────

@dataclass
class ETLStats:
    total_files: int = 0
    success: int = 0
    failed: int = 0
    instructions: int = 0
    aliases: int = 0
    cards_generated: int = 0
    shared_ps_functions: int = 0
    elapsed_seconds: float = 0.0
    failed_files: list[tuple[str, str]] = field(default_factory=list)  # (filename, error)


# ── Pipeline ──────────────────────────────────────────────────

class ETLPipeline:
    """ETL 管道编排器。

    单次遍历完成所有产出，避免重复解析。
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.db = SQLiteClient(str(self.settings.sqlite_db_path))
        self.console = Console()
        self.stats = ETLStats()

    # ── 主入口 ─────────────────────────────────────────────────

    def run_full(
        self,
        truncate: bool = True,
        no_cards: bool = False,
        cards_dir: Path | None = None,
    ) -> ETLStats:
        """运行完整 ETL 管道。

        Args:
            truncate: 是否清空已有数据库数据
            no_cards: 是否跳过 Instruction Card 生成
            cards_dir: Card 输出目录（默认 data/cards）

        Returns:
            ETLStats 统计对象
        """
        import time
        start_time = time.time()

        # 1. 确保数据目录
        self.settings.sqlite_db_path.parent.mkdir(parents=True, exist_ok=True)

        # 2. 初始化数据库
        self.db.initialize()
        if truncate:
            logger.info("etl.truncating")
            self.db.truncate_all()

        # 3. 解析共享伪代码
        self._process_shared_pseudocode()

        # 4. 扫描指令 XML 文件
        xml_files = self._collect_xml_files()

        # 5. 核心：单次遍历 → SQLite + Card
        self._process_instructions(xml_files, no_cards=no_cards, cards_dir=cards_dir)

        # 6. 解析指令索引
        self._process_index()

        from arm_isa_agent.kb.classification import InstructionClassificationService
        taxonomy_audit = InstructionClassificationService(self.db).rebuild()
        reports_dir = self.settings.data_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        (reports_dir / "classification_coverage.json").write_text(
            json.dumps(
                InstructionClassificationService(self.db).audit(self.settings.raw_xml_dir),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        logger.info("etl.classification_complete", **taxonomy_audit)

        self.stats.elapsed_seconds = round(time.time() - start_time, 2)

        # 7. 输出统计
        self._print_stats()

        return self.stats

    # ── 共享伪代码 ─────────────────────────────────────────────

    def _process_shared_pseudocode(self) -> None:
        ps_path = self.settings.raw_xml_dir / SHARED_PS_FILE
        if not ps_path.exists():
            logger.warning("etl.shared_ps_not_found", path=str(ps_path))
            return

        self.console.print(f"[bold]Parsing shared pseudocode:[/] {ps_path.name}")
        functions, errors = XMLInstructionParser.parse_shared_pseudocode(ps_path)
        self.stats.shared_ps_functions = len(functions)

        for func in functions:
            self.db.insert_shared_pseudocode({
                "function_name": func.name.split(".")[-1] if "." in func.name else func.name,
                "full_name": func.name,
                "signature": func.signature,
                "body": func.body,
                "link_id": func.link_id,
                "section_type": "Library",
            })

        if errors:
            logger.warning("etl.shared_ps_errors", count=len(errors))
            for err in errors[:5]:
                logger.warning("etl.shared_ps_error_detail", error=err)

        logger.info("etl.shared_ps_inserted", count=len(functions))

    # ── 指令文件收集 ───────────────────────────────────────────

    def _collect_xml_files(self) -> list[Path]:
        xml_dir = self.settings.raw_xml_dir
        if not xml_dir.exists():
            raise FileNotFoundError(f"XML directory not found: {xml_dir}")

        return sorted([
            f for f in xml_dir.glob("*.xml")
            if f.name != SHARED_PS_FILE
        ])

    # ── 指令处理（核心循环）────────────────────────────────────

    def _process_instructions(
        self,
        xml_files: list[Path],
        no_cards: bool = False,
        cards_dir: Path | None = None,
    ) -> None:
        """单次遍历：解析 → 写 SQLite → 生成 Card。"""
        self.stats.total_files = len(xml_files)

        cards_output_dir = cards_dir or (self.settings.data_dir / "cards")
        if not no_cards:
            cards_output_dir.mkdir(parents=True, exist_ok=True)

        self.console.print(
            f"[bold]Processing[/] {len(xml_files)} instruction XML files..."
        )

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=self.console,
        ) as progress:
            task = progress.add_task("ETL...", total=len(xml_files))

            for xml_file in xml_files:
                # ── 解析 ──
                result = XMLInstructionParser.parse_file(xml_file)

                if not result.ok:
                    self.stats.failed += 1
                    self.stats.failed_files.append(
                        (xml_file.name, result.error or "unknown")
                    )
                    progress.advance(task)
                    continue

                instruction = result.instruction
                if instruction is None:  # 类型收窄，安全守卫
                    self.stats.failed += 1
                    self.stats.failed_files.append((xml_file.name, "Parsed OK but instruction is None"))
                    progress.advance(task)
                    continue

                # ── 写入 SQLite ──
                try:
                    self._write_instruction_to_db(instruction)
                except Exception as e:
                    logger.error("etl.db_write_error", file=xml_file.name, error=str(e)[:200])
                    self.stats.failed += 1
                    self.stats.failed_files.append((xml_file.name, f"DB: {e}"))
                    progress.advance(task)
                    continue

                # ── 统计 ──
                if instruction.is_alias:
                    self.stats.aliases += 1
                else:
                    self.stats.instructions += 1
                self.stats.success += 1

                # ── 生成 Card ──
                if not no_cards:
                    try:
                        card_text = InstructionCardBuilder.build(instruction)
                        card_file = cards_output_dir / f"{instruction.xml_id}.md"
                        card_file.write_text(card_text, encoding="utf-8")
                        self.stats.cards_generated += 1
                    except Exception as e:
                        logger.error("etl.card_build_error", file=xml_file.name, error=str(e)[:200])

                progress.advance(task)

    # ── SQLite 写入 ────────────────────────────────────────────

    def _write_instruction_to_db(self, inst: Instruction) -> None:
        import json

        inst_id = self.db.insert_instruction({
            "xml_id": inst.xml_id,
            "title": inst.title,
            "mnemonic": inst.mnemonic,
            "instr_class": inst.instr_class,
            "instruction_type": inst.instruction_type,
            "is_alias": inst.is_alias,
            "alias_of": inst.alias_of,
            "alias_of_id": inst.alias_of_id,
            "brief": inst.brief,
            "description": inst.description,
            "is_predicated": inst.is_predicated,
            "uses_dit": inst.uses_dit,
            "uses_dit_condition": inst.uses_dit_condition,
            "sm_policy": inst.sm_policy,
            "regdiagram_form": inst.regdiagram_form,
            "operational_notes": inst.operational_notes,
            "source_file": inst.source_file,
            "docvars_json": json.dumps(inst.docvars, ensure_ascii=False),
        })

        # Encodings
        for enc in inst.encodings:
            self.db.insert_encoding({
                "instruction_id": inst_id,
                "name": enc.name,
                "label": enc.label,
                "bitdiffs": enc.bitdiffs,
                "assembly_template": enc.assembly_template,
                "assembly_template_raw": enc.assembly_template_raw,
                "bitfields_json": json.dumps(
                    [bf.model_dump() for bf in enc.bitfields], ensure_ascii=False,
                ),
                "docvars_json": json.dumps(enc.docvars, ensure_ascii=False),
                "arch_variants_json": json.dumps(
                    [av.model_dump() for av in enc.arch_variants], ensure_ascii=False,
                ),
                "equivalent_to": enc.equivalent_to,
                "alias_condition": enc.alias_condition,
                "operand_symbols_json": json.dumps(enc.operand_symbols, ensure_ascii=False),
                "bit_pattern": enc.bit_pattern,
                "bit_pattern_mask": enc.bit_pattern_mask,
            })

        # Operands
        for op in inst.operands:
            self.db.insert_operand({
                "instruction_id": inst_id,
                "symbol": op.symbol,
                "symbol_link": op.symbol_link,
                "description": op.description,
                "encoded_in": op.encoded_in,
                "operand_type": op.operand_type,
                "value_table_json": json.dumps(op.value_table, ensure_ascii=False),
                "encoding_name": op.encoding_name,
                "register_width": op.register_width,
                "register_class": op.register_class,
            })

        # Pseudocode
        for ps in inst.pseudocode_list:
            self.db.insert_pseudocode({
                "instruction_id": inst_id,
                "name": ps.name,
                "section_type": ps.section_type,
                "body": ps.body,
                "body_plain": ps.body_plain,
            })

        # Constraints
        for c in inst.constraints:
            self.db.insert_constraint({
                "instruction_id": inst_id,
                "constraint_type": c.constraint_type,
                "condition": c.condition,
                "description": c.description,
                "encoding_name": c.encoding_name,
                "source_section": c.source_section,
            })

        # Features (arch_variants)
        for av in inst.arch_variants:
            if av.feature:
                fid = self.db.get_or_create_feature(av.feature, av.name)
                self.db.link_instruction_feature(inst_id, fid, "iclass")

    # ── 索引处理 ───────────────────────────────────────────────

    def _process_index(self) -> None:
        from arm_isa_agent.core.constants import FPSIMD_INDEX_FILE, INDEX_FILE
        from lxml import etree as _etree

        index_files = [
            (INDEX_FILE, "base"),
            (FPSIMD_INDEX_FILE, "fpsimd"),
        ]

        for index_path_rel, index_type in index_files:
            # constants 中的路径带 "../" 前缀，而 raw_xml_dir.parent 已是
            # XML 目录的上层目录，故仅取文件名拼接，避免多退一层。
            index_path = (
                self.settings.raw_xml_dir.parent / Path(index_path_rel).name
            ).resolve()
            if not index_path.exists():
                logger.warning("etl.index_not_found", path=str(index_path))
                continue

            self.console.print(f"[bold]Parsing index:[/] {index_path.name}")
            try:
                parser = _etree.XMLParser(resolve_entities=False, no_network=True)
                tree = _etree.parse(str(index_path), parser)
                root = tree.getroot()
                count = 0
                for iforms in root.findall("iforms"):
                    for iform in iforms.findall("iform"):
                        self.db.insert_index_entry({
                            "index_id": iform.get("id", ""),
                            "heading": iform.get("heading", ""),
                            "iformfile": iform.get("iformfile", ""),
                            "summary": (iform.text or "").strip(),
                            "index_type": index_type,
                        })
                        count += 1
                logger.info("etl.index_inserted", file=index_path.name, count=count)
            except Exception as e:
                logger.error("etl.index_parse_error", file=index_path.name, error=str(e)[:200])

    # ── 统计输出 ───────────────────────────────────────────────

    def _print_stats(self) -> None:
        db_stats = self.db.get_stats()

        self.console.print("\n[bold cyan]=== ETL Pipeline Complete ===[/]")
        self.console.print(f"  Total XML files:         {self.stats.total_files}")
        self.console.print(f"  [green]Success:[/]                 {self.stats.success}")
        self.console.print(f"  [red]Failed:[/]                  {self.stats.failed}")
        self.console.print(f"  Instructions:            {self.stats.instructions}")
        self.console.print(f"  Aliases:                 {self.stats.aliases}")
        self.console.print(f"  Cards generated:         {self.stats.cards_generated}")
        self.console.print(f"  Shared Psuedocode fns:   {self.stats.shared_ps_functions}")
        self.console.print(f"  Elapsed:                 {self.stats.elapsed_seconds}s")

        if self.stats.failed_files:
            self.console.print(f"\n[bold red]  Failed files ({len(self.stats.failed_files)}):[/]")
            for fname, err in self.stats.failed_files:
                self.console.print(f"    [red]FAIL[/] {fname}: {err[:100]}")

        self.console.print(f"\n[bold cyan]  Database Stats:[/]")
        for key, value in db_stats.items():
            self.console.print(f"    {key}: {value}")
        self.console.print(f"    db_path: {self.settings.sqlite_db_path}")

        # 汇总成功率
        if self.stats.total_files > 0:
            rate = self.stats.success / self.stats.total_files * 100
            color = "green" if rate > 95 else ("yellow" if rate > 80 else "red")
            self.console.print(f"\n  [bold {color}]Success rate: {rate:.1f}%[/]")


# ── 便捷函数 ──────────────────────────────────────────────────

def run_etl(
    xml_dir: str | None = None,
    db_path: str | None = None,
    truncate: bool = True,
    no_cards: bool = False,
) -> ETLStats:
    """便捷函数：一行运行 ETL。

    Args:
        xml_dir: XML 目录（覆盖配置）
        db_path: SQLite 路径（覆盖配置）
        truncate: 是否清空已有数据
        no_cards: 是否跳过 Card 生成

    Returns:
        ETLStats
    """
    kwargs = {}
    if xml_dir:
        kwargs["raw_xml_dir"] = Path(xml_dir)
    if db_path:
        kwargs["sqlite_db_path"] = Path(db_path)

    settings = Settings(**kwargs) if kwargs else get_settings()
    pipeline = ETLPipeline(settings)
    return pipeline.run_full(truncate=truncate, no_cards=no_cards)
