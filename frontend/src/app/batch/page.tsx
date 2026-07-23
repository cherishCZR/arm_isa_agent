"use client";

import { useRef, useState } from "react";
import JSZip from "jszip";
import {
  AlertTriangle,
  CheckCircle2,
  Download,
  FileText,
  Loader2,
  Play,
  Settings2,
  Trash2,
  Upload,
  XCircle,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { IssueTable } from "@/components/verification/issue-table";
import { PipelineProgress } from "@/components/pipeline/pipeline-progress";
import { useScenarioBatchVerification } from "@/lib/hooks/use-batch-verification";
import { useDownload } from "@/lib/hooks/use-download";
import type { ScenarioState, VerificationParams } from "@/lib/api/types";
import { DEFAULT_VERIFICATION_PARAMS } from "@/lib/api/types";

type ParsedScenario = { label: string; instructions: string[] };

const SUCCESS_STATUSES = new Set(["PASS", "REPAIRED", "GENERATED", "REVIEWED", "COMPILED"]);

function isSuccessfulStatus(status?: string): boolean {
  return Boolean(status && SUCCESS_STATUSES.has(status));
}

function parseScenarioText(text: string, useLlm = false): ParsedScenario[] {
  return text
    .split(/\r?\n/)
    .map((line) => {
      if (useLlm) {
        const prompt = line.trim();
        return prompt ? { label: prompt, instructions: [prompt] } : null;
      }
      const instructions = line
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);
      return instructions.length ? { label: instructions.join(","), instructions } : null;
    })
    .filter((item): item is ParsedScenario => item !== null);
}

async function parseScenarioFile(file: File): Promise<string> {
  const name = file.name.toLowerCase();
  if (!name.endsWith(".xlsx")) {
    return file.text();
  }

  const zip = await JSZip.loadAsync(await file.arrayBuffer());
  const sharedXml = await zip.file("xl/sharedStrings.xml")?.async("text");
  const sharedStrings: string[] = [];
  if (sharedXml) {
    const doc = new DOMParser().parseFromString(sharedXml, "application/xml");
    doc.querySelectorAll("si").forEach((si) => {
      sharedStrings.push(
        Array.from(si.querySelectorAll("t"))
          .map((t) => t.textContent ?? "")
          .join(""),
      );
    });
  }

  const workbookRels = await zip.file("xl/_rels/workbook.xml.rels")?.async("text");
  let firstSheetPath = "xl/worksheets/sheet1.xml";
  if (workbookRels) {
    const relDoc = new DOMParser().parseFromString(workbookRels, "application/xml");
    const rel = relDoc.querySelector("Relationship[Type$='/worksheet']");
    const target = rel?.getAttribute("Target");
    if (target) {
      firstSheetPath = target.startsWith("/") ? target.slice(1) : `xl/${target}`;
    }
  }

  const sheetXml = await zip.file(firstSheetPath)?.async("text");
  if (!sheetXml) return "";

  const sheetDoc = new DOMParser().parseFromString(sheetXml, "application/xml");
  const rows: string[] = [];
  sheetDoc.querySelectorAll("sheetData row").forEach((row) => {
    const cells: string[] = [];
    row.querySelectorAll("c").forEach((cell) => {
      const type = cell.getAttribute("t");
      const raw = cell.querySelector("v")?.textContent ?? "";
      let value = raw;
      if (type === "s") value = sharedStrings[Number(raw)] ?? "";
      if (type === "inlineStr") value = cell.querySelector("is t")?.textContent ?? "";
      if (value.trim()) cells.push(value.trim());
    });
    if (cells.length) rows.push(cells.join(","));
  });
  return rows.join("\n");
}

