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
  VerificationResult,
} from "@/lib/api/types";
import { api } from "@/lib/api/client";

const STAGE_ORDER: PipelineStage[] = ["planner", "retrieval", "generator", "reviewer", "repair"];

function initialStages(): Record<PipelineStage, StageUIState> {
  const stages = {} as Record<PipelineStage, StageUIState>;
  for (const s of STAGE_ORDER) {
    stages[s] = { status: "pending", message: "", duration_ms: 0, summary: "", findings: [] };
  }
  return stages;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  result?: VerificationResult;
  pipeline?: PipelineState;
  isStreaming?: boolean;
}

export function useChatSSE() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [pipeline, setPipeline] = useState<PipelineState>({
    stages: initialStages(),
    current_stage: null,
    is_running: false,
    total_duration_ms: 0,
  });
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const handleSSEEvent = useCallback(
    (
      event: SSEEventName,
      data: Record<string, unknown>,
      assistantMsgId: string,
      setContent: (updater: (prev: string) => string) => void,
    ) => {
      switch (event) {
        case "stage_start": {
          const d = data as unknown as StageStartEvent;
          setPipeline((prev) => {
            const stages = { ...prev.stages };
            stages[d.stage] = { ...stages[d.stage], status: "running" as StageStatus, message: d.message };
            return { ...prev, stages, current_stage: d.stage, is_running: true };
          });
          break;
        }
        case "stage_progress": {
          const d = data as unknown as StageProgressEvent;
          setPipeline((prev) => {
            const stages = { ...prev.stages };
            stages[d.stage] = { ...stages[d.stage], message: d.detail };
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
          // Update the assistant message with the result
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantMsgId
                ? { ...m, result: res, content: `Generated ${res.total_tests} test cases for ${res.instruction}: ${res.passing_tests} passing, ${res.failing_tests} failing (${res.review_score.toFixed(0)}/100).` }
                : m,
            ),
          );
          break;
        }
        case "done": {
          setPipeline((prev) => ({ ...prev, is_running: false, current_stage: null }));
          setIsStreaming(false);
          break;
        }
        // Also handle token stream events if any
        default: {
          // If content field exists, append as streaming tokens
          if (typeof data.content === "string") {
            setContent((prev) => prev + data.content);
          }
        }
      }
    },
    [],
  );

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isStreaming) return;

      const controller = new AbortController();
      abortRef.current = controller;
      setIsStreaming(true);
      setError(null);

      const userMsg: ChatMessage = {
        id: `usr-${Date.now()}`,
        role: "user",
        content: content.trim(),
        timestamp: new Date().toISOString(),
      };

      const assistantId = `asst-${Date.now()}`;

      setMessages((prev) => [
        ...prev,
        userMsg,
        {
          id: assistantId,
          role: "assistant",
          content: "Thinking...",
          timestamp: new Date().toISOString(),
          isStreaming: true,
        },
      ]);

      let streamedContent = "";

      try {
        // First try the chat endpoint, fall back to verification SSE
        const response = await fetch(`${api.generateTestcaseStreamUrl().replace("/generate_testcase/stream", "/chat/stream")}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: content.trim(),
            history: messages.map((m) => ({ role: m.role, content: m.content })),
          }),
          signal: controller.signal,
        });

        if (response.ok) {
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
                  handleSSEEvent(eventName, data, assistantId, (updater) => {
                    streamedContent = updater(streamedContent);
                    setMessages((prev) =>
                      prev.map((m) => (m.id === assistantId ? { ...m, content: streamedContent } : m)),
                    );
                  });
                } catch { /* skip */ }
                eventName = "";
              }
            }
          }
        } else {
          throw new Error(`Chat endpoint not available (${response.status})`);
        }
      } catch (err: unknown) {
        if (err instanceof DOMException && err.name === "AbortError") {
          setMessages((prev) =>
            prev.map((m) => (m.id === assistantId ? { ...m, content: "Cancelled.", isStreaming: false } : m)),
          );
          setIsStreaming(false);
          return;
        }

        // Fallback: use regular verification
        const errMsg = err instanceof Error ? err.message : String(err);
        if (errMsg.includes("not available") || errMsg.includes("404") || errMsg.includes("Failed to fetch")) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId
                ? {
                    ...m,
                    content: "Chat backend not available. You can use /verify for instruction verification.",
                    isStreaming: false,
                  }
                : m,
            ),
          );
        } else {
          setError(errMsg);
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId ? { ...m, content: `Error: ${errMsg}`, isStreaming: false } : m,
            ),
          );
        }
        setIsStreaming(false);
      }
    },
    [messages, isStreaming, handleSSEEvent],
  );

  const cancel = useCallback(() => {
    abortRef.current?.abort();
    setIsStreaming(false);
    setPipeline((prev) => ({ ...prev, is_running: false }));
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setPipeline({ stages: initialStages(), current_stage: null, is_running: false, total_duration_ms: 0 });
    setError(null);
  }, []);

  return { messages, pipeline, isStreaming, error, sendMessage, cancel, clearMessages };
}
