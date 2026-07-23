"""ARM ISA Agent CLI."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from langchain_core.messages import AIMessage, HumanMessage

from arm_isa_agent.core.config import get_settings

app = typer.Typer(
    name="arm-isa",
    help="ARM ISA Copilot Agent — ETL, Search, Serve",
    no_args_is_help=True,
)
console = Console()

etl_app = typer.Typer(help="ETL pipeline commands")
app.add_typer(etl_app, name="etl")

rag_app = typer.Typer(help="RAG index & search commands")
app.add_typer(rag_app, name="rag")

agent_app = typer.Typer(help="AI Agent commands (LangGraph)")
app.add_typer(agent_app, name="agent")


# ── etl run ───────────────────────────────────────────────────

@etl_app.command("run")
def etl_run(
    xml_dir: str = typer.Option(
        "", "--xml-dir", "-x",
        help="ARM ISA XML directory path (default: auto-detect)",
    ),
    db_path: str = typer.Option(
        "", "--db-path", "-d",
        help="SQLite database path (default: data/sqlite/isa_kb.db)",
    ),
    truncate: bool = typer.Option(
        True, "--truncate/--no-truncate",
        help="Truncate existing data before import",
    ),
    no_cards: bool = typer.Option(
        False, "--no-cards",
        help="Skip Instruction Card (Markdown) generation",
    ),
    cards_dir: str = typer.Option(
        "", "--cards-dir",
        help="Output directory for Instruction Cards (default: data/cards)",
    ),
) -> None:
    """Run full ETL pipeline: parse XML → SQLite + Instruction Cards.

    By default, both SQLite database and Markdown Instruction Cards are generated.
    Use --no-cards to skip card generation.
    """
    from arm_isa_agent.etl.pipeline import ETLPipeline, Settings

    kwargs = {}
    if xml_dir:
        kwargs["raw_xml_dir"] = Path(xml_dir)
    if db_path:
        kwargs["sqlite_db_path"] = Path(db_path)

    settings = Settings(**kwargs) if kwargs else get_settings()
    pipeline = ETLPipeline(settings)

    out_cards_dir = Path(cards_dir) if cards_dir else None
    stats = pipeline.run_full(
        truncate=truncate,
        no_cards=no_cards,
        cards_dir=out_cards_dir,
    )

    # 汇总
    console.print(f"\n[bold green]Done![/] "
                  f"{stats.success} instructions, "
                  f"{stats.cards_generated} cards generated, "
                  f"{stats.failed} failed.")

    if stats.failed_files:
        console.print(f"\n[bold red]Failed files ({len(stats.failed_files)}):[/]")
        for fname, err in stats.failed_files:
            console.print(f"  [red]FAIL[/] {fname}: {err[:120]}")


# ── etl validate ──────────────────────────────────────────────

@etl_app.command("validate")
def etl_validate(
    xml_dir: str = typer.Option(
        "", "--xml-dir", "-x",
        help="ARM ISA XML directory path",
    ),
    limit: int = typer.Option(
        0, "--limit", "-n",
        help="Number of files to validate (0 = all)",
    ),
    show_detail: bool = typer.Option(
        False, "--detail", "-D",
        help="Show full error message for failed files",
    ),
) -> None:
    """Validate XML files (parse only, no DB write).

    Uses the same parser as 'etl run' to detect parsing issues early.
    """
    from arm_isa_agent.core.config import Settings
    from arm_isa_agent.etl.xml_parser import XMLInstructionParser
    from arm_isa_agent.core.constants import SHARED_PS_FILE

    kwargs = {}
    if xml_dir:
        kwargs["raw_xml_dir"] = Path(xml_dir)

    settings = Settings(**kwargs) if kwargs else get_settings()
    xml_path = settings.raw_xml_dir

    xml_files = sorted([
        f for f in xml_path.glob("*.xml")
        if f.name != SHARED_PS_FILE
    ])
    if limit > 0:
        xml_files = xml_files[:limit]

    console.print(f"[bold]Validating {len(xml_files)} XML files...[/]\n")

    ok_count = 0
    failed_count = 0
    failed_details: list[tuple[str, str]] = []

    for xml_file in xml_files:
        result = XMLInstructionParser.parse_file(xml_file)
        if result.ok:
            inst = result.instruction
            alias_mark = " [alias]" if inst.is_alias else ""
            console.print(
                f"  [green]OK[/] {xml_file.name}: "
                f"{inst.mnemonic} ({inst.instr_class}){alias_mark} "
                f"[dim]({len(inst.encodings)} encodings, {len(inst.operands)} operands)[/]"
            )
            ok_count += 1
        else:
            err_msg = result.error or "unknown"
            details = err_msg[:200] if show_detail else err_msg[:80]
            console.print(f"  [red]FAIL[/] {xml_file.name}: [red]{details}[/]")
            failed_count += 1
            failed_details.append((xml_file.name, err_msg))

    total = ok_count + failed_count
    rate = (ok_count / total * 100) if total > 0 else 0
    color = "green" if rate > 95 else ("yellow" if rate > 80 else "red")
    console.print(f"\n[bold {color}]{ok_count}/{total} passed ({rate:.1f}%)[/]")


# ── etl cards ─────────────────────────────────────────────────

@etl_app.command("cards")
def etl_cards(
    xml_dir: str = typer.Option("", "--xml-dir", "-x"),
    output_dir: str = typer.Option("data/cards", "--output", "-o"),
) -> None:
    """Generate Instruction Cards (Markdown) from XML, no DB write."""
    from arm_isa_agent.core.config import Settings
    from arm_isa_agent.etl.pipeline import ETLPipeline

    kwargs = {}
    if xml_dir:
        kwargs["raw_xml_dir"] = Path(xml_dir)

    settings = Settings(**kwargs) if kwargs else get_settings()
    pipeline = ETLPipeline(settings)

    stats = pipeline.run_full(
        truncate=False,
        no_cards=False,
        cards_dir=Path(output_dir),
    )
    console.print(f"[green]Generated {stats.cards_generated} cards → {output_dir}[/]")


# ── rag index ─────────────────────────────────────────────────

@rag_app.command("index")
def rag_index(
    cards_dir: str = typer.Option(
        "data/cards", "--cards-dir", "-c",
        help="Instruction Cards directory",
    ),
    force_rebuild: bool = typer.Option(
        False, "--force", "-f",
        help="Delete existing collection and rebuild from scratch",
    ),
    batch_size: int = typer.Option(
        32, "--batch-size", "-b",
        help="Embedding batch size",
    ),
) -> None:
    """Build RAG index: embed all Instruction Cards → ChromaDB + BM25.

    Requires: sentence-transformers with bge-m3 model (auto-download on first run).
    """
    from arm_isa_agent.core.config import Settings
    from arm_isa_agent.rag.pipeline import RAGPipeline

    settings = Settings(embedding_batch_size=batch_size)
    pipeline = RAGPipeline(settings)

    console.print("[bold]Initializing RAG pipeline...[/]")
    pipeline.initialize()

    console.print(
        f"[bold]Indexing cards from:[/] {cards_dir}"
        + (" [red](force rebuild)[/]" if force_rebuild else "")
    )

    count = pipeline.index_all_cards(
        cards_dir=Path(cards_dir),
        force_rebuild=force_rebuild,
    )

    console.print(f"\n[bold green]Done![/] {count} documents indexed.")
    console.print(f"  ChromaDB: {pipeline.chroma.persist_dir}")
    console.print(f"  Collection: {pipeline.chroma.collection_name}")


# ── rag search ─────────────────────────────────────────────────

@rag_app.command("search")
def rag_search(
    query: str = typer.Argument(..., help="Search query text"),
    top_k: int = typer.Option(5, "--top-k", "-k", help="Number of results"),
    instr_class: str = typer.Option(
        "", "--class", "-C",
        help="Filter by instruction class (general/fpsimd/advsimd/sve/...)",
    ),
    show_docs: bool = typer.Option(
        False, "--docs", "-d",
        help="Show full document text",
    ),
) -> None:
    """Hybrid search (BM25 + Vector) over Instruction Cards."""
    from arm_isa_agent.rag.pipeline import build_rag_pipeline

    console.print("[bold]Initializing RAG pipeline...[/]")
    pipeline = build_rag_pipeline()

    where_filter = None
    if instr_class:
        where_filter = {"instr_class": instr_class}

    console.print(f"[bold]Searching:[/] \"{query}\"\n")
    response = pipeline.search(query, top_k=top_k, where=where_filter)

    console.print(f"[dim]Candidates: {response.total_candidates} | "
                  f"Latency: {response.elapsed_ms:.1f}ms[/]\n")

    for i, r in enumerate(response.results, 1):
        mnemonic = r.metadata.get("mnemonic", "?")
        title = r.metadata.get("title", "")
        icls = r.metadata.get("instr_class", "")
        console.print(
            f"  [bold cyan]#{i}[/] [bold yellow]{mnemonic}[/] "
            f"({r.doc_id})"
        )
        console.print(
            f"     RRF={r.score:.4f}  "
            f"BM25={r.bm25_score:.4f}  Vec={r.vector_score:.4f}"
        )
        if icls:
            console.print(f"     Class: {icls}")
        if title:
            console.print(f"     {title}")
        if show_docs:
            console.print(f"     [dim]{r.document[:500]}...[/]")
        console.print("")

    if not response.results:
        console.print("[yellow]No results found.[/]")


# ── rag stats ─────────────────────────────────────────────────

@rag_app.command("stats")
def rag_stats() -> None:
    """Show RAG index statistics."""
    from arm_isa_agent.rag.pipeline import build_rag_pipeline

    console.print("[bold]Checking RAG index...[/]")
    pipeline = build_rag_pipeline()

    count = pipeline.chroma.count
    bm_count = pipeline.bm25.doc_count

    console.print(f"  ChromaDB documents: {count}")
    console.print(f"  BM25 documents:     {bm_count}")
    console.print(f"  Vector dim:         {pipeline.embedding.dim}")
    console.print(f"  Persist dir:        {pipeline.chroma.persist_dir}")


# ── agent ask ──────────────────────────────────────────────────

@agent_app.command("ask")
def agent_ask(
    query: str = typer.Argument(..., help="Question to ask the ARM ISA agent"),
    preset: str = typer.Option(
        "", "--preset", "-p",
        help="LLM preset: 'local' (Ollama Qwen3-8B) or 'deepseek' (DeepSeek API). "
             "Use --list-presets to see all options.",
    ),
    model: str = typer.Option(
        "", "--model", "-m",
        help="LLM model name (overrides preset, e.g., qwen3:8b, deepseek-chat)",
    ),
    api_key: str = typer.Option(
        "", "--api-key", "-k",
        help="OpenAI-compatible API key (overrides preset)",
    ),
    base_url: str = typer.Option(
        "", "--base-url", "-b",
        help="OpenAI-compatible base URL (overrides preset)",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Show intermediate tool-call results",
    ),
) -> None:
    """Ask the ARM ISA Agent a question (single query mode).

    The agent will automatically plan and execute tool calls to answer
    your question using the RAG pipeline and SQLite knowledge base.

    Examples:
        arm-isa agent ask --preset local "What does ADD shifted register do?"
        arm-isa agent ask --preset deepseek "Generate test case for STP" --verbose
        arm-isa agent ask -m qwen3:14b "Explain LDR encodings"
    """
    from arm_isa_agent.agent.graph import build_agent
    from arm_isa_agent.core.config import LLM_PRESETS, Settings
    from arm_isa_agent.kb.sqlite.client import SQLiteClient
    from arm_isa_agent.rag.pipeline import build_rag_pipeline

    # Build settings with overrides
    kwargs: dict[str, str] = {}
    if preset:
        kwargs["llm_preset"] = preset
    if model:
        kwargs["llm_model"] = model
    if api_key:
        kwargs["llm_api_key"] = api_key
    if base_url:
        kwargs["llm_base_url"] = base_url

    settings = Settings(**kwargs) if kwargs else get_settings()

    if not settings.llm_api_key and not settings.llm_base_url:
        presets_hint = (
            "Available presets:\n"
            f"  --preset local   → Ollama (Qwen3-8B) @ {LLM_PRESETS['local']['llm_base_url']}\n"
            f"  --preset deepseek → DeepSeek API @ {LLM_PRESETS['deepseek']['llm_base_url']}\n"
        )
        console.print(
            f"[bold red]Error:[/] No LLM configured.\n"
            f"Use --preset local for local dev, --preset deepseek for demo, "
            f"or configure via --model/--base-url/--api-key.\n\n"
            f"{presets_hint}"
        )
        raise typer.Exit(code=1)

    # Initialize knowledge bases
    console.print("[bold]Initializing knowledge bases...[/]")
    rag = build_rag_pipeline()
    sqlite = SQLiteClient(str(settings.sqlite_db_path))
    sqlite.initialize()

    # Build agent
    preset_tag = f" [preset: {settings.llm_preset}]" if settings.llm_preset else ""
    console.print(f"[bold]Initializing agent (model: {settings.llm_model}{preset_tag})...[/]\n")
    agent = build_agent(
        rag_pipeline=rag,
        sqlite_client=sqlite,
        settings=settings,
    )

    # Run
    console.print(f"[bold cyan]Query:[/] {query}\n")
    console.print("[dim]Agent is thinking...[/]\n")

    result = agent.run(query)

    # Print answer
    console.print(f"[bold green]Answer:[/]\n")
    console.print(result["answer"])
    console.print(f"\n[dim]({result['iterations']} iterations, {len(result['tool_results'])} tool calls)[/]")

    if verbose and result["tool_results"]:
        console.print("\n[bold]Tool Execution Details:[/]")
        for tr in result["tool_results"]:
            step = tr.get("step", "?")
            tool = tr.get("tool_name", "?")
            console.print(f"\n  [bold yellow]Step {step}: {tool}[/]")
            if "error" in tr:
                console.print(f"    [red]Error: {tr['error'][:200]}[/]")
            elif "result" in tr:
                raw = str(tr["result"])
                console.print(f"    [dim]{raw[:500]}[/]")


# ── agent chat ──────────────────────────────────────────────────

@agent_app.command("chat")
def agent_chat(
    preset: str = typer.Option(
        "", "--preset", "-p",
        help="LLM preset: 'local' (Ollama Qwen3-8B) or 'deepseek' (DeepSeek API)",
    ),
    model: str = typer.Option(
        "", "--model", "-m",
        help="LLM model name",
    ),
    api_key: str = typer.Option(
        "", "--api-key", "-k",
        help="OpenAI-compatible API key",
    ),
    base_url: str = typer.Option(
        "", "--base-url", "-b",
        help="OpenAI-compatible base URL",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Show intermediate tool-call results",
    ),
) -> None:
    """Start an interactive chat session with the ARM ISA Agent.

    Type 'exit' or 'quit' to end the session.
    Type 'verbose' to toggle tool-call details.

    Examples:
        arm-isa agent chat --preset local
        arm-isa agent chat --preset deepseek --verbose
    """
    from arm_isa_agent.agent.graph import build_agent
    from arm_isa_agent.core.config import LLM_PRESETS, Settings
    from arm_isa_agent.kb.sqlite.client import SQLiteClient
    from arm_isa_agent.rag.pipeline import build_rag_pipeline

    kwargs: dict[str, str] = {}
    if preset:
        kwargs["llm_preset"] = preset
    if model:
        kwargs["llm_model"] = model
    if api_key:
        kwargs["llm_api_key"] = api_key
    if base_url:
        kwargs["llm_base_url"] = base_url

    settings = Settings(**kwargs) if kwargs else get_settings()

    if not settings.llm_api_key and not settings.llm_base_url:
        presets_hint = (
            f"  --preset local   → Ollama @ {LLM_PRESETS['local']['llm_base_url']}\n"
            f"  --preset deepseek → DeepSeek API @ {LLM_PRESETS['deepseek']['llm_base_url']}\n"
        )
        console.print(
            f"[bold red]Error:[/] No LLM configured.\n"
            f"Use --preset local or --preset deepseek.\n\n{presets_hint}"
        )
        raise typer.Exit(code=1)

    # Initialize
    console.print("[bold]Initializing knowledge bases...[/]")
    rag = build_rag_pipeline()
    sqlite = SQLiteClient(str(settings.sqlite_db_path))
    sqlite.initialize()

    console.print("[bold]Initializing agent (model: {}{})...[/]".format(
        settings.llm_model,
        f" [preset: {settings.llm_preset}]" if settings.llm_preset else "",
    ))
    agent = build_agent(rag_pipeline=rag, sqlite_client=sqlite, settings=settings)

    console.print("\n[bold green]ARM ISA Agent Chat[/]")
    console.print("[dim]Type 'exit' to quit, 'verbose' to toggle tool details[/]\n")

    show_verbose = verbose
    chat_history: list = []

    while True:
        try:
            query = typer.prompt("You").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye![/]")
            break

        if query.lower() in ("exit", "quit"):
            console.print("[dim]Goodbye![/]")
            break

        if query.lower() == "verbose":
            show_verbose = not show_verbose
            console.print(f"[dim]Verbose mode: {'ON' if show_verbose else 'OFF'}[/]")
            continue

        if not query:
            continue

        console.print("[dim]Thinking...[/]")

        try:
            result = agent.run(query, chat_history=chat_history)
        except Exception as e:
            console.print(f"[bold red]Error:[/] {e}")
            continue

        console.print(f"\n[bold]Agent:[/] {result['answer']}\n")
        console.print(f"[dim]({result['iterations']} iterations, {len(result['tool_results'])} tools)[/]")

        if show_verbose and result["tool_results"]:
            for tr in result["tool_results"]:
                step = tr.get("step", "?")
                tool = tr.get("tool_name", "?")
                console.print(f"  [yellow]{step}. {tool}[/]")
                if "result" in tr:
                    raw = str(tr["result"])[:200]
                    console.print(f"     [dim]{raw}[/]")

        console.print("")

        # Update chat history
        chat_history.append(HumanMessage(content=query))
        chat_history.append(AIMessage(content=result["answer"]))


# ── agent tools ─────────────────────────────────────────────────

@agent_app.command("tools")
def agent_tools() -> None:
    """List all available agent tools and their descriptions."""
    # Trigger @register_tool side effects by importing the tools package
    import arm_isa_agent.tools  # noqa: F401
    from arm_isa_agent.agent.tool_registry import get_all_tools

    tools = get_all_tools()
    if not tools:
        console.print("[yellow]No tools registered.[/]")
        return

    console.print(f"[bold]Available Tools ({len(tools)}):[/]\n")
    for name, meta in tools.items():
        console.print(f"  [bold cyan]{name}[/]")
        console.print(f"    {meta['description']}")
        params = meta.get("parameters", {}).get("properties", {})
        if params:
            console.print("    [dim]Parameters:[/]")
            for pname, pinfo in params.items():
                req = "required" if pname in meta.get("parameters", {}).get("required", []) else "optional"
                console.print(f"      {pname}: {pinfo.get('type', 'string')} ({req})")
        console.print("")


# ── agent presets ───────────────────────────────────────────────

@agent_app.command("presets")
def agent_presets() -> None:
    """List available LLM presets."""
    from arm_isa_agent.core.config import LLM_PRESETS

    console.print("[bold]Available LLM Presets:[/]\n")
    for name, cfg in LLM_PRESETS.items():
        console.print(f"  [bold cyan]{name}[/]")
        console.print(f"    model:    {cfg['llm_model']}")
        console.print(f"    base_url: {cfg['llm_base_url']}")
        console.print(f"    provider: {cfg['llm_provider']}")
        if name == "local":
            console.print(f"    [dim](local dev — requires Ollama running on localhost:11434)[/]")
        elif name == "deepseek":
            console.print(f"    [dim](demo/production — requires DeepSeek API key)[/]")
        console.print("")


# ── serve ─────────────────────────────────────────────────────

@app.command("serve")
def serve(
    host: str = typer.Option("0.0.0.0", "--host"),
    port: int = typer.Option(8000, "--port"),
) -> None:
    """Start FastAPI server with SQLite + RAG + optional LLM auto-initialized."""
    import uvicorn

    from arm_isa_agent.api.app import create_app

    console.print(f"[bold green]Starting ARM ISA API server on {host}:{port}...[/]")
    app = create_app()
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    app()
