"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { TestFileTable } from "@/components/verification/test-file-table";
import { IssueTable } from "@/components/verification/issue-table";
import { CoverageView } from "@/components/verification/coverage-view";
import { ReasoningTimeline } from "@/components/verification/reasoning-timeline";
import type { VerificationResult } from "@/lib/api/types";
import { CheckCircle2, XCircle, AlertTriangle, Download, Copy } from "lucide-react";

interface ResultViewProps {
  result: VerificationResult;
}

const STATUS_CONFIG: Record<string, { icon: typeof CheckCircle2; color: string; label: string }> = {
  PASS:     { icon: CheckCircle2, color: "text-green-600", label: "PASS" },
  COMPILED: { icon: CheckCircle2, color: "text-green-600", label: "COMPILED" },
  REVIEWED: { icon: CheckCircle2, color: "text-green-600", label: "REVIEWED" },
  GENERATED: { icon: CheckCircle2, color: "text-green-600", label: "GENERATED" },
  FAIL:     { icon: XCircle,      color: "text-red-600",   label: "FAIL" },
  FAILED:   { icon: XCircle,      color: "text-red-600",   label: "FAILED" },
  REPAIRED: { icon: AlertTriangle, color: "text-yellow-600", label: "REPAIRED" },
  ERROR:    { icon: XCircle,      color: "text-red-600",   label: "ERROR" },
};

export function VerificationResultView({ result }: ResultViewProps) {
  const [copied, setCopied] = useState(false);
  const cfg = STATUS_CONFIG[result.status] || STATUS_CONFIG.ERROR;
  const Icon = cfg.icon;
  const safeScore = result.review_score ?? 0;
  const safeStageDetails = result.stage_details ?? [];
  const safeTestFiles = result.test_files ?? [];
  const safeIssues = result.issues ?? [];
  const safeCoverage = result.coverage ?? {};

  const handleCopyAll = async () => {
    const text = safeTestFiles.map((tf) => tf.content).join("\n\n");
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Summary Card */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <Icon className={`w-5 h-5 ${cfg.color}`} />
            <CardTitle className={`text-lg ${cfg.color}`}>{cfg.label}</CardTitle>
            <Badge variant="outline" className="ml-2">
              Score: {safeScore.toFixed(0)}/100
            </Badge>
          </div>
          <CardDescription>
            {(result.passing_tests ?? 0)} passing · {(result.failing_tests ?? 0)} failing ·{" "}
            {(result.total_tests ?? 0)} total · {((result.total_duration_ms ?? 0) as number).toFixed(0)}ms
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {(["planner", "retrieval", "llm", "generator", "reviewer", "compiler"] as const).map((s) => {
              const detail = safeStageDetails.find((d) => d.stage === s);
              const dur = detail?.duration_ms || 0;
              const skipped = detail?.status === "skipped";
              const label = s === "reviewer" ? "static" : s;
              return (
                <Badge
                  key={s}
                  variant={skipped ? "outline" : "secondary"}
                  className="font-mono text-xs"
                >
                  {label} {dur > 0 ? `${dur.toFixed(0)}ms` : skipped ? "(skip)" : ""}
                </Badge>
              );
            })}
          </div>

          {result.budget && (
            <div className="flex flex-wrap gap-2 mt-3 text-xs text-muted-foreground">
              <span>Total {result.budget.actual_instruction_count ?? result.budget.program_instruction_count}/{result.budget.program_instruction_count}</span>
              <span>Target occurrences {result.budget.target_instruction_count}</span>
              <span>Mode {result.generation_mode ?? "rule_based"}</span>
              {result.required_features?.length ? <span>Features {result.required_features.join(", ")}</span> : null}
              {result.canonical_targets?.map((target) => (
                <span key={target.key}>Target {target.key}{target.aliases.length > 1 ? ` (aliases: ${target.aliases.slice(1).join(", ")})` : ""}</span>
              ))}
            </div>
          )}

          <div className="flex gap-2 mt-4">
            <Button size="sm" variant="outline" onClick={handleCopyAll}>
              <Copy className="w-3 h-3 mr-1" />
              {copied ? "Copied!" : "Copy All"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Tabs defaultValue="reasoning" className="w-full">
        <TabsList>
          <TabsTrigger value="reasoning">Reasoning</TabsTrigger>
          <TabsTrigger value="files">
            Test Files ({safeTestFiles.length})
          </TabsTrigger>
          {result.scenario_plan && result.scenario_plan.length > 0 && (
            <TabsTrigger value="scenarios">
              Scenarios ({result.scenario_plan.length})
            </TabsTrigger>
          )}
          <TabsTrigger value="coverage">Coverage</TabsTrigger>
          <TabsTrigger value="issues">
            Issues ({safeIssues.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="reasoning" className="mt-4">
          <ReasoningTimeline stages={safeStageDetails} />
        </TabsContent>

        <TabsContent value="files" className="mt-4">
          <TestFileTable files={safeTestFiles} />
        </TabsContent>

        {result.scenario_plan && result.scenario_plan.length > 0 && (
          <TabsContent value="scenarios" className="mt-4 space-y-2">
            {result.scenario_plan.map((scenario) => (
              <div key={scenario.scenario_id} className="border rounded-md px-3 py-2 text-sm">
                <div className="flex items-center justify-between gap-3">
                  <span className="font-mono font-medium">{scenario.title}</span>
                  <div className="flex items-center gap-2 shrink-0">
                    <Badge variant="outline">.{scenario.format}</Badge>
                    <Badge variant={scenario.status === "compiled" ? "default" : "destructive"}>{scenario.status}</Badge>
                  </div>
                </div>
                <p className="text-xs text-muted-foreground mt-1">{scenario.reason}</p>
                {scenario.budget && (
                  <p className="text-xs font-mono text-muted-foreground mt-1">
                    total {scenario.budget.actual_instruction_count}/{scenario.budget.program_instruction_count}; target {scenario.budget.target_instruction_count}
                  </p>
                )}
              </div>
            ))}
          </TabsContent>
        )}

        <TabsContent value="coverage" className="mt-4">
          <CoverageView coverage={safeCoverage} />
        </TabsContent>

        <TabsContent value="issues" className="mt-4">
          <IssueTable issues={safeIssues} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
