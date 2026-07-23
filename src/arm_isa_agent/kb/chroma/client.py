"""ChromaDB 客户端 — 连接管理、集合创建、文档索引与检索."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb
import structlog
from chromadb.api import ClientAPI
from chromadb.api.types import EmbeddingFunction
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions

from arm_isa_agent.core.config import Settings as AppSettings
from arm_isa_agent.core.config import get_settings

logger = structlog.get_logger(__name__)


class ExternalEmbeddingFunction(EmbeddingFunction):
    """接受外部传入的向量列表，绕过 ChromaDB 内置 embedding。"""

    def __init__(self, embedding_fn: Any = None) -> None:
        self._embedding_fn = embedding_fn
        self._cache: dict[str, list[float]] = {}

    def set_embeddings(self, id_to_embedding: dict[str, list[float]]) -> None:
        """预置文档 ID → 向量映射，query 时由 embedding_fn 动态生成。"""
        self._cache = id_to_embedding

    def __call__(self, texts: list[str]) -> list[list[float]]:
        # 查询时走外部 embedding 函数
        if self._embedding_fn is not None:
            return self._embedding_fn(texts)  # type: ignore[call-arg]
        return [[0.0]] * len(texts)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if self._embedding_fn is not None:
            return self._embedding_fn(texts)
        return [[0.0]] * len(texts)

    def embed_query(self, text: str) -> list[float]:
        if self._embedding_fn is not None:
            result = self._embedding_fn([text])
            return result[0] if result else [0.0]
        return [0.0]


class ChromaClient:
    """ChromaDB 向量知识库客户端。

    封装了 ChromaDB 持久化连接、集合管理、及基础的文档增删查。

    Usage:
        client = ChromaClient()
        client.initialize()
        client.add_documents(ids, documents, embeddings, metadatas)
        results = client.query(query_embedding, n_results=5)
    """

    def __init__(
        self,
        settings: AppSettings | None = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._client: ClientAPI | None = None
        self._collection: Any = None
        self._ef: ExternalEmbeddingFunction | None = None

    @property
    def persist_dir(self) -> Path:
        return self._settings.chroma_persist_dir

    @property
    def collection_name(self) -> str:
        return self._settings.chroma_collection_name

    # ── 生命周期 ───────────────────────────────────────────────

    def initialize(self) -> None:
        """初始化 ChromaDB 持久化客户端和集合。"""
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        self._client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=ChromaSettings(anonymized_telemetry=False),
        )

        self._ef = ExternalEmbeddingFunction()
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self._ef,
            metadata={"hnsw:space": "cosine"},
        )

        count = self._collection.count()
        logger.info(
            "chroma.initialized",
            collection=self.collection_name,
            path=str(self.persist_dir),
            document_count=count,
        )

    def close(self) -> None:
        """关闭客户端（ChromaDB PersistentClient 无显式 close，仅清理引用）。"""
        self._collection = None
        self._client = None
        self._ef = None

    @property
    def client(self) -> ClientAPI:
        if self._client is None:
            raise RuntimeError("ChromaClient not initialized. Call initialize() first.")
        return self._client

    @property
    def collection(self) -> Any:
        if self._collection is None:
            raise RuntimeError("ChromaClient not initialized. Call initialize() first.")
        return self._collection

    @property
    def count(self) -> int:
        """集合中文档数量。"""
        if self._collection is None:
            return 0
        return self._collection.count()

    def set_embedding_fn(self, fn: Any) -> None:
        """注入外部 embedding 函数（用于查询时动态编码）。"""
        if self._ef is not None:
            self._ef._embedding_fn = fn

    # ── 文档管理 ───────────────────────────────────────────────

    def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]] | None = None,
    ) -> None:
        """批量添加文档及其向量到集合。

        Args:
            ids: 文档唯一标识列表（如 xml_id）
            documents: 文档文本列表
            embeddings: 对应的向量列表
            metadatas: 可选元数据列表
        """
        if self.collection is None:
            raise RuntimeError("ChromaClient not initialized.")

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas or [{}] * len(ids),
        )
        logger.info("chroma.added", count=len(ids))

    def add_documents_batch(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]] | None = None,
        batch_size: int = 100,
    ) -> int:
        """分批添加文档，避免单次提交过大。

        Returns:
            实际添加的文档总数。
        """
        total = 0
        meta_list = metadatas or [{}] * len(ids)
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i : i + batch_size]
            batch_docs = documents[i : i + batch_size]
            batch_embs = embeddings[i : i + batch_size]
            batch_meta = meta_list[i : i + batch_size]
            self.add_documents(batch_ids, batch_docs, batch_embs, batch_meta)
            total += len(batch_ids)
        return total

    def delete_by_ids(self, ids: list[str]) -> None:
        """按 ID 删除文档。"""
        if self.collection is None:
            return
        self.collection.delete(ids=ids)
        logger.info("chroma.deleted", count=len(ids))

    def delete_collection(self) -> None:
        """删除整个集合（谨慎使用）。"""
        if self._client is None:
            return
        try:
            self._client.delete_collection(self.collection_name)
            self._collection = None
            logger.info("chroma.collection_deleted", name=self.collection_name)
        except Exception:
            pass

    # ── 查询 ───────────────────────────────────────────────────

    def query(
        self,
        query_embedding: list[float],
        n_results: int = 5,
        where: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """向量相似度查询。

        Args:
            query_embedding: 查询向量
            n_results: 返回结果数
            where: ChromaDB 过滤条件

        Returns:
            ChromaDB 原生查询结果（ids, documents, metadatas, distances）
        """
        if self.collection is None:
            return {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

    # ── 检查 ───────────────────────────────────────────────────

    def collection_exists(self) -> bool:
        """检查集合是否已存在且非空。"""
        return self._collection is not None and self._collection.count() > 0
