"use client";

import { useCallback, useRef, useState } from "react";
import { api } from "@/lib/api/client";
import type {
  PipelineStage,
  PipelineState,
  SSEEventName,
  StageCompleteEvent,
  StageProgressEvent,
  StageStartEvent,
  StageStatus,
  StageUIState,
  VerificationParams,
  VerificationResult,
} from "@/lib/api/types";
import {
  DEFAULT_VERIFICATION_PARAMS,
} from "@/lib/api/types";
import type {
  BatchInstructionState,
} from "@/lib/api/types";
import type {
  ScenarioState,
} from "@/lib/api/types";

// ── Helpers ──────────────────────────────────────────────────────

const STAGE_ORDER: PipelineStage[] = [
  "analyzer",
  "planner",
  "splitter",
  "llm",
  "generator",
  "compiler",
  "reviewer",
];

const INITIAL_STAGES: Record<PipelineStage, StageUIState> = {
  analyzer: { status: "pending", message: "Waiting...", detail: "Waiting...", duration_ms: 0, summary: "", findings: [] },
  planner: { status: "pending", message: "Waiting...", detail: "Waiting...", duration_ms: 0, summary: "", findings: [] },
  retrieval: { status: "pending", message: "Waiting...", detail: "Waiting...", duration_ms: 0, summary: "", findings: [] },
  splitter: { status: "pending", message: "Waiting...", detail: "Waiting...", duration_ms: 0, summary: "", findings: [] },
  llm: { status: "pending", message: "Waiting...", detail: "Waiting...", duration_ms: 0, summary: "", findings: [] },
  generator: { status: "pending", message: "Waiting...", detail: "Waiting...", duration_ms: 0, summary: "", findings: [] },
  compiler: { status: "pending", message: "Waiting...", detail: "Waiting...", duration_ms: 0, summary: "", findings: [] },
  reviewer: { status: "pending", message: "Waiting...", detail: "Waiting...", duration_ms: 0, summary: "", findings: [] },
  repair: { status: "pending", message: "Waiting...", detail: "Waiting...", duration_ms: 0, summary: "", findings: [] },
};

// ── Pipeline (UI) helpers ─────────────────────────────────────

/** Stage order that PipelineProgress component renders */
const UI_STAGE_ORDER: readonly string[] = [
  "planner",
  "retrieval",
  "llm",
  "generator",
  "reviewer",
  "compiler",
] as const;

/** Map the hook-internal stage name → canonical UI PipelineStage */
function toUiPipelineStage(hookStage: PipelineStage | string): PipelineStage | null {
  const m: Record<string, string> = {
    analyzer: "retrieval",
    planner: "planner",
    splitter: "generator",
    llm: "llm",
    generator: "generator",
    compiler: "compiler",
    reviewer: "reviewer",
  };
  return (m[hookStage] ?? null) as PipelineStage | null;
}

/** Create a fresh PipelineState for PipelineProgress */
function createInitialPipeline(): PipelineState {
  const stages = {} as Record<string, StageUIState>;
  for (const key of UI_STAGE_ORDER) {
    stages[key] = {
      status: "pending" as StageStatus,
      message: "Waiting...",
      duration_ms: 0,
      summary: "",
      findings: [],
    };
  }
  return {
    stages: stages as Record<PipelineStage, StageUIState>,
    current_stage: null,
    is_running: true,
    total_duration_ms: 0,
  };
}

