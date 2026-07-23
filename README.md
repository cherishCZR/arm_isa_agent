# ARM ISA Copilot Agent

AI-powered **Compiler Verification Agent** for ARM A64 instruction set architecture. Combines LLM reasoning, RAG retrieval, and automated test generation to produce verifiable compiler test suites.

---

## Architecture

```
                           ┌─────────────────────────────────────┐
                           │            User / API               │
                           └──────────────┬──────────────────────┘
                                          │
                           ┌──────────────▼──────────────────────┐
                           │         Planner Agent               │
                           │  (Intent classification + plan)     │
                           └──────────────┬──────────────────────┘
                                          │
              ┌───────────────────────────┼───────────────────────────┐
              │                           │                           │
    ┌─────────▼─────────┐    ┌───────────▼───────────┐    ┌──────────▼──────────┐
    │ Instruction       │    │  Constraint Analyzer  │    │  Test Planning      │
    │ Retrieval (RAG)   │    │  (immediates/feat/    │    │  (dimensions/       │
    │ BM25 + Vector     │    │   CONSTRAINED_UNPRED) │    │   priority matrix)  │
    └─────────┬─────────┘    └───────────┬───────────┘    └──────────┬──────────┘
              │                           │                           │
              └───────────────────────────┼───────────────────────────┘
                                          │
                              ┌───────────▼───────────┐
                              │  Testcase Generator   │
                              │  8 formats: ASM, LLVM,│
                              │  C++, boundary, alias, │
                              │  invalid, feature      │
                              └───────────┬───────────┘
                                          │
                              ┌───────────▼───────────┐
                              │  Testcase Reviewer    │
                              │  5 dimensions: syntax,│
                              │  constraint, encoding,│
                              │  semantic, coverage   │
                              └───────────┬───────────┘
                                          │
                              ╔═══════════▼═══════════╗
                              ║   Self-Correction     ║
                              ║   Loop (max 3)        ║
                              ║   Repair → Re-Review  ║
                              ╚═══════════╤═══════════╝
                                          │
                              ┌───────────▼───────────┐
                              │  Verification Report  │
                              │  (JSON / Markdown)    │
                              └───────────────────────┘
```

### Data Flow

```
ARM XML Spec → ETL Pipeline → Dual KB (SQLite + ChromaDB)
                                    ↓
User Query → RAG Retrieval → Instruction Profile → Constraint Analysis
                                    ↓
                              Test Plan (dimensions + strategy)
                                    ↓
                              Test Generator (8 formats)
                                    ↓
                              Test Reviewer (5 dimensions)
                                    ↓
                     ┌──────── Self-Correction Loop (3x max) ────────┐
                     │  Repair Generator → Re-Review → Decision      │
                     └───────────────────────────────────────────────┘
                                    ↓
                            Verification Report
```

---

## Key Capabilities

### AI Agent Workflow
- **LangGraph-based** multi-node agent with Planner → Executor → Reviewer → Repair loop
- LLM-powered intent classification and tool-call planning
- Safety limits: max 15 executor iterations, 3 repair attempts per test

### RAG (Retrieval-Augmented Generation)
- **Dual Knowledge Base**: SQLite (structured metadata) + ChromaDB (semantic search)
- **Hybrid Retrieval**: BM25 + Vector embeddings fused with RRF (Reciprocal Rank Fusion)
- Embeddings via BAAI/bge-m3 (1024-dim)

### Compiler Verification
- **Full Pipeline**: Retrieval → Constraint Analysis → Planning → Generation → Review → Repair → Report
- **8 Test Formats**: ARM assembly, LLVM MC CHECK, GCC inline asm, C++ verification, boundary, alias, invalid operand, feature enable
- **5-Dimension Review**: syntax, constraint, encoding, semantic, coverage

### Self-Reflection
- Auto-detect test quality issues across 5 dimensions
- Auto-repair with LLM assistance (max 3 iterations per test)
- Structured feedback: issue type, severity, location, fix suggestion

### Automatic Test Generation
- Rule-based (fast, deterministic) + LLM-assisted (higher quality)
- Coverage: normal operations, boundary values, register constraints, encoding variants, CONSTRAINED UNPREDICTABLE, feature dependencies

---

## Project Structure

