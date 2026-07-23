"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { PipelineProgress } from "@/components/pipeline/pipeline-progress";
import { useVerificationSSE } from "@/lib/hooks/use-verification-sse";
import { VerificationResultView } from "@/components/verification/result-view";
import { Play, Loader2, Settings2 } from "lucide-react";
import type { VerificationParams } from "@/lib/api/types";
import { DEFAULT_VERIFICATION_PARAMS } from "@/lib/api/types";

export default function VerifyPage() {
  const [instruction, setInstruction] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [params, setParams] = useState<VerificationParams>(DEFAULT_VERIFICATION_PARAMS);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const { pipeline, result, error, isRunning, startVerification, cancel, reset } = useVerificationSSE();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const ins = params.use_llm ? instruction.trim() : instruction.trim().toUpperCase();
    if (!ins) return;
    setSubmitted(true);
    await startVerification(ins, params);
  };

  const handleReset = () => {
    setInstruction("");
    setSubmitted(false);
    reset();
  };

  // Single-instruction input form
  if (!submitted || (!isRunning && !result && !error)) {
    return (
      <div className="max-w-2xl mx-auto pt-16">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2">ARM ISA Compiler Verification</h1>
          <p className="text-muted-foreground">
            {params.use_llm ? "Describe the AArch64 assembly program to generate and verify." : "Enter an ARM A64 instruction mnemonic to run the verification pipeline."}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="flex gap-3 mb-4">
          <Input
            placeholder={params.use_llm ? "Describe a program, e.g. generate ADD immediate and ADD shift cases" : "Enter instruction, e.g. ADD, ADD imm, ADD sve..."}
            value={instruction}
            onChange={(e) => setInstruction(params.use_llm ? e.target.value : e.target.value.toUpperCase())}
            className="font-mono text-lg h-12"
            maxLength={params.use_llm ? 1000 : 80}
            autoFocus
          />
          <Button type="submit" size="lg" disabled={!instruction.trim()}>
            <Play className="w-4 h-4 mr-1" />
            Verify
          </Button>
        </form>

        {/* ── Advanced options toggle ── */}
        <div className="mb-4">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <Settings2 className="w-4 h-4" />
            Advanced Options
            <span className="text-xs">{showAdvanced ? "▲" : "▼"}</span>
          </button>
        </div>

        {showAdvanced && (
          <Card className="mb-6">
            <CardContent className="pt-4 space-y-4">
              {/* Instruction count */}
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-medium">
                  Total instructions per assembly program
                </label>
                <div className="flex items-center gap-2">
                  <input
                    type="range"
                    min={10}
                    max={1000}
                    step={10}
                    value={params.instruction_count}
                    onChange={(e) =>
                      setParams((p) => ({ ...p, instruction_count: Number(e.target.value), target_instruction_count: Math.min(p.target_instruction_count, Number(e.target.value)) }))
                    }
                    className="flex-1 h-2 accent-primary"
                  />
                  <input
                    type="number"
                    min={1}
                    max={10000}
                    value={params.instruction_count}
                    onChange={(e) =>
                      setParams((p) => ({
                        ...p,
                        instruction_count: Math.max(1, Math.min(10000, Number(e.target.value) || 100)),
                        target_instruction_count: Math.min(p.target_instruction_count, Math.max(1, Math.min(10000, Number(e.target.value) || 100))),
                      }))
                    }
                    className="w-20 rounded-md border px-2 py-1 text-sm text-center"
                  />
                </div>
                <p className="text-xs text-muted-foreground">
                  Target number of instruction instances per generated test program (1–10000, default 100).
                </p>
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
                    onChange={(e) => setParams((p) => ({ ...p, target_instruction_count: Number(e.target.value) }))}
                    className="flex-1 h-2 accent-primary"
                  />
                  <input
                    type="number"
                    min={1}
                    max={params.instruction_count}
                    value={params.target_instruction_count}
                    onChange={(e) => setParams((p) => ({ ...p, target_instruction_count: Math.max(1, Math.min(p.instruction_count, Number(e.target.value) || 1)) }))}
                    className="w-20 rounded-md border px-2 py-1 text-sm text-center"
                  />
                </div>
                <p className="text-xs text-muted-foreground">Must not exceed the total program instruction count.</p>
              </div>

              {/* Use LLM toggle */}
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium">Use LLM for test generation</label>
                  <p className="text-xs text-muted-foreground">
                    Enable LLM-assisted generation (slower, potentially higher quality).
                  </p>
                </div>
                <button
                  type="button"
                  role="switch"
                  aria-checked={params.use_llm}
                  onClick={() => setParams((p) => ({ ...p, use_llm: !p.use_llm }))}
                  className={`
                    relative inline-flex h-6 w-11 items-center rounded-full transition-colors
                    ${params.use_llm ? "bg-primary" : "bg-muted-foreground/30"}
                  `}
                >
                  <span
                    className={`
                      inline-block h-4 w-4 rounded-full bg-white transition-transform
                      ${params.use_llm ? "translate-x-6" : "translate-x-1"}
                    `}
                  />
                </button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Instruction suggestions */}
        <div className="mt-6 grid grid-cols-2 gap-3">
          {["ADD", "LDR", "MADD", "STP"].map((ins) => (
            <Card
              key={ins}
              className="cursor-pointer hover:border-primary/50 transition-colors"
              onClick={() => setInstruction(ins)}
            >
              <CardContent className="p-3">
                <code className="text-sm font-mono font-semibold">{ins}</code>
                <p className="text-xs text-muted-foreground mt-1">Click to try</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  // Pipeline running or result ready
  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-bold">
            Verification: <code className="font-mono text-primary">{instruction}</code>
          </h1>
          {isRunning && <Loader2 className="w-4 h-4 animate-spin text-blue-500" />}
        </div>
        <div className="flex gap-2">
          {isRunning && (
            <Button variant="outline" size="sm" onClick={cancel}>
              Cancel
            </Button>
          )}
          {!isRunning && (
            <Button variant="outline" size="sm" onClick={handleReset}>
              New
            </Button>
          )}
        </div>
      </div>

      {/* Pipeline Progress */}
      <PipelineProgress
        pipeline={pipeline}
        instruction={instruction}
        className="mb-6"
      />

      {/* Error */}
      {error && (
        <Card className="mb-6 border-red-200 bg-red-50 dark:bg-red-950/20">
          <CardHeader className="pb-2">
            <CardTitle className="text-red-700 text-base">Verification Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-red-600 font-mono">{error}</p>
          </CardContent>
        </Card>
      )}

      {/* Result */}
      {result && !isRunning && (
        <VerificationResultView result={result} />
      )}
    </div>
  );
}
