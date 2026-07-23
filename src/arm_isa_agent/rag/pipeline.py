"""RAG Pipeline — 索引 Instruction Card + 检索查询.

核心流程:
    1. 索引: Card Markdown → EmbeddingService.encode_documents() → ChromaDB + BM25
    2. 查询: 用户问题 → HybridRetriever.search() → Top-K Instruction Cards

Usage:
    pipeline = RAGPipeline()
    pipeline.initialize()
    pipeline.index_all_cards()        # 首次/重建索引
    results = pipeline.search("ADD 指令怎么用？", top_k=5)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import structlog

from arm_isa_agent.core.config import Settings, get_settings
from arm_isa_agent.etl.instruction_card_builder import InstructionCardBuilder
from arm_isa_agent.kb.chroma.client import ChromaClient
from arm_isa_agent.rag.bm25 import BM25Retriever
from arm_isa_agent.rag.embedding import EmbeddingService
from arm_isa_agent.rag.retriever import HybridRetriever, SearchResponse

logger = structlog.get_logger(__name__)


class RAGPipeline:
    """RAG 管线：索引管理 + 检索入口。

    Usage:
        pipeline = RAGPipeline()
        pipeline.initialize()
        pipeline.index_all_cards()
        results = pipeline.search("What does ADC do?")
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._chroma: ChromaClient | None = None
        self._embedding: EmbeddingService | None = None
        self._bm25: BM25Retriever | None = None
        self._retriever: HybridRetriever | None = None

    # ── 生命周期 ──────────────────────────────────────────────

    def initialize(self) -> None:
        """初始化 ChromaDB + Embedding + BM25 + Retriever。

        BM25 索引优先从磁盘缓存加载；若缓存缺失或与 ChromaDB 不一致，
        则自动从 ChromaDB 重建并写回缓存。
        """
        logger.info("rag.initializing")

        self._chroma = ChromaClient(self._settings)
        self._chroma.initialize()

        self._embedding = EmbeddingService(self._settings)

        # 注册到 ChromaClient，使查询时能用同一模型编码
        self._chroma.set_embedding_fn(self._embedding.encode_queries)

        self._bm25 = BM25Retriever()

        self._retriever = HybridRetriever(
            chroma=self._chroma,
            bm25=self._bm25,
            embedding=self._embedding,
        )

        # 尝试从缓存加载 BM25；缓存缺失或过期则从 ChromaDB 重建
        self._load_bm25_cache()

        logger.info("rag.initialized", dim=self._embedding.dim)

    @property
    def is_initialized(self) -> bool:
        return self._chroma is not None and self._retriever is not None

    @property
    def retriever(self) -> HybridRetriever:
        if self._retriever is None:
            raise RuntimeError("RAGPipeline not initialized. Call initialize() first.")
        return self._retriever

    @property
    def chroma(self) -> ChromaClient:
        if self._chroma is None:
            raise RuntimeError("RAGPipeline not initialized. Call initialize() first.")
        return self._chroma

    @property
    def embedding(self) -> EmbeddingService:
        if self._embedding is None:
            raise RuntimeError("RAGPipeline not initialized. Call initialize() first.")
        return self._embedding

    @property
    def bm25(self) -> BM25Retriever:
        if self._bm25 is None:
            raise RuntimeError("RAGPipeline not initialized. Call initialize() first.")
        return self._bm25

    @property
    def _bm25_cache_path(self) -> Path:
        """BM25 缓存文件路径。"""
        return self._settings.bm25_cache_dir / "index.pkl"

    # ── BM25 缓存加载 ──────────────────────────────────────────

    def _load_bm25_cache(self) -> None:
        """加载 BM25 缓存。

        策略：
        1. 缓存文件存在且 doc_count 与 ChromaDB 一致 → 直接加载（毫秒级）
        2. 缓存缺失/过期/损坏 → 从 ChromaDB 重建 → 写回缓存
        """
        if self._bm25 is None:
            return

        cache_path = self._bm25_cache_path
        chroma_count = self._chroma.count if self._chroma else 0

        if cache_path.exists() and chroma_count > 0:
            try:
                self._bm25.load(cache_path)
                if self._bm25.doc_count == chroma_count:
                    logger.info(
                        "rag.bm25_cache_hit",
                        doc_count=self._bm25.doc_count,
                    )
                    return
                else:
                    logger.info(
                        "rag.bm25_cache_stale",
                        cached=self._bm25.doc_count,
                        current=chroma_count,
                    )
                    self._bm25.clear()
            except Exception as e:
                logger.warning("rag.bm25_cache_load_failed", error=str(e)[:100])
                self._bm25.clear()

        # 缓存不可用，从 ChromaDB 重建（_rebuild 内部自动持久化）
        self._rebuild_bm25_from_chroma()

    def _persist_bm25_cache(self) -> None:
        """将当前 BM25 状态持久化到磁盘。"""
        if self._bm25 is None or not self._bm25.is_indexed:
            return
        try:
            self._bm25.save(self._bm25_cache_path)
            logger.debug("rag.bm25_saved", path=str(self._bm25_cache_path))
        except Exception as e:
            logger.warning("rag.bm25_save_failed", error=str(e)[:100])

    # ── 索引 ───────────────────────────────────────────────────

    def index_all_cards(
        self,
        cards_dir: Path | None = None,
        force_rebuild: bool = False,
    ) -> int:
        """索引所有 Instruction Card Markdown 文件。

        Args:
            cards_dir: Card 目录（默认 data/cards）
            force_rebuild: 是否删除旧集合后重建

        Returns:
            索引的文档数
        """
        if not self.is_initialized:
            self.initialize()

        assert self._chroma is not None
        assert self._embedding is not None
        assert self._bm25 is not None

        cards_path = cards_dir or (self._settings.data_dir / "cards")
        if not cards_path.exists():
            raise FileNotFoundError(f"Cards directory not found: {cards_path}")

        if force_rebuild and self._chroma.collection_exists():
            logger.info("rag.rebuild_deleting_old")
            self._chroma.delete_collection()
            self._chroma.initialize()
            self._bm25.clear()

        # 若已索引则跳过
        existing_count = self._chroma.count
        if existing_count > 0 and not force_rebuild:
            logger.info("rag.skip_index", existing_count=existing_count)
            # 但仍需重建 BM25
            if not self._bm25.is_indexed:
                self._rebuild_bm25_from_chroma()
            return existing_count

        # 收集 Card 文件
        card_files = sorted(cards_path.glob("*.md"))
        if not card_files:
            logger.warning("rag.no_cards_found", path=str(cards_path))
            return 0

        logger.info("rag.indexing_cards", total=len(card_files))

        # 批量读取 + 编码 + 入库
        batch_size = self._settings.embedding_batch_size
        total = 0

        for i in range(0, len(card_files), batch_size):
            batch_files = card_files[i : i + batch_size]
            ids, docs, metas = self._read_card_batch(batch_files)

            if not ids:
                continue

            # 编码
            embeddings = self._embedding.encode_documents(docs)

            # 写入 ChromaDB
            self._chroma.add_documents(ids, docs, embeddings, metas)
            total += len(ids)

            # 进度
            if (i + batch_size) % (batch_size * 5) == 0 or (i + batch_size) >= len(card_files):
                logger.info(
                    "rag.index_progress",
                    done=min(i + batch_size, len(card_files)),
                    total=len(card_files),
                )

        # 构建 BM25 索引
        self._rebuild_bm25_from_chroma()

        logger.info("rag.index_complete", count=total)
        return total

    def _read_card_batch(
        self,
        card_files: list[Path],
    ) -> tuple[list[str], list[str], list[dict[str, Any]]]:
        """读取一批 Card 文件，返回 (ids, documents, metadatas)。"""
        ids: list[str] = []
        docs: list[str] = []
        metas: list[dict[str, Any]] = []

        for f in card_files:
            try:
                text = f.read_text(encoding="utf-8")
                if not text.strip():
                    continue

                doc_id = f.stem  # xml_id

                # 从 Card 前几行提取元数据
                meta = self._extract_card_meta(text, doc_id)

                ids.append(doc_id)
                docs.append(text)
                metas.append(meta)
            except Exception as e:
                logger.warning("rag.read_card_error", file=f.name, error=str(e)[:100])

        return ids, docs, metas

    @staticmethod
    def _extract_card_meta(text: str, xml_id: str) -> dict[str, Any]:
        """从 Card Markdown 文本中提取元数据。"""
        meta: dict[str, Any] = {
            "xml_id": xml_id,
            "mnemonic": "",
            "instr_class": "",
            "title": "",
        }

        lines = text.split("\n")
        for line in lines[:20]:
            line = line.strip()

            # 标题行: ## MNEMONIC
            if line.startswith("## ") and not meta["mnemonic"]:
                mnem = line[3:].strip()
                if "`" in mnem:
                    mnem = mnem.split("`")[1]
                if "[" in mnem:
                    mnem = mnem.split("[")[0].strip()
                meta["mnemonic"] = mnem
                continue

            # Meta 行: **Title**: ... | **Class**: ... | **XML ID**: ...
            if line.startswith("**Title**:"):
                parts = line.split("|")
                for part in parts:
                    part = part.strip()
                    if part.startswith("**Title**:"):
                        meta["title"] = part.split(":", 1)[1].strip()
                    elif part.startswith("**Class**:"):
                        cls_val = part.split(":", 1)[1].strip().strip("`")
                        meta["instr_class"] = cls_val

        return meta

    def _rebuild_bm25_from_chroma(self) -> None:
        """从 ChromaDB 已有数据重建 BM25 索引，并持久化到磁盘。"""
        if self._chroma is None or self._bm25 is None:
            return
        if self._chroma.count == 0:
            return

        logger.info("rag.building_bm25")
        # 获取 ChromaDB 中所有文档
        result = self._chroma.collection.get(
            include=["documents", "metadatas"],
        )
        ids = result.get("ids", [])
        docs = result.get("documents", [])
        metas = result.get("metadatas", [])

        bm_docs: list[dict] = []
        for i in range(len(ids)):
            bm_docs.append({
                "id": ids[i],
                "text": docs[i] if i < len(docs) else "",
                "metadata": metas[i] if i < len(metas) else {},
            })

        self._bm25.index(bm_docs)
        logger.info("rag.bm25_ready", doc_count=self._bm25.doc_count)

        # 持久化到磁盘
        self._persist_bm25_cache()

    # ── 跨文档获取 ──────────────────────────────────────────────

    def get_card_text(self, xml_id: str) -> str | None:
        """从 ChromaDB 获取指定指令的完整 Card 文本。

        Args:
            xml_id: 指令 XML ID

        Returns:
            Card Markdown 文本，不存在则返回 None
        """
        if self._chroma is None or self._chroma.count == 0:
            return None

        try:
            result = self._chroma.collection.get(
                ids=[xml_id],
                include=["documents"],
            )
            docs = result.get("documents", [])
            if docs and docs[0]:
                return docs[0]
        except Exception:
            pass
        return None

    # ── 查询 ───────────────────────────────────────────────────

    def search(
        self,
        query: str,
        top_k: int = 5,
        *,
        where: dict[str, Any] | None = None,
    ) -> SearchResponse:
        """执行混合检索。

        Args:
            query: 用户查询文本
            top_k: 返回 Top-K 结果
            where: ChromaDB 元数据过滤条件（如 {"instr_class": "general"}）

        Returns:
            SearchResponse 包含排序结果列表
        """
        if not self.is_initialized:
            self.initialize()

        assert self._retriever is not None
        return self._retriever.search(query, top_k=top_k, where=where)


# ── 便捷函数 ──────────────────────────────────────────────────

def build_rag_pipeline() -> RAGPipeline:
    """快速构建并初始化 RAG 管线。"""
    pipeline = RAGPipeline()
    pipeline.initialize()
    return pipeline
