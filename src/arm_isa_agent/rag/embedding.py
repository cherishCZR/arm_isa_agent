"""bge-m3 Embedding 服务 — 封装 sentence-transformers，提供文档/查询编码.

bge-m3 (BAAI/bge-m3):
  - 维度: 1024
  - 需添加 instruction prefix 以获得最佳效果
  - 查询前缀: "Represent this sentence for searching relevant passages: "
  - 文档前缀: 无（空字符串）

单例模式，避免重复加载模型。
"""

from __future__ import annotations

import threading
from typing import Sequence

import structlog

from arm_isa_agent.core.config import Settings, get_settings

logger = structlog.get_logger(__name__)

# bge-m3 查询指令前缀
_QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "

_model_lock = threading.Lock()
_model: "SentenceTransformer | None" = None  # type: ignore[name-defined]


def _load_model(settings: Settings) -> "SentenceTransformer":  # type: ignore[name-defined]
    """懒加载 bge-m3 模型（线程安全）。"""
    global _model
    if _model is not None:
        return _model

    with _model_lock:
        if _model is not None:
            return _model

        from sentence_transformers import SentenceTransformer

        logger.info(
            "embedding.loading_model",
            model=settings.embedding_model_name,
            device=settings.embedding_device,
        )
        _model = SentenceTransformer(
            settings.embedding_model_name,
            device=settings.embedding_device,
        )
        # 如果 model card 中有 instruction 字段则设置（bge-m3 需要）
        if hasattr(_model, "_model_card_vars") and _model._model_card_vars:
            # bge-m3 使用 {"query_instruction": "..."} 这类配置
            pass  # bge-m3 通过 encode 参数控制，见下文
        logger.info("embedding.model_loaded", model=settings.embedding_model_name)
        return _model


class EmbeddingService:
    """bge-m3 嵌入服务。

    文档编码: encode_documents(texts)   → 无前缀
    查询编码: encode_queries(queries)   → 加查询指令前缀

    Usage:
        svc = EmbeddingService()
        emb = svc.encode_documents(["ADD adds two register values..."])
        query_emb = svc.encode_queries(["How does ADD work?"])
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._model: "SentenceTransformer | None" = None  # type: ignore[name-defined]

    @property
    def model(self) -> "SentenceTransformer":  # type: ignore[name-defined]
        if self._model is None:
            self._model = _load_model(self._settings)
        return self._model

    @property
    def dim(self) -> int:
        """向量维度（bge-m3 = 1024）。"""
        return self.model.get_sentence_embedding_dimension()

    @property
    def batch_size(self) -> int:
        return self._settings.embedding_batch_size

    def encode_documents(self, texts: Sequence[str]) -> list[list[float]]:
        """编码文档文本（不带查询指令前缀）。

        Args:
            texts: 文档文本列表

        Returns:
            向量列表，每个向量 1024 维 float
        """
        if not texts:
            return []
        embeddings = self.model.encode(
            list(texts),
            batch_size=self.batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return embeddings.tolist()

    def encode_queries(self, queries: Sequence[str]) -> list[list[float]]:
        """编码查询文本（带 bge-m3 查询指令前缀）。

        Args:
            queries: 查询文本列表

        Returns:
            向量列表，每个向量 1024 维 float
        """
        if not queries:
            return []
        prefixed = [_QUERY_INSTRUCTION + q for q in queries]
        embeddings = self.model.encode(
            prefixed,
            batch_size=self.batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return embeddings.tolist()

    def encode_documents_batch(
        self,
        texts: Sequence[str],
        batch_size: int | None = None,
    ) -> list[list[float]]:
        """批量编码文档，分批显示进度。

        Args:
            texts: 文档文本列表
            batch_size: 每批大小（默认 Settings.embedding_batch_size）

        Returns:
            向量列表
        """
        bs = batch_size or self.batch_size
        all_embeddings: list[list[float]] = []

        for i in range(0, len(texts), bs):
            batch = texts[i : i + bs]
            embeddings = self.model.encode(
                list(batch),
                batch_size=bs,
                show_progress_bar=False,
                normalize_embeddings=True,
            )
            all_embeddings.extend(embeddings.tolist())

            if (i + bs) % (bs * 10) == 0 or (i + bs) >= len(texts):
                logger.debug(
                    "embedding.batch_progress",
                    done=min(i + bs, len(texts)),
                    total=len(texts),
                )

        return all_embeddings

    # ── 便捷方法 ───────────────────────────────────────────────

    def encode_query(self, query: str) -> list[float]:
        """编码单个查询。"""
        return self.encode_queries([query])[0]
