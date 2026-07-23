"use client";

import { cn } from "@/lib/utils";
import type { PipelineState } from "@/lib/api/types";

interface PipelineMiniProps {
  pipeline: PipelineState;
  className?: string;
}

/** Compact pipeline progress for embedding in chat bubbles. */
export function PipelineMini({ pipeline, className }: PipelineMiniProps) {
  const stages = ["planner", "retrieval", "generator", "reviewer", "repair"] as const;
  const labels: Record<string, string> = {
    planner: "P",
    retrieval: "R",
    generator: "G",
    reviewer: "Rv",
    repair: "Rp",
  };

  return (
    <div className={cn("flex items-center gap-1.5 py-1", className)}>
      {stages.map((s) => {
        const stage = pipeline.stages[s];
        const completed = stage.status !== "pending" && stage.status !== "running";
        const active = stage.status === "running";

        return (
          <div
            key={s}
            className={cn(
              "flex items-center gap-1 rounded px-1.5 py-0.5 text-[10px] font-mono transition-colors",
              completed && "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
              active && "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 animate-pulse",
              !completed && !active && "bg-muted text-muted-foreground/40"
            )}
          >
            <span>{labels[s]}</span>
            {stage.duration_ms > 0 && (
              <span className="opacity-60">{stage.duration_ms.toFixed(0)}ms</span>
            )}
          </div>
        );
      })}
      {pipeline.total_duration_ms > 0 && (
        <span className="text-[10px] text-muted-foreground ml-1">
          {pipeline.total_duration_ms.toFixed(0)}ms total
        </span>
      )}
    </div>
  );
}
