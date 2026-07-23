"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CopyButton } from "@/components/common/copy-button";
import type { StageDetail } from "@/lib/api/types";
import { ChevronDown, ChevronRight } from "lucide-react";

interface ReasoningTimelineProps {
  stages: StageDetail[];
}

export function ReasoningTimeline({ stages }: ReasoningTimelineProps) {
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  const toggle = (stage: string) => {
    setExpanded((prev) => ({ ...prev, [stage]: !prev[stage] }));
  };

  if (!stages.length) {
    return <p className="text-muted-foreground text-sm">No stage data available.</p>;
  }

  return (
    <div className="space-y-3">
      {stages.map((stage, i) => (
        <Card key={i} className="overflow-hidden">
          <div
            className="flex items-center gap-3 px-4 py-3 cursor-pointer hover:bg-muted/50"
            onClick={() => toggle(stage.stage)}
          >
            <span className="text-sm">
              {expanded[stage.stage] ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
            </span>
            <Badge variant="outline" className="font-mono text-xs capitalize">
              {stage.stage}
            </Badge>
            <span className="flex-1 text-sm">
              {stage.summary || "No summary"}
            </span>
            <Badge
              variant="secondary"
              className={
                stage.status === "ok"
                  ? "bg-green-100 text-green-700"
                  : stage.status === "warning"
                    ? "bg-yellow-100 text-yellow-700"
                    : stage.status === "error"
                      ? "bg-red-100 text-red-700"
                      : stage.status === "skipped"
                        ? "bg-gray-100 text-gray-500"
                        : ""
              }
            >
              {stage.status}
            </Badge>
            <span className="text-xs text-muted-foreground font-mono w-16 text-right">
              {stage.duration_ms > 0 ? `${stage.duration_ms.toFixed(0)}ms` : ""}
            </span>
          </div>

          {expanded[stage.stage] && (
            <div className="px-4 pb-4 space-y-2 border-t pt-3">
              {stage.reasoning && (
                <div>
                  <h4 className="text-xs font-semibold text-muted-foreground mb-1">Reasoning</h4>
                  <p className="text-sm whitespace-pre-wrap">{stage.reasoning}</p>
                </div>
              )}

              {stage.key_findings.length > 0 && (
                <div>
                  <h4 className="text-xs font-semibold text-muted-foreground mb-1">Key Findings</h4>
                  <ul className="list-disc list-inside text-sm space-y-0.5">
                    {stage.key_findings.map((f, j) => (
                      <li key={j}>{f}</li>
                    ))}
                  </ul>
                </div>
              )}

              {Object.keys(stage.data_snapshot).length > 0 && (
                <div>
                  <h4 className="text-xs font-semibold text-muted-foreground mb-1">Snapshot</h4>
                  <div className="grid grid-cols-2 gap-1 text-sm">
                    {Object.entries(stage.data_snapshot).map(([k, v]) => (
                      <div key={k} className="flex justify-between bg-muted/50 px-2 py-1 rounded">
                        <span className="text-muted-foreground">{k}</span>
                        <span className="font-mono">{String(v)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {stage.error && (
                <div className="text-sm text-red-600 font-mono bg-red-50 dark:bg-red-950/20 p-2 rounded">
                  {stage.error}
                </div>
              )}
            </div>
          )}
        </Card>
      ))}
    </div>
  );
}
