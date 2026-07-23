"use client";

import { useCallback, useRef, useState } from "react";
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
import { DEFAULT_VERIFICATION_PARAMS } from "@/lib/api/types";
import { api } from "@/lib/api/client";

const STAGE_ORDER: PipelineStage[] = [
  "planner",
  "retrieval",
  "llm",
  "generator",
  "reviewer",
  "compiler",
];

function initialStages(): Record<PipelineStage, StageUIState> {
  const stages = {} as Record<PipelineStage, StageUIState>;
  for (const s of STAGE_ORDER) {
    stages[s] = {
      status: "pending",
      message: "",
      duration_ms: 0,
      summary: "",
      findings: [],
    };
  }
  return stages;
}

export function useVerificationSSE() {
  const [pipeline, setPipeline] = useState<PipelineState>({
    stages: initialStages(),
    current_stage: null,
    is_running: false,
    total_duration_ms: 0,
  });
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const handleSSEEvent = useCallback(
    (event: SSEEventName, data: Record<string, unknown>) => {
      switch (event) {
        case "stage_start": {
          const d = data as unknown as StageStartEvent;
          setPipeline((prev) => {
            const stages = { ...prev.stages };
            stages[d.stage] = {
              ...stages[d.stage],
              status: "running" as StageStatus,
              message: d.message,
            };
            return { ...prev, stages, current_stage: d.stage };
          });
          break;
        }
        case "stage_progress": {
          const d = data as unknown as StageProgressEvent;
          setPipeline((prev) => {
            const stages = { ...prev.stages };
            stages[d.stage] = {
              ...stages[d.stage],
              message: d.detail,
            };
            return { ...prev, stages };
          });
          break;
        }
        case "stage_complete": {
          const d = data as unknown as StageCompleteEvent;
          setPipeline((prev) => {
            const stages = { ...prev.stages };
            stages[d.stage] = {
              status: d.status,
              message: d.summary,
              duration_ms: d.duration_ms,
              summary: d.summary,
              findings: d.findings || [],
            };
            return { ...prev, stages };
          });
          break;
        }
        case "result": {
          const res = data as unknown as VerificationResult;
          setResult(res);
          setPipeline((prev) => ({
            ...prev,
            total_duration_ms: (data.total_duration_ms as number) || 0,
          }));
          try {
            const stored = localStorage.getItem("arm_isa_history");
            const history = stored ? JSON.parse(stored) : [];
            history.unshift({
              instruction: res.instruction,
              status: res.status,
              score: res.review_score,
              timestamp: new Date().toISOString(),
              result: res,
            });
            localStorage.setItem("arm_isa_history", JSON.stringify(history.slice(0, 50)));
          } catch {
            // ignore storage errors
          }
          break;
        }
        case "done": {
          setPipeline((prev) => ({ ...prev, is_running: false, current_stage: null }));
          break;
        }
      }
    },
    [],
  );

  const startVerification = useCallback(async (
    instruction: string,
    params: VerificationParams = DEFAULT_VERIFICATION_PARAMS,
  ) => {
    const controller = new AbortController();
    abortRef.current = controller;

    const initStages = initialStages();
    setPipeline({
      stages: initStages,
      current_stage: null,
      is_running: true,
      total_duration_ms: 0,
    });
    setResult(null);
    setError(null);

    try {
      const response = await fetch(api.generateTestcaseStreamUrl(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          instruction,
          use_llm: params.use_llm,
          instruction_count: params.instruction_count,
          target_instruction_count: params.target_instruction_count,
        }),
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${await response.text()}`);
      }

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        let eventName: SSEEventName | "" = "";
        for (const line of lines) {
          if (line.startsWith("event: ")) {
            eventName = line.slice(7).trim() as SSEEventName;
          } else if (line.startsWith("data: ") && eventName) {
            try {
              const data = JSON.parse(line.slice(6));
              handleSSEEvent(eventName, data);
            } catch {
              // skip malformed JSON
            }
            eventName = "";
          }
        }
      }
    } catch (err: unknown) {
      if (err instanceof DOMException && err.name === "AbortError") {
        // User cancelled
        setPipeline((prev) => ({ ...prev, is_running: false }));
        return;
      }
      setError(err instanceof Error ? err.message : String(err));
      setPipeline((prev) => ({ ...prev, is_running: false }));
    }
  }, [handleSSEEvent]);

  const cancel = useCallback(() => {
    abortRef.current?.abort();
    setPipeline((prev) => ({ ...prev, is_running: false }));
  }, []);

  const reset = useCallback(() => {
    setPipeline({
      stages: initialStages(),
      current_stage: null,
      is_running: false,
      total_duration_ms: 0,
    });
    setResult(null);
    setError(null);
  }, []);

  return { pipeline, result, error, isRunning: pipeline.is_running, startVerification, cancel, reset };
}
