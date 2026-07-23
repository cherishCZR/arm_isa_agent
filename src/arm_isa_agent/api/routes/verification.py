"""Verification API routes — sync + SSE stream + download endpoints."""

from __future__ import annotations

import io
import zipfile
from typing import Any

import structlog
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from arm_isa_agent.api.deps import get_llm, get_sqlite
from arm_isa_agent.api.schemas import (
    BatchDownloadRequest,
    BatchGenerateRequest,
    BatchGenerateResponse,
    BatchStreamRequest,
    DownloadFileRequest,
    GenerateTestcaseRequest,
    GenerateTestcaseResponse,
    HealthResponse,
    ParseScenarioFileRequest,
    ScenarioBatchStreamRequest,
    StreamVerificationRequest,
)
from arm_isa_agent.verification.orchestrator import VerificationOrchestrator

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api", tags=["verification"])


# ── Health Check ─────────────────────────────────────────────────

@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """API health check."""
    return HealthResponse()


# ── Single Instruction Verification (Sync) ───────────────────────

@router.post("/generate_testcase", response_model=GenerateTestcaseResponse)
async def generate_testcase(request: GenerateTestcaseRequest) -> GenerateTestcaseResponse:
    """Run the full Compiler Verification pipeline for a single ARM instruction.

    Pipeline stages:
        1. Instruction Retrieval (profile loading from KB)
        2. Constraint Analysis (immediates, registers, features, UNPREDICTABLE)
        3. Test Planning (dimensions, priorities, coverage matrix)
        4. Test Generation (ARM asm, LLVM MC, inline asm, boundary, alias, invalid, feature)
        5. Test Review (syntax, constraint, encoding, semantic, coverage — 5 dimensions)
        6. Repair Loop (max 3 iterations, auto-fix detected issues)
        7. Verification Report (coverage, score, issues, suggestions, test_files)
    """
    instruction = request.instruction.strip()
    if not instruction:
        raise HTTPException(status_code=400, detail="instruction field is required")

    logger.info("api.generate_testcase", instruction=instruction, use_llm=request.use_llm)

    try:
        sqlite = get_sqlite()
        llm = get_llm() if request.use_llm else None

        orchestrator = VerificationOrchestrator(
            sqlite_client=sqlite,
            llm=llm,
            use_llm_planning=request.use_llm,
            use_llm_review=request.use_llm,
        )

        report = orchestrator.verify(instruction, use_llm=request.use_llm, instruction_count=request.instruction_count, target_instruction_count=request.target_instruction_count)

        return GenerateTestcaseResponse(
            instruction=report.instruction,
            status=report.status,
            generated_tests=report.generated_tests,
            passing_test_count=report.passing_test_count,
            failing_test_count=report.failing_test_count,
            coverage={
                "normal": report.coverage.normal,
                "boundary": report.coverage.boundary,
                "encoding": report.coverage.encoding,
                "alias": report.coverage.alias,
                "invalid": report.coverage.invalid,
                "feature": report.coverage.feature,
                "overall": report.coverage.overall,
            },
            review_score=report.review_score,
            review_passed=report.review_passed,
            repair_attempts=report.repair_attempts,
            repair_successful=report.repair_successful,
            total_duration_ms=report.total_duration_ms,
            stage_results=[sr.model_dump() for sr in report.stage_results],
            stage_details=[sd.model_dump() for sd in report.stage_details],
            test_files=[tf.model_dump() for tf in report.test_files],
            issues=report.issues,
            suggestions=report.suggestions,
            generated_at=report.generated_at,
            verification_level=report.verification_level,
            generated_status=report.generated_status,
            static_review_status=report.static_review_status,
            compile_status=report.compile_status,
            compile_results=[r.model_dump() for r in report.compile_results],
            failed_files=report.failed_files,
            toolchain=report.toolchain,
            generation_mode=report.generation_mode,
            generation_trace=report.generation_trace,
            budget=report.budget,
            required_features=report.required_features,
            canonical_targets=report.canonical_targets,
            scenario_plan=report.scenario_plan,
        )

    except ValueError as e:
        logger.error("api.generate_testcase.value_error", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("api.generate_testcase.error", error=str(e)[:300])
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)[:300]}")


# ── Single Instruction Verification (SSE Stream) ─────────────────

