"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { ChevronDown, ChevronRight, Brain } from "lucide-react";
import type { StageDetail } from "@/lib/api/types";

interface ReasoningCollapseProps {
  stages: StageDetail[];
  className?: string;
}

const STAGE_LABELS: Record<string, string> = {
  planner: "Planner",
  retrieval: "Retrieval",
  generator: "Generator",
  reviewer: "Reviewer",
  repair: "Repair",
};

const STATUS_EMOJI: Record<string, string> = {
  ok: "✅", warning: "⚠️", error: "❌", skipped: "⏭️", pending: "○", running: "●",
};

export function ReasoningCollapse({ stages, className }: ReasoningCollapseProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className={cn("rounded-lg border bg-muted/30", className)}>
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-3 py-2 w-full text-left text-sm hover:bg-muted/50 rounded-lg transition-colors"
      >
        <Brain className="w-4 h-4 text-purple-500" />
        <span className="font-medium">Reasoning Summary</span>
        <span className="text-xs text-muted-foreground">
          ({stages.length} stages)
        </span>
        <span className="flex-1" />
        {open ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
      </button>

      {open && (
        <div className="px-3 pb-3 space-y-2">
          {stages.map((s) => (
            <div key={s.stage} className="pl-6 border-l-2 border-muted-foreground/20 py-1">
              <div className="flex items-center gap-2 text-xs">
                <span>{STATUS_EMOJI[s.status] || "○"}</span>
                <span className="font-semibold">{STAGE_LABELS[s.stage] || s.stage}</span>
                {s.duration_ms > 0 && (
                  <span className="text-muted-foreground font-mono">{s.duration_ms.toFixed(0)}ms</span>
                )}
              </div>
              {s.summary && (
                <p className="text-xs text-muted-foreground mt-0.5">{s.summary}</p>
              )}
              {s.key_findings && s.key_findings.length > 0 && (
                <ul className="mt-1 text-xs text-muted-foreground list-disc list-inside">
                  {s.key_findings.map((f, i) => (
                    <li key={i}>{f}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
