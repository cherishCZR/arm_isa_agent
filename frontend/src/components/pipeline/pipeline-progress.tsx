"use client";

import { cn } from "@/lib/utils";
import type { PipelineStage, PipelineState, StageStatus } from "@/lib/api/types";

const STAGE_LABELS: Record<PipelineStage, { icon: string; label: string; description: string }> = {
  analyzer: { icon: "A", label: "Analyzer", description: "Analyzing scenario input" },
  planner: { icon: "P", label: "Planner", description: "Analyzing constraints and planning" },
  retrieval: { icon: "R", label: "Retrieval", description: "Loading instruction profile" },
  splitter: { icon: "T", label: "Splitter", description: "Preparing scenario groups" },
  llm: { icon: "AI", label: "LLM", description: "Generating structured assembly" },
  generator: { icon: "G", label: "Generator", description: "Creating test program" },
  compiler: { icon: "C", label: "Compiler", description: "Compile-only validation" },
  reviewer: { icon: "S", label: "Static Review", description: "Reviewing generated assembly" },
  repair: { icon: "C", label: "Compile", description: "Compile-only validation" },
};

const STATUS_DOT: Record<StageStatus, string> = {
  pending: ".",
  running: "*",
  completed: "OK",
  failed: "X",
  ok: "OK",
  warning: "!",
  error: "X",
  skipped: "-",
};

const STATUS_COLOR: Record<StageStatus, string> = {
  pending: "text-muted-foreground/40",
  running: "text-blue-500",
  completed: "text-green-600",
  failed: "text-red-600",
  ok: "text-green-600",
  warning: "text-yellow-600",
  error: "text-red-600",
  skipped: "text-muted-foreground/50",
};

interface PipelineProgressProps {
  pipeline: PipelineState;
  instruction?: string;
  className?: string;
}

export function PipelineProgress({ pipeline, instruction, className }: PipelineProgressProps) {
  return (
    <div className={cn("rounded-lg border bg-card p-4 space-y-0.5", className)}>
      <div className="flex items-center justify-between mb-3 px-2">
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold">
            {instruction ? `Verifying: ${instruction}` : "Pipeline"}
          </span>
          {pipeline.is_running && (
            <span className="inline-block w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
          )}
        </div>
        <span className="text-xs text-muted-foreground font-mono">
          {pipeline.total_duration_ms > 0
            ? `${pipeline.total_duration_ms.toFixed(0)}ms`
            : pipeline.is_running
              ? "running..."
              : ""}
        </span>
      </div>

      {STAGE_ORDER.map((key) => {
        const stage = pipeline.stages[key];
        const { icon, label } = STAGE_LABELS[key];
        const colorClass = STATUS_COLOR[stage.status];
        const dot = STATUS_DOT[stage.status];

        return (
          <PipelineStageRow
            key={key}
            icon={icon}
            label={label}
            status={stage.status}
            message={stage.message ?? stage.detail ?? ""}
            durationMs={stage.duration_ms}
            colorClass={colorClass}
            dot={dot}
          />
        );
      })}
    </div>
  );
}

function PipelineStageRow({
  icon,
  label,
  status,
  message,
  durationMs,
  colorClass,
  dot,
}: {
  icon: string;
  label: string;
  status: StageStatus;
  message: string;
  durationMs: number;
  colorClass: string;
  dot: string;
}) {
  return (
    <div
      className={cn(
        "flex items-center gap-3 py-1.5 px-2 rounded text-sm transition-colors",
        status === "running" && "bg-blue-50/50 dark:bg-blue-950/20",
      )}
    >
      <span className="w-6 text-center text-[10px] font-mono">{dot}</span>
      <span className="font-mono text-xs w-[122px] shrink-0">
        {icon} {label}
      </span>

      {status !== "pending" ? (
        <>
          <span className={cn("flex-1 truncate", colorClass)}>
            {status === "running" && (
              <span className="inline-block w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse mr-1.5 align-middle" />
            )}
            {message || "Running..."}
          </span>
          {durationMs > 0 && (
            <span className="text-xs text-muted-foreground w-16 text-right font-mono shrink-0">
              {durationMs.toFixed(0)}ms
            </span>
          )}
        </>
      ) : (
        <>
          <span className="flex-1 text-muted-foreground/30">-----</span>
          <span className="text-xs text-muted-foreground/40 w-16 text-right shrink-0">waiting</span>
        </>
      )}
    </div>
  );
}

export const STAGE_ORDER: PipelineStage[] = ["planner", "retrieval", "llm", "generator", "reviewer", "compiler"];
export { STAGE_LABELS };