@router.post("/generate_testcase/stream")
async def generate_testcase_stream(request: StreamVerificationRequest):
    """Run verification with SSE event streaming for real-time progress.

    Yields SSE events:
        stage_start → stage_progress → stage_complete → result → done

    The frontend consumes this stream to render the real-time Pipeline panel.
    """
    instruction = request.instruction.strip()
    if not instruction:
        raise HTTPException(status_code=400, detail="instruction field is required")

    logger.info("api.generate_testcase.stream", instruction=instruction, use_llm=request.use_llm)

    try:
        sqlite = get_sqlite()
        llm = get_llm() if request.use_llm else None

        orchestrator = VerificationOrchestrator(
            sqlite_client=sqlite,
            llm=llm,
            use_llm_planning=request.use_llm,
            use_llm_review=request.use_llm,
        )

        async def event_generator():
            async for sse_msg in orchestrator.verify_stream(
                instruction, use_llm=request.use_llm, instruction_count=request.instruction_count, target_instruction_count=request.target_instruction_count,
            ):
                yield sse_msg

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    except Exception as e:
        logger.error("api.generate_testcase.stream.error", error=str(e)[:300])
        raise HTTPException(status_code=500, detail=f"Stream verification failed: {str(e)[:300]}")


# ── Batch Verification (Sync) ────────────────────────────────────

@router.post("/generate_testcases", response_model=BatchGenerateResponse)
async def generate_testcases(request: BatchGenerateRequest) -> BatchGenerateResponse:
    """Run verification for multiple ARM instructions in sequence."""
    if not request.instructions:
        raise HTTPException(status_code=400, detail="instructions list is required")

    logger.info("api.generate_testcases", count=len(request.instructions), use_llm=request.use_llm)

    try:
        sqlite = get_sqlite()
        llm = get_llm() if request.use_llm else None

        orchestrator = VerificationOrchestrator(
            sqlite_client=sqlite,
            llm=llm,
            use_llm_planning=request.use_llm,
            use_llm_review=request.use_llm,
        )

        reports: list[dict] = []
        pass_count = 0
        fail_count = 0

        for instr in request.instructions:
            instr = instr.strip().upper()
            if not instr:
                continue
            report = orchestrator.verify(instr, use_llm=request.use_llm, instruction_count=request.instruction_count)
            reports.append(report.to_json_api())
            if report.status in ("PASS", "REPAIRED"):
                pass_count += 1
            else:
                fail_count += 1

        summary = f"Processed {len(reports)} instructions: {pass_count} passed, {fail_count} failed"

        return BatchGenerateResponse(
            total=len(reports),
            reports=reports,
            summary=summary,
        )

    except Exception as e:
        logger.error("api.generate_testcases.error", error=str(e)[:300])
        raise HTTPException(status_code=500, detail=f"Batch verification failed: {str(e)[:300]}")


# ── Batch Verification (SSE Stream) ──────────────────────────────

@router.post("/generate_testcases/stream")
async def generate_testcases_stream(request: BatchStreamRequest):
    """Run batch verification with SSE event streaming."""
    if not request.instructions:
        raise HTTPException(status_code=400, detail="instructions list is required")

    logger.info("api.generate_testcases.stream", count=len(request.instructions), use_llm=request.use_llm)

    try:
        sqlite = get_sqlite()
        llm = get_llm() if request.use_llm else None

        orchestrator = VerificationOrchestrator(
            sqlite_client=sqlite,
            llm=llm,
            use_llm_planning=request.use_llm,
            use_llm_review=request.use_llm,
        )

        async def event_generator():
            async for sse_msg in orchestrator.verify_batch_stream(
                request.instructions,
                use_llm=request.use_llm,
                instruction_count=request.instruction_count,
            ):
                yield sse_msg

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    except Exception as e:
        logger.error("api.generate_testcases.stream.error", error=str(e)[:300])
        raise HTTPException(status_code=500, detail=f"Batch stream failed: {str(e)[:300]}")


# ── File Download ────────────────────────────────────────────────

@router.get("/testcase/{instruction}/{file_id}")
async def download_test_file(instruction: str, file_id: str) -> dict[str, Any]:
    """Download a single generated test file by file_id.

    The file content is returned inline for frontend display.
    File ID format: {INSN}_test_name, e.g. ADD_test_normal_01
    """
    logger.info("api.download.file", instruction=instruction.upper(), file_id=file_id)

    try:
        sqlite = get_sqlite()

        orchestrator = VerificationOrchestrator(
            sqlite_client=sqlite, llm=None,
        )
        report = orchestrator.verify(instruction.upper())

        for tf in report.test_files:
            if tf.file_id == file_id:
                return {
                    "file_id": tf.file_id,
                    "filename": tf.filename,
                    "format": tf.format,
                    "content": tf.content,
                    "status": tf.status,
                }

        raise HTTPException(status_code=404, detail=f"Test file '{file_id}' not found for '{instruction}'")

    except HTTPException:
        raise
    except Exception as e:
        logger.error("api.download.file.error", error=str(e)[:300])
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)[:300]}")