/** Apply a stage event to *pipeline*, returning a new stages snapshot */
function applyStageToPipeline(
  prev: PipelineState,
  eventName: SSEEventName,
  data: Record<string, unknown>,
): PipelineState {
  const stages = { ...prev.stages } as Record<string, StageUIState>;
  let active: PipelineStage | null = null;

  // Derive raw stage name from event data
  let rawName = "";
  if (eventName === "stage_start") {
    rawName = (data as { stage?: string }).stage ?? "";
  } else if (eventName === "stage_progress") {
    rawName = (data as { stage?: string }).stage ?? "";
  } else if (eventName === "stage_complete") {
    rawName = (data as { stage?: string }).stage ?? "";
  }

  // Map via hook's stageKey first, then to UI stage
  const hookName = rawName ? stageKey(rawName) : null;
  const uiName = hookName ? toUiPipelineStage(hookName) : null;

  if (uiName && stages[uiName]) {
    active = uiName as PipelineStage;

    if (eventName === "stage_start") {
      const msg = (data as { detail?: string; message?: string }).detail
        ?? (data as { message?: string }).message
        ?? "In progress...";
      stages[uiName] = { ...stages[uiName], status: "running" as StageStatus, message: msg };
    } else if (eventName === "stage_progress") {
      const detail = (data as { detail?: string }).detail ?? stages[uiName].message;
      stages[uiName] = { ...stages[uiName], message: detail };
    } else if (eventName === "stage_complete") {
      const ev = data as unknown as StageCompleteEvent & { status?: string };
      const status = String(ev.status ?? "");
      const isOk = status === "passed" || status === "completed" || status === "ok" || status === "skipped";
      stages[uiName] = {
        ...stages[uiName],
        status: (isOk ? "ok" : "error") as StageStatus,
        duration_ms: ev.duration_ms ?? stages[uiName].duration_ms,
        summary: ev.summary ?? stages[uiName].summary,
      };
      // Advance previous stages
      const idx = UI_STAGE_ORDER.indexOf(uiName);
      for (let i = 0; i < idx; i++) {
        const st = UI_STAGE_ORDER[i];
        if (stages[st].status === "pending" || stages[st].status === "running") {
          stages[st] = { ...stages[st], status: "ok" as StageStatus };
        }
      }
    }
  }

  return {
    stages: stages as Record<PipelineStage, StageUIState>,
    current_stage: active,
    is_running: true,
    total_duration_ms: prev.total_duration_ms,
  };
}

// ── SSE stage helpers (existing) ──────────────────────────────

type StageEventData = {
  stage_progress: StageProgressEvent;
  stage_start: StageStartEvent;
  stage_complete: StageCompleteEvent;
};

function stageKey(label: string): PipelineStage | null {
  const map: Record<string, PipelineStage> = {
    analyzer: "analyzer",
    analyse: "analyzer",
    planner: "planner",
    planning: "planner",
    plan: "planner",
    retrieval: "retrieval",
    splitting: "splitter",
    split: "splitter",
    splitter: "splitter",
    llm: "llm",
    generator: "generator",
    generating: "generator",
    generation: "generator",
    reviewer: "reviewer",
    compile: "compiler",
    compiling: "compiler",
    compiler: "compiler",
    reviewing: "reviewer",
    review: "reviewer",
  };
  return map[label.toLowerCase()] ?? null;
}

const COMMON_SSE_HANDLER = (
  stages: Record<PipelineStage, StageUIState>,
  eventName: SSEEventName,
  data: StageEventData,
): { stage: PipelineStage | null; new_stage: boolean } | null => {
  if (eventName === "stage_start") {
    const ev = data.stage_start;
    const st = stageKey(ev.stage);
    if (st) {
      const wasRunning = stages[st].status === "running";
      const message = ev.message ?? "In progress...";
      stages[st] = {
        ...stages[st],
        status: "running",
        message,
        detail: message,
      };
      return { stage: st, new_stage: !wasRunning };
    }
  }
  if (eventName === "stage_progress") {
    const ev = data.stage_progress;
    const st = stageKey(ev.stage);
    if (st) {
      stages[st] = {
        ...stages[st],
        detail: ev.detail ?? "In progress...",
        message: ev.detail ?? "In progress...",
        status: "running",
      };
      return { stage: st, new_stage: false };
    }
  }
  if (eventName === "stage_complete") {
    const ev = data.stage_complete;
    const st = stageKey(ev.stage);
    if (st) {
      const eventStatus = String(ev.status ?? "");
      const isPass = eventStatus === "passed" || eventStatus === "completed" || eventStatus === "ok";
      stages[st] = {
        status: eventStatus === "skipped" ? "skipped" : isPass ? "completed" : "failed",
        message: ev.summary ?? stages[st].detail ?? "",
        detail: ev.summary ?? stages[st].detail,
        duration_ms: ev.duration_ms ?? stages[st].duration_ms,
        summary: ev.summary ?? stages[st].summary,
        findings: ev.findings ?? stages[st].findings,
      };
      // Mark all previous stages as completed if they're still running
      const idx = STAGE_ORDER.indexOf(st);
      for (let i = 0; i < idx; i++) {
        const prev = STAGE_ORDER[i];
        if (stages[prev].status === "running" || stages[prev].status === "pending") {
          stages[prev] = { ...stages[prev], status: "completed" };
        }
      }
      return { stage: st, new_stage: false };
    }
  }
  return null;
};

// ── Hook: useBatchVerification ────────────────────────────────────

