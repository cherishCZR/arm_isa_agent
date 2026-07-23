"""Hybrid Retriever — BM25 + Vector 混合检索 + RRF 融合排序.

Retrieval Pipeline:
    1. 查询 → EmbeddingService.encode_query()           → 向量
    2. 向量 → ChromaClient.query()                      → 语义 Top-K
    3. 查询 → BM25Retriever.search()                    → 关键词 Top-K
    4. RRF(Reciprocal Rank Fusion)融合两路结果          → 最终 Top-K

RRF 公式:
    RRF(d) = Σ_{r in ranks} 1 / (k + rank_r(d))
    k=60 (经典默认值)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import structlog

from arm_isa_agent.kb.chroma.client import ChromaClient
from arm_isa_agent.rag.bm25 import BM25Retriever
from arm_isa_agent.rag.embedding import EmbeddingService

logger = structlog.get_logger(__name__)


# ── 结果数据结构 ──────────────────────────────────────────────

@dataclass
class SearchResult:
    """单条检索结果。"""

    doc_id: str
    score: float                     # RRF 融合分数，0~1 之间
    document: str = ""               # 文档文本（Markdown Card）
    metadata: dict[str, Any] = field(default_factory=dict)
    bm25_score: float = 0.0
    vector_score: float = 0.0        # cosine distance → similarity (1 - distance)


@dataclass
class SearchResponse:
    """检索响应。"""

    query: str
    results: list[SearchResult]
    total_candidates: int = 0        # 两路候选总数
    elapsed_ms: float = 0.0


# ── Hybrid Retriever ──────────────────────────────────────────

class HybridRetriever:
    """BM25 + Vector 混合检索器。

    用法:
        retriever = HybridRetriever(chroma_client, bm25, embedding_service)
        results = retriever.search("What does the ADD instruction do?", top_k=5)
    """

    def __init__(
        self,
        chroma: ChromaClient,
        bm25: BM25Retriever,
        embedding: EmbeddingService,
        *,
        vector_weight: float = 0.6,
        bm25_weight: float = 0.4,
        rrf_k: int = 60,
        candidate_multiplier: int = 3,
    ) -> None:
        """
        Args:
            chroma: ChromaDB 客户端
            bm25: BM25 检索器
            embedding: Embedding 服务
            vector_weight: 向量检索在全融合中的权重
            bm25_weight: BM25 在全融合中的权重
            rrf_k: RRF 平滑参数
            candidate_multiplier: 每路检索 top_k × multiplier 的候选数
        """
        self.chroma = chroma
        self.bm25 = bm25
        self.embedding = embedding

        self.vector_weight = vector_weight
        self.bm25_weight = bm25_weight
        self.rrf_k = rrf_k
        self.candidate_multiplier = candidate_multiplier

    # ── 主查询入口 ─────────────────────────────────────────────

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
            where: ChromaDB 元数据过滤条件

        Returns:
            SearchResponse 包含排序结果列表
        """
        import time
        t0 = time.perf_counter()

        # 每路取 top_k × candidate_multiplier 候选，给融合更多余地
        candidate_k = top_k * self.candidate_multiplier

        # ── 1. 向量检索 ──
        query_emb = self.embedding.encode_query(query)
        chroma_result = self.chroma.query(query_emb, n_results=candidate_k, where=where)

        vector_hits: dict[str, tuple[str, float, str, dict]] = {}
        ids_flat = chroma_result.get("ids", [[]])[0]
        docs_flat = chroma_result.get("documents", [[]])[0]
        metas_flat = chroma_result.get("metadatas", [[]])[0]
        dists_flat = chroma_result.get("distances", [[]])[0]

        for i, doc_id in enumerate(ids_flat):
            dist = dists_flat[i] if i < len(dists_flat) else 1.0
            sim = max(0.0, 1.0 - dist)  # cosine distance → similarity
            vector_hits[doc_id] = (
                docs_flat[i] if i < len(docs_flat) else "",
                sim,
                metas_flat[i] if i < len(metas_flat) else {},
            )

        # ── 2. BM25 检索 ──
        bm25_hits: dict[str, tuple[str, float, dict]] = {}
        for doc_id, score, meta in self.bm25.search(query, k=candidate_k):
            bm25_hits[doc_id] = (doc_id, score, meta)

        # ── 3. RRF 融合 ──
        all_ids = set(vector_hits.keys()) | set(bm25_hits.keys())

        # 构建两路排名
        vec_ranked = sorted(
            [(vid, v[1]) for vid, v in vector_hits.items()],
            key=lambda x: x[1], reverse=True,
        )
        bm_ranked = sorted(
            [(bid, b[1]) for bid, b in bm25_hits.items()],
            key=lambda x: x[1], reverse=True,
        )

        vec_rank_map = {vid: i + 1 for i, (vid, _) in enumerate(vec_ranked)}
        bm_rank_map = {bid: i + 1 for i, (bid, _) in enumerate(bm_ranked)}

        # RRF 得分
        rrf_scores: dict[str, float] = {}
        for doc_id in all_ids:
            score = 0.0
            if doc_id in vec_rank_map:
                r = vec_rank_map[doc_id]
                score += self.vector_weight / (self.rrf_k + r)
            if doc_id in bm_rank_map:
                r = bm_rank_map[doc_id]
                score += self.bm25_weight / (self.rrf_k + r)
            rrf_scores[doc_id] = score

        # 归一化到 [0, 1]
        if rrf_scores:
            max_score = max(rrf_scores.values())
            for doc_id in rrf_scores:
                rrf_scores[doc_id] /= max_score

        # ── 4. 组装结果 ──
        sorted_ids = sorted(rrf_scores, key=rrf_scores.get, reverse=True)[:top_k]  # type: ignore[arg-type]

        results: list[SearchResult] = []
        for doc_id in sorted_ids:
            doc_text = ""
            meta = {}

            if doc_id in vector_hits:
                doc_text = vector_hits[doc_id][0]
                meta = vector_hits[doc_id][2]
            elif doc_id in bm25_hits:
                # BM25 侧没有文档原文，从 bm25 docs 中查找
                for d in self.bm25._docs:
                    if d.id == doc_id:
                        doc_text = " ".join(d.tokens)  # 回退用 token
                        meta = d.metadata
                        break

            # 尝试从 ChromaDB 获取完整文档（补全 BM25-only 结果）
            if not doc_text and doc_id in vector_hits:
                doc_text = vector_hits[doc_id][0]

            results.append(SearchResult(
                doc_id=doc_id,
                score=round(rrf_scores[doc_id], 4),
                document=doc_text,
                metadata=meta,
                bm25_score=round(bm25_hits.get(doc_id, ("", 0.0, {}))[1], 4),
                vector_score=round(vector_hits.get(doc_id, ("", 0.0, {}))[1], 4),
            ))

        elapsed = (time.perf_counter() - t0) * 1000
        logger.info(
            "hybrid.search",
            query=query[:80],
            top_k=top_k,
            candidates=len(all_ids),
            results=len(results),
            elapsed_ms=round(elapsed, 2),
        )

        return SearchResponse(
            query=query,
            results=results,
            total_candidates=len(all_ids),
            elapsed_ms=round(elapsed, 2),
        )