@router.post("/testcase/download-all")
async def download_all_testcase(request: DownloadFileRequest):
    """Download all passing test files for an instruction as a ZIP archive."""
    instruction = request.instruction.strip().upper()
    if not instruction:
        raise HTTPException(status_code=400, detail="instruction field is required")

    logger.info("api.download.all", instruction=instruction)

    try:
        sqlite = get_sqlite()

        orchestrator = VerificationOrchestrator(
            sqlite_client=sqlite, llm=None,
        )
        report = orchestrator.verify(instruction)

        # Filter tests
        if request.file_ids:
            files = [tf for tf in report.test_files if tf.file_id in request.file_ids]
        else:
            files = [tf for tf in report.test_files if tf.status == "pass"]

        # Build ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            folder = f"{instruction}/"
            for tf in files:
                zf.writestr(folder + tf.filename, tf.content)

        zip_buffer.seek(0)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="{instruction}_testcases.zip"',
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("api.download.all.error", error=str(e)[:300])
        raise HTTPException(status_code=500, detail=f"ZIP creation failed: {str(e)[:300]}")


@router.post("/testcase/batch-download")
async def batch_download_testcases(request: BatchDownloadRequest):
    """Download test files for multiple instructions as a single ZIP."""
    if not request.instructions:
        raise HTTPException(status_code=400, detail="instructions list is required")

    logger.info("api.download.batch", instructions=request.instructions)

    try:
        sqlite = get_sqlite()

        orchestrator = VerificationOrchestrator(
            sqlite_client=sqlite, llm=None,
        )

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for instr_name in request.instructions:
                instr_name = instr_name.strip().upper()
                if not instr_name:
                    continue
                report = orchestrator.verify(instr_name)
                folder = f"{instr_name}/"
                for tf in report.test_files:
                    if request.only_passing and tf.status != "pass":
                        continue
                    zf.writestr(folder + tf.filename, tf.content)

        zip_buffer.seek(0)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": 'attachment; filename="arm_testcases_batch.zip"',
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("api.download.batch.error", error=str(e)[:300])
        raise HTTPException(status_code=500, detail=f"Batch ZIP failed: {str(e)[:300]}")


# ── Scenario Batch (Multi-instruction per program) ────────────────

@router.post("/scenario/stream")
async def scenario_batch_stream(request: ScenarioBatchStreamRequest):
    """Run scenario-based batch verification with SSE streaming.

    Each entry in *scenarios* is a list of instruction mnemonics that get
    combined into a single test program.  One scenario = one row = one test
    program.  The same SSE events are emitted as for the regular batch stream.

    Example request body:
      {"scenarios": [["ADD","SUB","MOV"], ["LDR","STR"]], "use_llm": false, "instruction_count": 100}
    """
    if not request.scenarios:
        raise HTTPException(status_code=400, detail="scenarios list is required")

    logger.info("api.scenario.stream", num_scenarios=len(request.scenarios), use_llm=request.use_llm)

    try:
        sqlite = get_sqlite()
        llm = get_llm() if request.use_llm else None

        orchestrator = VerificationOrchestrator(
            sqlite_client=sqlite,
            llm=llm,
            use_llm_planning=request.use_llm,
            use_llm_review=request.use_llm,
        )

        async def event_generator():
            async for sse_msg in orchestrator.verify_scenario_program_stream(
                request.scenarios,
                use_llm=request.use_llm,
                instruction_count=request.instruction_count,
                target_instruction_count=request.target_instruction_count,
            ):
                yield sse_msg

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    except Exception as e:
        logger.error("api.scenario.stream.error", error=str(e)[:300])
        raise HTTPException(status_code=500, detail=f"Scenario stream failed: {str(e)[:300]}")


@router.post("/scenario/parse")
async def parse_scenario_content(request: ParseScenarioFileRequest):
    """Parse raw text content in scenario format and return structured scenarios.

    Format: one row per scenario, comma-separated instruction mnemonics.
    Lines with only whitespace are ignored.

    Example input:
        ADD,SUB,MOV
        LDR,STR
        CMP,B.cond

    Returns: {"scenarios": [["ADD","SUB","MOV"],["LDR","STR"],["CMP","B.cond"]]}
    """
    lines = [line.strip() for line in request.content.splitlines() if line.strip()]
    scenarios: list[list[str]] = []
    for line in lines:
        items = [item.strip() for item in line.split(",") if item.strip()]
        if items:
            scenarios.append(items)
    return {"scenarios": scenarios}
