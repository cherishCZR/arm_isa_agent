"use client";

import { cn } from "@/lib/utils";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import type { BatchState, BatchInstructionState } from "@/lib/api/types";
import { CheckCircle2, Loader2, Clock, XCircle, AlertTriangle } from "lucide-react";

interface PipelineBatchProps {
  batch: BatchState;
  onViewResult?: (instruction: string) => void;
  className?: string;
}

const STATUS_ICON: Record<BatchInstructionState["status"], typeof CheckCircle2 | null> = {
  waiting: null,
  running: Loader2,
  completed: CheckCircle2,
  error: XCircle,
};

const STATUS_COLOR: Record<BatchInstructionState["status"], string> = {
  waiting: "text-muted-foreground/40",
  running: "text-blue-500",
  completed: "text-green-600",
  error: "text-red-600",
};

const STATUS_LABEL: Record<BatchInstructionState["status"], string> = {
  waiting: "Waiting",
  running: "Running",
  completed: "Done",
  error: "Error",
};

const STAGE_LABELS: Record<string, string> = {
  planner: "P",
  retrieval: "R",
  generator: "G",
  reviewer: "Rv",
  repair: "Rp",
};

export function PipelineBatch({ batch, onViewResult, className }: PipelineBatchProps) {
  const progress = batch.total > 0 ? (batch.completed / batch.total) * 100 : 0;

  return (
    <div className={cn("space-y-4", className)}>
      {/* Overall Progress */}
      <div className="rounded-lg border bg-card p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-semibold">Batch Progress</span>
          <span className="text-xs text-muted-foreground font-mono">
            {batch.completed}/{batch.total}
          </span>
        </div>
        <Progress value={progress} className="h-2" />
        {batch.total_duration_ms > 0 && (
          <p className="text-xs text-muted-foreground mt-2">
            Total: {batch.total_duration_ms.toFixed(0)}ms
          </p>
        )}
      </div>

      {/* Instruction List */}
      <div className="rounded-lg border bg-card">
        <div className="grid grid-cols-[1fr_100px_60px_100px] gap-3 px-4 py-2 border-b bg-muted/50 text-xs font-medium text-muted-foreground">
          <span>Instruction</span>
          <span>Status</span>
          <span>Score</span>
          <span>Duration</span>
        </div>

        {batch.instructions.map((ins, idx) => {
          const isActive = idx === batch.active_index;
          const Icon = STATUS_ICON[ins.status];
          const colorCls = STATUS_COLOR[ins.status];

          return (
            <div
              key={ins.instruction}
              className={cn(
                "grid grid-cols-[1fr_100px_60px_100px] gap-3 px-4 py-2.5 text-sm border-b last:border-0 items-center transition-colors",
                isActive && "bg-blue-50/50 dark:bg-blue-950/20"
              )}
            >
              {/* Instruction Name */}
              <div className="flex items-center gap-2">
                <code
                  className={cn(
                    "font-mono font-semibold text-sm cursor-pointer hover:text-primary",
                    colorCls
                  )}
                  onClick={() => ins.status === "completed" && onViewResult?.(ins.instruction)}
                >
                  {ins.instruction}
                </code>
                {ins.current_stage && ins.status === "running" && (
                  <Badge variant="outline" className="text-[10px] px-1 py-0 h-4">
                    {STAGE_LABELS[ins.current_stage] || ins.current_stage}
                  </Badge>
                )}
              </div>

              {/* Status */}
              <div className={cn("flex items-center gap-1 text-xs", colorCls)}>
                {Icon && (
                  <Icon
                    className={cn("w-3.5 h-3.5", ins.status === "running" && "animate-spin")}
                  />
                )}
                <span>{STATUS_LABEL[ins.status]}</span>
              </div>

              {/* Score */}
              <span className="text-xs font-mono text-right">
                {ins.review_score > 0 ? `${ins.review_score.toFixed(0)}` : "—"}
              </span>

              {/* Duration */}
              <span className="text-xs text-muted-foreground font-mono text-right">
                {ins.duration_ms > 0 ? `${ins.duration_ms.toFixed(0)}ms` : "—"}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
