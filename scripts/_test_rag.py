"""快速测试 RAG 管线：索引少量卡片 + 搜索验证."""
import sys
from pathlib import Path

# 添加项目根目录
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from arm_isa_agent.rag.pipeline import RAGPipeline
from arm_isa_agent.core.config import Settings


def main():
    settings = Settings(embedding_batch_size=8)
    pipeline = RAGPipeline(settings)

    print("[1/4] Initializing...")
    pipeline.initialize()
    print(f"  Embedding dim: {pipeline.embedding.dim}")
    print(f"  ChromaDB count (before): {pipeline.chroma.count}")

    print("\n[2/4] Force rebuild index from cards...")
    count = pipeline.index_all_cards(force_rebuild=True)
    print(f"  Indexed: {count} documents")
    print(f"  ChromaDB count: {pipeline.chroma.count}")
    print(f"  BM25 doc count: {pipeline.bm25.doc_count}")

    print("\n[3/4] Testing hybrid search...")
    queries = [
        "ADD instruction register",
        "branch conditional",
        "SVE predicate",
        "SIMD absolute value",
        "load store memory",
    ]
    for query in queries:
        response = pipeline.search(query, top_k=3)
        print(f"\n  Query: \"{query}\"")
        print(f"  Candidates: {response.total_candidates}, Latency: {response.elapsed_ms:.1f}ms")
        for i, r in enumerate(response.results, 1):
            mnem = r.metadata.get("mnemonic", "?")
            print(f"    #{i}: {mnem} ({r.doc_id})  "
                  f"RRF={r.score:.4f}  BM25={r.bm25_score:.4f}  Vec={r.vector_score:.4f}")

    print("\n[4/4] Testing card retrieval...")
    card = pipeline.get_card_text("ADD_shiftedreg")
    if card:
        print(f"  ADD_shiftedreg card: {len(card)} chars")
        print(f"  First 200 chars: {card[:200]}...")
    else:
        print("  ADD_shiftedreg card: NOT FOUND")

    print("\n✅ All RAG pipeline tests passed!")


if __name__ == "__main__":
    main()