export default function BatchPage() {
  const [inputMode, setInputMode] = useState<"text" | "file">("text");
  const [textInput, setTextInput] = useState("");
  const [uploadedFileName, setUploadedFileName] = useState("");
  const [parsedScenarios, setParsedScenarios] = useState<ParsedScenario[]>([]);
  const [started, setStarted] = useState(false);
  const [selectedScenarioIdx, setSelectedScenarioIdx] = useState<number | null>(null);
  const [params, setParams] = useState<VerificationParams>(DEFAULT_VERIFICATION_PARAMS);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const {
    scenarios: batchScenarios,
    activeIndex,
    completed,
    total,
    isRunning,
    totalDurationMs,
    currentPipeline,
    startBatch,
    stopBatch,
  } = useScenarioBatchVerification();
  const { downloadSingle, batchDownloadAsZip } = useDownload();

  const handleTextChange = (value: string) => {
    setTextInput(value);
    setParsedScenarios(parseScenarioText(value, params.use_llm));
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setUploadedFileName(file.name);
    const content = await parseScenarioFile(file);
    setTextInput(content);
    setParsedScenarios(parseScenarioText(content, params.use_llm));
  };

  const handleLlmToggle = () => {
    const nextUseLlm = !params.use_llm;
    setParams((prev) => ({ ...prev, use_llm: nextUseLlm }));
    setParsedScenarios(parseScenarioText(textInput, nextUseLlm));
  };

  const handleDownloadScenario = (scenario: ScenarioState) => {
    const file = scenario.result?.test_files?.find((entry) => entry.status === "pass");
    if (file) downloadSingle(file);
  };

  const handleStart = async () => {
    if (parsedScenarios.length === 0) return;
    setStarted(true);
    setSelectedScenarioIdx(null);
    await startBatch(parsedScenarios, params);
  };

  const handleReset = () => {
    setTextInput("");
    setUploadedFileName("");
    setParsedScenarios([]);
    setStarted(false);
    setSelectedScenarioIdx(null);
  };

  if (!started) {
    return (
      <div className="max-w-2xl mx-auto pt-12">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2">Scenario Batch Verification</h1>
          <p className="text-muted-foreground text-sm max-w-md mx-auto">
            {params.use_llm ? "One line is one descriptive assembly-generation request." : "One line is one assembly test program. Instructions on the same line are split by commas."}
          </p>
        </div>

        <div className="flex gap-1 mb-4 bg-muted rounded-lg p-1">
          {(["text", "file"] as const).map((mode) => (
            <button
              key={mode}
              type="button"
              onClick={() => setInputMode(mode)}
              className={`flex-1 py-1.5 rounded-md text-sm font-medium transition-colors ${
                inputMode === mode ? "bg-background shadow-sm" : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <span className="flex items-center justify-center gap-1">
                {mode === "text" ? <FileText className="w-3.5 h-3.5" /> : <Upload className="w-3.5 h-3.5" />}
                {mode === "text" ? "Text Input" : "File Upload"}
              </span>
            </button>
          ))}
        </div>

        {inputMode === "text" ? (
          <textarea
            value={textInput}
            onChange={(event) => handleTextChange(event.target.value)}
            placeholder={params.use_llm ? "Generate ADD immediate and shifted-register cases\nCreate an SVE ADD test program" : "ADD,sub,mov\naddp sve, ldp\ncmp,b.cond,b"}
            rows={8}
            className="w-full rounded-md border bg-background px-3 py-2 font-mono text-sm resize-y min-h-[160px] focus:outline-none focus:ring-2 focus:ring-primary/30"
            autoFocus
          />
        ) : (
          <div
            className="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer hover:border-primary/50 transition-colors"
            onClick={() => fileInputRef.current?.click()}
          >
            <Upload className="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
            <p className="text-sm text-muted-foreground">
              {uploadedFileName ? `Loaded: ${uploadedFileName}` : "Click to upload .txt, .csv, or .xlsx file"}
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              {params.use_llm ? "One row per descriptive generation request." : "One row per scenario, comma-separated instructions."}
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept=".txt,.csv,.xlsx"
              onChange={handleFileUpload}
              className="hidden"
            />
          </div>
        )}

        {parsedScenarios.length > 0 && (
          <div className="mt-4">
            <p className="text-xs text-muted-foreground mb-2">Parsed {parsedScenarios.length} scenario(s):</p>
            <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
              {parsedScenarios.map((scenario, index) => (
                <Badge key={`${scenario.label}-${index}`} variant="outline" className="text-xs font-mono">
                  <span className="text-muted-foreground mr-1">#{index + 1}</span>
                  {scenario.label}
                </Badge>
              ))}
            </div>
          </div>
        )}

        <div className="mt-4">
          <button
            type="button"
            onClick={() => setShowAdvanced((value) => !value)}
            className="flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <Settings2 className="w-4 h-4" />
            Advanced Options
            <span className="text-xs">{showAdvanced ? "up" : "down"}</span>
          </button>
        </div>

        {showAdvanced && (
          <Card className="mt-2 mb-4">
            <CardContent className="pt-4 space-y-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-medium">Total instructions per assembly program</label>
                <div className="flex items-center gap-2">
                  <input
                    type="range"
                    min={1}
                    max={1000}
                    step={1}
                    value={params.instruction_count}
                    onChange={(event) =>
                      setParams((prev) => ({
                        ...prev,
                        instruction_count: Number(event.target.value),
                        target_instruction_count: Math.min(prev.target_instruction_count, Number(event.target.value)),
                      }))
                    }
                    className="flex-1 h-2 accent-primary"
                  />
                  <input
                    type="number"
                    min={1}
                    max={10000}
                    value={params.instruction_count}
                    onChange={(event) =>
                      setParams((prev) => ({
                        ...prev,
                        instruction_count: Math.max(1, Math.min(10000, Number(event.target.value) || 1)),
                        target_instruction_count: Math.min(prev.target_instruction_count, Math.max(1, Math.min(10000, Number(event.target.value) || 1))),
                      }))
                    }
                    className="w-20 rounded-md border px-2 py-1 text-sm text-center"
                  />
                </div>
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-medium">Occurrences of each target instruction</label>
                <div className="flex items-center gap-2">
                  <input
                    type="range"
                    min={1}
                    max={params.instruction_count}
                    step={1}
                    value={params.target_instruction_count}
                    onChange={(event) => setParams((prev) => ({ ...prev, target_instruction_count: Number(event.target.value) }))}
                    className="flex-1 h-2 accent-primary"
                  />
                  <input
                    type="number"
                    min={1}
                    max={params.instruction_count}
                    value={params.target_instruction_count}
                    onChange={(event) => setParams((prev) => ({ ...prev, target_instruction_count: Math.max(1, Math.min(prev.instruction_count, Number(event.target.value) || 1)) }))}
                    className="w-20 rounded-md border px-2 py-1 text-sm text-center"
                  />
                </div>
                <p className="text-xs text-muted-foreground">Every resolved target in this scenario must appear this many times.</p>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium">Use LLM for test generation</label>
                  <p className="text-xs text-muted-foreground">Enable LLM-assisted generation when configured.</p>
                </div>
                <button
                  type="button"
                  role="switch"
                  aria-checked={params.use_llm}
                  onClick={handleLlmToggle}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    params.use_llm ? "bg-primary" : "bg-muted-foreground/30"
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 rounded-full bg-white transition-transform ${
                      params.use_llm ? "translate-x-6" : "translate-x-1"
                    }`}
                  />
                </button>
              </div>
            </CardContent>
          </Card>
        )}

        <Button
          size="lg"
          onClick={handleStart}
          disabled={parsedScenarios.length === 0}
          className="w-full mt-2"
        >
          <Play className="w-4 h-4 mr-2" />
          Start Batch ({parsedScenarios.length} scenario{parsedScenarios.length > 1 ? "s" : ""})
        </Button>

        <div className="mt-6">
          <p className="text-xs text-muted-foreground mb-2">Quick examples:</p>
          <div className="grid grid-cols-1 gap-2">
            {[
              { label: "Basic arithmetic", text: "ADD,sub,mov\nADD imm,ADD shift" },
              { label: "Memory and branch", text: "LDR,STR\ncmp,b.cond,b" },
              { label: "SVE hints", text: "ADD sve,ADDP sve\nLD1 sve,ST1 sve" },
            ].map((example) => (
              <Button
                key={example.label}
                variant="outline"
                size="sm"
                onClick={() => handleTextChange(example.text)}
                className="justify-start font-mono text-xs h-auto py-2"
              >
                <span className="text-muted-foreground mr-2 font-sans">{example.label}:</span>
                {example.text.replace(/\n/g, " | ")}
              </Button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const downloadable = batchScenarios.filter(
    (scenario) => isSuccessfulStatus(scenario.result?.status) && scenario.result?.test_files?.length,
  );

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-bold">Scenario Batch Verification</h1>
          <p className="text-sm text-muted-foreground">
            {total} scenarios | {completed} completed
            {totalDurationMs > 0 && ` | ${(totalDurationMs / 1000).toFixed(1)}s`}
          </p>
        </div>
        <div className="flex gap-2">
          {isRunning ? (
            <Button variant="outline" size="sm" onClick={stopBatch}>
              Cancel
            </Button>
          ) : (
            <>
              <Button variant="outline" size="sm" onClick={handleReset}>
                <Trash2 className="w-3 h-3 mr-1" />
                New Batch
              </Button>
              {downloadable.length > 0 && (
                <Button size="sm" onClick={() => batchDownloadAsZip(downloadable.map((item) => item.result!))}>
                  <Download className="w-3 h-3 mr-1" />
                  Download All
                </Button>
              )}
            </>
          )}
        </div>
      </div>

      {isRunning && batchScenarios[activeIndex] && currentPipeline && (
        <div className="mb-6">
          <PipelineProgress pipeline={currentPipeline} instruction={batchScenarios[activeIndex]?.label} />
        </div>
      )}

      <div className="space-y-3">
        {batchScenarios.map((scenario, index) => {
          const result = scenario.result;
          const isSelected = selectedScenarioIdx === index;
          const isSuccess = isSuccessfulStatus(result?.status);
          const isFail = Boolean(result && !isSuccess);
          const hasFiles = Boolean(result?.test_files?.length);
          const hasIssues = isFail && Boolean(result?.issues?.length);
          const isActive = index === activeIndex;

          let statusIcon: React.ReactNode = (
            <span className="w-4 h-4 inline-block rounded-full border border-muted-foreground/30" />
          );
          let statusColor = "";
          if (scenario.status === "running") {
            statusIcon = <Loader2 className="w-4 h-4 animate-spin text-blue-500" />;
            statusColor = "border-blue-200 dark:border-blue-800";
          } else if (result) {
            statusIcon = isSuccess ? (
              <CheckCircle2 className="w-4 h-4 text-green-500" />
            ) : (
              <XCircle className="w-4 h-4 text-red-500" />
            );
            statusColor = isSuccess ? "border-green-200 dark:border-green-800" : "border-red-200 dark:border-red-800";
          } else if (scenario.status === "error") {
            statusIcon = <AlertTriangle className="w-4 h-4 text-yellow-500" />;
            statusColor = "border-yellow-200 dark:border-yellow-800";
          }

          return (
            <Card
              key={`${scenario.label}-${index}`}
              className={`${isActive ? "ring-2 ring-primary/40" : ""} ${statusColor} ${isSelected ? "shadow-md" : ""}`}
            >
              <CardContent className="p-4">
                <div className="flex items-center justify-between gap-3">
                  <div className="flex items-center gap-3 min-w-0">
                    <span className="text-xs text-muted-foreground font-mono w-6 shrink-0">#{index + 1}</span>
                    {statusIcon}
                    <button
                      type="button"
                      onClick={() => setSelectedScenarioIdx(isSelected ? null : index)}
                      className="text-left min-w-0"
                    >
                      <code className="font-mono font-semibold text-sm block truncate max-w-[360px]">
                        {scenario.label}
                      </code>
                      <span className="text-xs text-muted-foreground">
                        {scenario.instructions.length} instruction{scenario.instructions.length > 1 ? "s" : ""}
                        {result && ` | Score ${result.review_score.toFixed(0)}`}
                        {result && ` | ${result.total_tests} tests`}
                        {result?.verification_level && ` | ${result.verification_level}`}
                      </span>
                    </button>
                  </div>

                  <div className="flex items-center gap-1.5 shrink-0">
                    {result && (
                      <Badge variant={isFail ? "destructive" : "default"} className="text-xs">
                        {result.status}
                      </Badge>
                    )}
                    {hasFiles && !isRunning && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(event) => {
                          event.stopPropagation();
                          handleDownloadScenario(scenario);
                        }}
                        title="Download test file"
                      >
                        <Download className="w-3.5 h-3.5" />
                      </Button>
                    )}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setSelectedScenarioIdx(isSelected ? null : index)}
                      className="text-xs"
                    >
                      {isSelected ? "Hide" : "Details"}
                    </Button>
                  </div>
                </div>

                {isSelected && result && (
                  <div className="mt-4 pt-4 border-t space-y-3">
                    <div>
                      <p className="text-xs font-semibold mb-1.5">Verification Layers</p>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                        {[
                          ["generated", result.generated_status ?? "NOT_STARTED"],
                          ["static review", result.static_review_status ?? "NOT_STARTED"],
                          ["compile", result.compile_status ?? "NOT_STARTED"],
                        ].map(([label, value]) => (
                          <div
                            key={label}
                            className="flex items-center justify-between text-xs px-2 py-1 rounded bg-muted/50"
                          >
                            <span className="text-muted-foreground">{label}</span>
                            <Badge variant={value === "FAIL" ? "destructive" : "outline"} className="text-xs">
                              {value}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    </div>

                    {result.budget && (
                      <div>
                        <p className="text-xs font-semibold mb-1.5">Generation Summary</p>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-1 text-xs">
                          <div className="flex justify-between px-2 py-1 rounded bg-muted/50">
                            <span className="text-muted-foreground">Mode</span>
                            <span className="font-mono">{result.generation_mode ?? "rule_based"}</span>
                          </div>
                          <div className="flex justify-between px-2 py-1 rounded bg-muted/50">
                            <span className="text-muted-foreground">Instruction budget</span>
                            <span className="font-mono">{result.budget.actual_instruction_count}/{result.budget.program_instruction_count}</span>
                          </div>
                          <div className="flex justify-between px-2 py-1 rounded bg-muted/50">
                            <span className="text-muted-foreground">Target occurrence requirement</span>
                            <span className="font-mono">{result.budget.target_instruction_count}</span>
                          </div>
                          <div className="flex justify-between px-2 py-1 rounded bg-muted/50">
                            <span className="text-muted-foreground">Actual target counts</span>
                            <span className="font-mono truncate">
                              {Object.entries(result.budget.target_counts).map(([key, value]) => `${key}=${value}`).join(", ") || "none"}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {result.generation_trace && result.generation_trace.length > 0 && (
                      <div>
                        <p className="text-xs font-semibold mb-1.5">Generation Trace</p>
                        <div className="space-y-1">
                          {result.generation_trace.map((entry, traceIndex) => (
                            <div key={`${traceIndex}-${entry}`} className="font-mono text-xs px-2 py-1 rounded bg-muted/50 break-words">
                              {entry}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {result.resolved && result.resolved.length > 0 && (
                      <div>
                        <p className="text-xs font-semibold mb-1.5">Resolved Instructions</p>
                        <div className="space-y-1">
                          {result.resolved.map((item, resolvedIndex) => (
                            <div
                              key={`${String(item.query ?? item.mnemonic ?? resolvedIndex)}-${resolvedIndex}`}
                              className="flex items-center justify-between gap-2 text-xs px-2 py-1 rounded bg-muted/50"
                            >
                              <span className="font-mono truncate">{String(item.query ?? item.mnemonic ?? "")}</span>
                              <span className="font-mono text-muted-foreground truncate">
                                {String(item.xml_id ?? item.instruction_id ?? item.status ?? "")}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {result.test_files && result.test_files.length > 0 && (
                      <div>
                        <p className="text-xs font-semibold mb-1.5">Test Files</p>
                        <div className="space-y-1">
                          {result.test_files.map((file) => (
                            <div
                              key={file.file_id}
                              className="flex items-center justify-between text-xs px-2 py-1 rounded bg-muted/50"
                            >
                              <span className="font-mono">{file.filename ?? file.file_id}</span>
                              <div className="flex items-center gap-2">
                                <Badge variant="outline" className="text-xs">
                                  {file.test_type ?? "unknown"}
                                </Badge>
                                <span className={file.status === "pass" ? "text-green-600" : "text-red-600"}>
                                  {file.status}
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {result.compile_results && result.compile_results.length > 0 && (
                      <div>
                        <p className="text-xs font-semibold mb-1.5">Compile Results</p>
                        <div className="space-y-1">
                          {result.compile_results.map((item, compileIndex) => (
                            <div
                              key={`${String(item.file_id ?? compileIndex)}-${compileIndex}`}
                              className="flex items-center justify-between gap-2 text-xs px-2 py-1 rounded bg-muted/50"
                            >
                              <span className="font-mono truncate">{String(item.filename ?? item.file_id ?? "")}</span>
                              <span className="font-mono text-muted-foreground">{String(item.status ?? "")}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {hasIssues && (
                      <div>
                        <p className="text-xs font-semibold mb-1.5 text-red-600">Reviewer Issues</p>
                        <IssueTable issues={result.issues || []} />
                      </div>
                    )}

                    {result.coverage && Object.keys(result.coverage).length > 0 && (
                      <div>
                        <p className="text-xs font-semibold mb-1.5">Coverage</p>
                        <div className="grid grid-cols-2 gap-1">
                          {Object.entries(result.coverage).map(([key, value]) => (
                            <div key={key} className="text-xs flex justify-between px-1">
                              <span className="text-muted-foreground capitalize">{key}</span>
                              <span className="font-mono">{String(value)}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
