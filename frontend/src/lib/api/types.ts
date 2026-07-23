// ── SSE Event Types ──────────────────────────────────────

export type SSEEventName =
  | "stage_start"
  | "stage_progress"
  | "stage_complete"
  | "instruction_start"
  | "instruction_complete"
  | "batch_start"
  | "batch_complete"
  | "result"
  | "done";

export type PipelineStage =
  | "analyzer"
  | "planner"
  | "retrieval"
  | "splitter"
  | "llm"
  | "generator"
  | "compiler"
  | "reviewer"
  | "repair";

export type StageStatus =
  | "pending"
  | "running"
  | "completed"
  | "failed"
  | "ok"
  | "warning"
  | "error"
  | "skipped";

// ── SSE Event Payloads ────────────────────────────────────

export interface StageStartEvent {
  stage: PipelineStage;
  message: string;
  timestamp: number;
  instruction?: string;
}

export interface StageProgressEvent {
  stage: PipelineStage;
  detail: string;
  instruction?: string;
}

export interface StageCompleteEvent {
  stage: PipelineStage;
  status: StageStatus;
  duration_ms: number;
  summary: string;
  findings: string[];
  snapshot: Record<string, unknown>;
  instruction?: string;
}

// ── Data Models ───────────────────────────────────────────

export interface TestFileEntry {
  file_id: string;
  filename: string;
  format: "s" | "c" | "cpp" | "llvm";
  test_type: string;
  content: string;
  status: "pass" | "fail";
  description: string;
  issue_count: number;
}

export interface StageDetail {
  stage: PipelineStage;
  status: StageStatus;
  duration_ms: number;
  summary: string;
  reasoning: string;
  key_findings: string[];
  data_snapshot: Record<string, unknown>;
  error?: string;
}

export interface VerificationResult {
  instruction: string;
  status: "PASS" | "FAIL" | "REPAIRED" | "ERROR" | "GENERATED" | "REVIEWED" | "COMPILED" | "FAILED";
  review_score: number;
  total_tests: number;
  passing_tests: number;
  failing_tests: number;
  total_duration_ms: number;
  stage_details: StageDetail[];
  test_files: TestFileEntry[];
  coverage: Record<string, number>;
  issues: Array<Record<string, unknown>>;
  verification_level?: "generated" | "statically_reviewed" | "compiled";
  generated_status?: string;
  static_review_status?: string;
  compile_status?: string;
  compile_results?: Array<Record<string, unknown>>;
  resolved?: Array<Record<string, unknown>>;
  generation_mode?: "rule_based" | "llm";
  generation_trace?: string[];
  budget?: {
    program_instruction_count: number;
    target_instruction_count: number;
    actual_instruction_count: number;
    target_counts: Record<string, number>;
  };
  required_features?: string[];
  canonical_targets?: Array<{ key: string; query: string; aliases: string[] }>;
  scenario_plan?: Array<{
    scenario_id: string;
    title: string;
    format: string;
    reason: string;
    status: string;
    file_id?: string;
    budget?: { program_instruction_count: number; target_instruction_count: number; actual_instruction_count: number };
  }>;
}

// ── Pipeline Frontend State ───────────────────────────────

export interface StageUIState {
  status: StageStatus;
  message: string;
  detail?: string;
  duration_ms: number;
  summary: string;
  findings: string[];
}

export interface PipelineState {
  stages: Record<PipelineStage, StageUIState>;
  current_stage: PipelineStage | null;
  is_running: boolean;
  total_duration_ms: number;
}

// ── Batch State ───────────────────────────────────────────

export interface BatchInstructionState {
  instruction: string;
  status: "waiting" | "running" | "completed" | "error";
  result: VerificationResult | null;
  current_stage: PipelineStage | null;
  duration_ms: number;
  review_score: number;
}

export interface BatchState {
  instructions: BatchInstructionState[];
  active_index: number;
  completed: number;
  total: number;
  is_running: boolean;
  total_duration_ms: number;
}

// ── Scenario Batch State ──────────────────────────────────

export interface ScenarioState {
  /** The comma-separated label, e.g. "ADD,SUB,MOV" */
  label: string;
  /** Individual instruction mnemonics */
  instructions: string[];
  status: "waiting" | "running" | "completed" | "error";
  result: VerificationResult | null;
  current_stage: PipelineStage | null;
  duration_ms: number;
  review_score: number;
}

export interface ScenarioBatchState {
  scenarios: ScenarioState[];
  active_index: number;
  completed: number;
  total: number;
  is_running: boolean;
  total_duration_ms: number;
}

// ── Verification Parameters ───────────────────────────────

export interface VerificationParams {
  use_llm: boolean;
  instruction_count: number;
  target_instruction_count: number;
}

export const DEFAULT_VERIFICATION_PARAMS: VerificationParams = {
  use_llm: false,
  instruction_count: 100,
  target_instruction_count: 1,
};