```
src/arm_isa_agent/
├── verification/         # Compiler Verification Pipeline (NEW)
│   ├── models.py         #   VerificationReport, CoverageBreakdown
│   └── orchestrator.py   #   Full pipeline orchestrator
├── agent/                # LangGraph Agent Runtime
│   ├── graph.py          #   StateGraph with self-correction loop
│   ├── state.py          #   AgentState (TypedDict)
│   ├── tool_registry.py  #   @register_tool decorator
│   └── prompt_manager.py #   System prompts
├── generation/           # Test Generation Logic
│   ├── models.py         #   10 Pydantic models (8 test types)
│   ├── generators.py     #   8 generators + suite orchestrator
│   └── prompts.py        #   Generation prompts
├── planning/             # Test Planning Logic
│   ├── models.py         #   InstructionProfile, TestStrategy
│   ├── planner.py        #   InstructionPlanner (LLM-assisted)
│   ├── analyzer.py       #   InstructionAnalyzer (rule-based)
│   └── prompts.py        #   Planning prompts
├── review_generation/    # Review & Self-Correction
│   ├── models.py         #   ReviewResult, ReviewIssue, RepairResult
│   ├── reviewer.py       #   5 dimension reviewers + orchestrator
│   └── prompts.py        #   Review prompts
├── rag/                  # RAG Retrieval Pipeline
│   ├── pipeline.py       #   RAGPipeline orchestrator
│   ├── retriever.py      #   HybridRetriever (BM25 + Vector)
│   ├── bm25.py           #   BM25 keyword indexing
│   └── embedding.py      #   BGE-M3 embedding service
├── tools/                # 22 Registered Agent Tools
│   ├── retrieval.py      #   retrieve_instruction, query_*
│   ├── generation.py     #   generate_*, validate_operand
│   ├── planning.py       #   plan_instruction_tests
│   ├── testgen.py        #   generate_test_suite + 7 specific generators
│   ├── review_gen.py     #   review_testcase, repair_testcase
│   └── review.py         #   review_result
├── api/                  # FastAPI REST API
│   ├── app.py            #   App factory
│   ├── deps.py           #   Dependency injection
│   ├── schemas.py        #   Request/Response models
│   └── routes/
│       └── verification.py  # POST /api/generate_testcase
├── kb/                   # Dual Knowledge Base
│   ├── sqlite/           #   SQLite (structured ORM)
│   └── chroma/           #   ChromaDB (vector search)
├── etl/                  # ETL Pipeline (XML → KB)
├── core/                 # Config, constants, exceptions
└── cli/                  # CLI (arm-isa)
```

---

## Quick Start

```bash
# Install
pip install -e ".[dev]"

# Build knowledge base from ARM XML spec
arm-isa etl run

# Start API server (with verification endpoint)
uvicorn arm_isa_agent.api.app:create_app --factory --port 8000

# Or use CLI
arm-isa serve
```

---

## API Reference

### `POST /api/generate_testcase`

Run the full Compiler Verification pipeline for one instruction.

**Request:**
```json
{
  "instruction": "ADD",
  "use_llm": false
}
```

**Response:**
```json
{
  "instruction": "ADD",
  "status": "PASS",
  "generated_tests": 20,
  "coverage": {
    "normal": 100,
    "boundary": 100,
    "encoding": 100,
    "alias": 100,
    "invalid": 100,
    "feature": 100,
    "overall": 100
  },
  "review_score": 96,
  "review_passed": true,
  "repair_attempts": 0,
  "repair_successful": false,
  "total_duration_ms": 1234,
  "stage_results": [...],
  "issues": [],
  "suggestions": [],
  "generated_at": "2026-01-01T00:00:00Z"
}
```

### `POST /api/generate_testcases`

Batch verification for multiple instructions.

**Request:**
```json
{
  "instructions": ["ADD", "SUB", "LDR"],
  "use_llm": false
}
```

### `GET /api/health`

Health check.

---

## Agent Usage

```python
from arm_isa_agent import build_agent

# Create agent with services
agent = build_agent(rag_pipeline=rag, sqlite_client=sqlite)

# Retrieve instruction info
result = agent.run("What registers does ADD use?")

# Generate and verify tests
result = agent.run("Generate tests for ADD and review quality")
# Returns: answer, tool_results, review_results, verification_report

# Use verification directly
from arm_isa_agent.verification import run_verification

report = run_verification("ADD", sqlite_client=sqlite, llm=llm)
print(report.to_markdown())
```

---

## Configuration

Environment variables (prefix `ARM_ISA_`):

| Variable | Default | Description |
|----------|---------|-------------|
| `ARM_ISA_LLM_MODEL` | `gpt-4o` | LLM model name |
| `ARM_ISA_LLM_API_KEY` | — | API key for LLM provider |
| `ARM_ISA_LLM_BASE_URL` | — | Custom API base URL |
| `ARM_ISA_LLM_PRESET` | — | `local` (Ollama) or `deepseek` |
| `ARM_ISA_EMBEDDING_MODEL_NAME` | `BAAI/bge-m3` | Embedding model |
| `ARM_ISA_API_PORT` | `8000` | API server port |
