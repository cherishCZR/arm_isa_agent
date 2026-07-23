"""BM25 稀疏检索器 — 纯 Python 实现，支持索引构建与关键词搜索.

BM25 公式:
    score(q, d) = Σ IDF(q_i) · [f(q_i,d) · (k1+1)] / [f(q_i,d) + k1·(1 - b + b·|d|/avgdl)]

默认参数: k1=1.5, b=0.75

此模块与 ChromaDB 向量检索配合使用，构成 Hybrid Search。
"""

from __future__ import annotations

import math
import pickle
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


# ── 中文/英文分词 ──────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    """简单分词：提取字母数字序列，统一小写。

    对 ARM ISA 文本，保留编码字段名（如 tszh, sf, imm3）和特征名（如 FEAT_SVE）等。
    """
    return re.findall(r"[A-Za-z0-9_]+", text.lower())


# ── 数据结构 ──────────────────────────────────────────────────

@dataclass
class BM25Doc:
    """BM25 索引中的文档。"""

    id: str
    tokens: list[str]
    metadata: dict = field(default_factory=dict)


# ── BM25 索引 ─────────────────────────────────────────────────

class BM25Retriever:
    """BM25 关键词检索器。

    用法:
        bm25 = BM25Retriever()
        bm25.index(documents)           # 构建索引
        results = bm25.search(query, k=10)  # 检索
    """

    def __init__(
        self,
        k1: float = 1.5,
        b: float = 0.75,
        epsilon: float = 0.25,
    ) -> None:
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon

        # 索引状态
        self._docs: list[BM25Doc] = []
        self._doc_count: int = 0
        self._avgdl: float = 0.0
        self._df: dict[str, int] = defaultdict(int)  # term → document frequency
        self._idf: dict[str, float] = {}              # term → IDF
        self._term_freqs: list[dict[str, int]] = []   # per-document term frequencies
        self._doc_lengths: list[int] = []              # per-document token counts

    @property
    def doc_count(self) -> int:
        return self._doc_count

    @property
    def is_indexed(self) -> bool:
        return self._doc_count > 0

    # ── 索引构建 ───────────────────────────────────────────────

    def index(self, documents: list[dict]) -> None:
        """构建/重建 BM25 索引。

        Args:
            documents: 文档列表，每个文档为 {id, text [, metadata]}
        """
        self._docs = []
        self._df.clear()
        self._term_freqs.clear()
        self._doc_lengths.clear()

        total_length = 0

        for doc in documents:
            doc_id = doc["id"]
            text = doc.get("text", "")
            metadata = doc.get("metadata", {})
            tokens = _tokenize(text)

            # 文档内词频
            tf: dict[str, int] = defaultdict(int)
            for t in tokens:
                tf[t] += 1

            self._docs.append(BM25Doc(id=doc_id, tokens=tokens, metadata=metadata))
            self._term_freqs.append(dict(tf))
            self._doc_lengths.append(len(tokens))
            total_length += len(tokens)

            # 文档频率
            for t in set(tokens):
                self._df[t] += 1

        self._doc_count = len(self._docs)
        self._avgdl = total_length / max(self._doc_count, 1)

        # 预计算 IDF
        self._compute_idf()

    def _compute_idf(self) -> None:
        """计算所有词的 IDF。"""
        self._idf.clear()
        for term, df in self._df.items():
            idf = math.log(
                (self._doc_count - df + 0.5) / (df + 0.5) + 1.0
            )
            self._idf[term] = idf

    # ── 搜索 ───────────────────────────────────────────────────

    def search(
        self,
        query: str,
        k: int = 10,
    ) -> list[tuple[str, float, dict]]:
        """BM25 关键词搜索。

        Args:
            query: 查询文本
            k: 返回 Top-K 结果

        Returns:
            [(doc_id, score, metadata), ...]  按 score 降序排列
        """
        if not self.is_indexed:
            return []

        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        scores: list[float] = [0.0] * self._doc_count

        for token in set(query_tokens):
            if token not in self._idf:
                continue
            idf = self._idf[token]

            for i, tf_dict in enumerate(self._term_freqs):
                f = tf_dict.get(token, 0)
                if f == 0:
                    continue
                doc_len = self._doc_lengths[i]
                numerator = f * (self.k1 + 1.0)
                denominator = f + self.k1 * (
                    1.0 - self.b + self.b * doc_len / max(self._avgdl, 1.0)
                )
                scores[i] += idf * numerator / (denominator + self.epsilon)

        # 排序取 top-k
        indexed_scores = [
            (self._docs[i].id, scores[i], self._docs[i].metadata)
            for i in range(self._doc_count)
            if scores[i] > 0
        ]
        indexed_scores.sort(key=lambda x: x[1], reverse=True)
        return indexed_scores[:k]

    def search_batch(
        self,
        queries: list[str],
        k: int = 10,
    ) -> list[list[tuple[str, float, dict]]]:
        """批量检索。"""
        return [self.search(q, k) for q in queries]

    # ── 持久化 ─────────────────────────────────────────────────

    def save(self, path: Path) -> None:
        """将 BM25 索引状态持久化到磁盘。

        Args:
            path: 缓存文件路径（如 data/bm25/index.pkl）
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        state: dict = {
            "docs": self._docs,
            "doc_count": self._doc_count,
            "avgdl": self._avgdl,
            "df": dict(self._df),
            "idf": self._idf,
            "term_freqs": self._term_freqs,
            "doc_lengths": self._doc_lengths,
        }
        with open(path, "wb") as f:
            pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, path: Path) -> None:
        """从磁盘恢复 BM25 索引状态。

        Args:
            path: 缓存文件路径

        Raises:
            FileNotFoundError: 缓存文件不存在
        """
        with open(path, "rb") as f:
            state = pickle.load(f)

        self._docs = state["docs"]
        self._doc_count = state["doc_count"]
        self._avgdl = state["avgdl"]
        self._df = defaultdict(int, state["df"])
        self._idf = state["idf"]
        self._term_freqs = state["term_freqs"]
        self._doc_lengths = state["doc_lengths"]

    # ── 维护 ───────────────────────────────────────────────────

    def clear(self) -> None:
        """清空索引。"""
        self._docs.clear()
        self._df.clear()
        self._idf.clear()
        self._term_freqs.clear()
        self._doc_lengths.clear()
        self._doc_count = 0
        self._avgdl = 0.0