export function useBatchVerification() {
  const [instructions, setInstructions] = useState<BatchInstructionState[]>([]);
  const [activeIndex, setActiveIndex] = useState(-1);
  const [completed, setCompleted] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [totalDurationMs, setTotalDurationMs] = useState(0);
  const [currentPipeline, setCurrentPipeline] = useState<PipelineState>(createInitialPipeline());

  const abortRef = useRef<AbortController | null>(null);
  const activeIdxRef = useRef(-1);

  const startBatch = useCallback(async (
    instrList: string[],
    params: VerificationParams = DEFAULT_VERIFICATION_PARAMS,
  ) => {
    const controller = new AbortController();
    abortRef.current = controller;

    const initial: BatchInstructionState[] = instrList.map((i) => ({
      instruction: i,
      status: "waiting" as const,
      result: null,
      current_stage: null,
      duration_ms: 0,
      review_score: 0,
    }));

    setInstructions(initial);
    setActiveIndex(0);
    setCompleted(0);
    setIsRunning(true);
    setTotalDurationMs(0);
    setCurrentPipeline(createInitialPipeline());

    const stages: Record<PipelineStage, StageUIState> = { ...INITIAL_STAGES };

    try {
      const response = await fetch(api.generateTestcasesStreamUrl(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          instructions: instrList,
          use_llm: params.use_llm,
          instruction_count: params.instruction_count,
          target_instruction_count: params.target_instruction_count,
        }),
        signal: controller.signal,
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}: ${await response.text()}`);

      const reader = response.body?.getReader();
      if (!reader) throw new Error("No response body");

      const dec = new TextDecoder();
      let buf = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });

        const lines = buf.split("\n");
        buf = lines.pop() ?? "";

        let eventName: SSEEventName | "" = "";
        let dataStr = "";

        for (const line of lines) {
          if (line.startsWith("event: ")) {
            eventName = line.slice(7).trim() as SSEEventName;
          }
          if (line.startsWith("data: ")) {
            dataStr = line.slice(6);
          }
          if (line === "" && eventName !== "" && dataStr !== "") {
            // Process event
            try {
              const data = JSON.parse(dataStr);

              if (eventName === "instruction_start") {
                const idx = data.index as number;
                activeIdxRef.current = idx;
                setActiveIndex(idx);
                setInstructions((prev) =>
                  prev.map((ins, i) =>
                    i === idx ? { ...ins, status: "running" as const } : ins,
                  ),
                );
              }

              // Stage events
              const stageInfo = COMMON_SSE_HANDLER(stages, eventName, data as StageEventData);
              if (stageInfo) {
                const curIdx = activeIdxRef.current;
                setInstructions((prev) =>
                  prev.map((ins, i) =>
                    i === curIdx
                      ? { ...ins, current_stage: stageInfo.stage }
                      : ins,
                  ),
                );
              }

              // Update UI pipeline for PipelineProgress
              if (eventName === "stage_start" || eventName === "stage_progress" || eventName === "stage_complete") {
                setCurrentPipeline((prev) =>
                  applyStageToPipeline(prev, eventName as SSEEventName, data as Record<string, unknown>),
                );
              }

              if (eventName === "result") {
                const res = data as VerificationResult;
                setInstructions((prev) => {
                  const next = [...prev];
                  const idx = prev.findIndex(
                    (i) => i.instruction === res.instruction && i.status === "running",
                  );
                  if (idx >= 0) {
                    next[idx] = {
                      ...next[idx],
                      status: "completed" as const,
                      result: res,
                      review_score: res.review_score,
                    };
                  }
                  return next;
                });
              }

              if (eventName === "instruction_complete") {
                const d = data;
                setInstructions((prev) => {
                  const next = [...prev];
                  const idx = prev.findIndex(
                    (i) => i.instruction === d.instruction && i.status === "running",
                  );
                  if (idx >= 0) {
                    next[idx] = {
                      ...next[idx],
                      status: "completed" as const,
                      review_score: d.review_score ?? 0,
                    };
                  }
                  return next;
                });
                setCompleted((c) => c + 1);
              }

              if (eventName === "batch_complete") {
                setTotalDurationMs(data.total_duration_ms ?? 0);
              }
            } catch {
              // skip malformed
            }
            eventName = "";
            dataStr = "";
          }
        }
      }
    } catch (err: unknown) {
      if (err instanceof Error && err.name !== "AbortError") {
        throw err;
      }
    } finally {
      setIsRunning(false);
    }
  }, []);

  const stopBatch = useCallback(() => {
    abortRef.current?.abort();
  }, []);

  return {
    instructions,
    activeIndex,
    completed,
    total: instructions.length,
    isRunning,
    totalDurationMs,
    currentPipeline,
    startBatch,
    stopBatch,
  };
}

// ── Hook: useScenarioBatchVerification ────────────────────────────

export function useScenarioBatchVerification() {
  const [scenarios, setScenarios] = useState<ScenarioState[]>([]);
  const [activeIndex, setActiveIndex] = useState(-1);
  const [completed, setCompleted] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [totalDurationMs, setTotalDurationMs] = useState(0);
  const [currentPipeline, setCurrentPipeline] = useState<PipelineState>(createInitialPipeline());

  const abortRef = useRef<AbortController | null>(null);
  const activeIdxRef = useRef(-1);

  const startBatch = useCallback(async (
    scenarioList: Array<{ label: string; instructions: string[] }>,
    params: VerificationParams = DEFAULT_VERIFICATION_PARAMS,
  ) => {
    const controller = new AbortController();
    abortRef.current = controller;

    const initial: ScenarioState[] = scenarioList.map((s) => ({
      label: s.label,
      instructions: s.instructions,
      status: "waiting" as const,
      result: null,
      current_stage: null,
      duration_ms: 0,
      review_score: 0,
    }));

    setScenarios(initial);
    setActiveIndex(0);
    setCompleted(0);
    setIsRunning(true);
    setTotalDurationMs(0);
    setCurrentPipeline(createInitialPipeline());

    const stages: Record<PipelineStage, StageUIState> = { ...INITIAL_STAGES };

    try {
      const response = await fetch(api.scenarioStreamUrl(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          scenarios: scenarioList.map((s) => s.instructions),
          use_llm: params.use_llm,
          instruction_count: params.instruction_count,
          target_instruction_count: params.target_instruction_count,
        }),
        signal: controller.signal,
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}: ${await response.text()}`);

      const reader = response.body?.getReader();
      if (!reader) throw new Error("No response body");

      const dec = new TextDecoder();
      let buf = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });

        const lines = buf.split("\n");
        buf = lines.pop() ?? "";

        let eventName: SSEEventName | "" = "";
        let dataStr = "";

        for (const line of lines) {
          if (line.startsWith("event: ")) {
            eventName = line.slice(7).trim() as SSEEventName;
          }
          if (line.startsWith("data: ")) {
            dataStr = line.slice(6);
          }
          if (line === "" && eventName !== "" && dataStr !== "") {
            try {
              const data = JSON.parse(dataStr);

              if (eventName === "instruction_start") {
                const idx = data.index as number;
                activeIdxRef.current = idx;
                setActiveIndex(idx);
                setScenarios((prev) =>
                  prev.map((sc, i) =>
                    i === idx ? { ...sc, status: "running" as const } : sc,
                  ),
                );
              }

              const stageInfo = COMMON_SSE_HANDLER(stages, eventName, data as StageEventData);
              if (stageInfo) {
                const curIdx = activeIdxRef.current;
                setScenarios((prev) =>
                  prev.map((sc, i) =>
                    i === curIdx
                      ? { ...sc, current_stage: stageInfo.stage }
                      : sc,
                  ),
                );
              }

              // Update UI pipeline for PipelineProgress
              if (eventName === "stage_start" || eventName === "stage_progress" || eventName === "stage_complete") {
                setCurrentPipeline((prev) =>
                  applyStageToPipeline(prev, eventName as SSEEventName, data as Record<string, unknown>),
                );
              }

              if (eventName === "result") {
                const res = data as VerificationResult;
                setScenarios((prev) => {
                  const next = [...prev];
                  const idx = prev.findIndex(
                    (sc) => sc.label === res.instruction && (sc.status === "running" || sc.status === "waiting"),
                  );
                  if (idx >= 0) {
                    next[idx] = {
                      ...next[idx],
                      status: "completed" as const,
                      result: res,
                      review_score: res.review_score,
                    };
                  }
                  return next;
                });
              }

              if (eventName === "instruction_complete") {
                setCompleted((c) => c + 1);
              }

              if (eventName === "batch_complete") {
                setTotalDurationMs(data.total_duration_ms ?? 0);
              }
            } catch {
              // skip malformed
            }
            eventName = "";
            dataStr = "";
          }
        }
      }
    } catch (err: unknown) {
      if (err instanceof Error && err.name !== "AbortError") {
        throw err;
      }
    } finally {
      setIsRunning(false);
    }
  }, []);

  const stopBatch = useCallback(() => {
    abortRef.current?.abort();
  }, []);

  return {
    scenarios,
    activeIndex,
    completed,
    total: scenarios.length,
    isRunning,
    totalDurationMs,
    currentPipeline,
    startBatch,
    stopBatch,
  };
}
