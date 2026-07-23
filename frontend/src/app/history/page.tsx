"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { VerificationResultView } from "@/components/verification/result-view";
import type { VerificationResult } from "@/lib/api/types";

export default function HistoryPage() {
  const [history] = useState<Array<{
    instruction: string;
    status: string;
    score: number;
    timestamp: string;
    result?: VerificationResult;
  }>>(() => {
    if (typeof window === "undefined") return [];
    try {
      const stored = localStorage.getItem("arm_isa_history");
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });
  const [selected, setSelected] = useState<VerificationResult | null>(null);

  return (
    <div className="max-w-4xl mx-auto pt-8">
      <h1 className="text-2xl font-bold mb-2">Verification History</h1>
      <p className="text-muted-foreground mb-6">
        Recent verification results (stored locally). Click a record to view details.
      </p>

      {history.length === 0 ? (
        <div className="border rounded-lg p-12 text-center text-muted-foreground">
          <p>No history yet. Run a verification to see results here.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {history.map((item, i) => (
            <Card
              key={i}
              className="cursor-pointer hover:border-primary/50 transition-colors"
              onClick={() => item.result && setSelected(item.result)}
            >
              <CardHeader className="pb-2 flex flex-row items-center justify-between">
                <CardTitle className="text-base font-mono">{item.instruction}</CardTitle>
                <Badge
                  variant={item.status === "PASS" ? "default" : "secondary"}
                  className={item.status === "PASS" ? "bg-green-600" : ""}
                >
                  {item.status}
                </Badge>
              </CardHeader>
              <CardContent className="text-xs text-muted-foreground">
                Score: {item.score.toFixed(0)}/100 · {new Date(item.timestamp).toLocaleString()}
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Dialog open={!!selected} onOpenChange={(open) => !open && setSelected(null)}>
        <DialogContent className="!max-w-4xl max-h-[90vh] overflow-auto">
          <DialogHeader>
            <DialogTitle>Verification Detail</DialogTitle>
            <DialogDescription>
              Full result for {selected?.instruction}
            </DialogDescription>
          </DialogHeader>
          {selected && <VerificationResultView result={selected} />}
        </DialogContent>
      </Dialog>
    </div>
  );
}
