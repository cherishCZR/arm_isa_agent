/** API client for the ARM ISA Verification backend. */

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

export const api = {
  /** POST /api/generate_testcase/stream — SSE stream for single instruction */
  generateTestcaseStreamUrl: () => `${API_BASE}/generate_testcase/stream`,

  /** POST /api/generate_testcases/stream — SSE stream for batch (per-instruction) */
  generateTestcasesStreamUrl: () => `${API_BASE}/generate_testcases/stream`,

  /** POST /api/scenario/stream — SSE stream for scenario batch (multi-instruction per program) */
  scenarioStreamUrl: () => `${API_BASE}/scenario/stream`,

  exploreTaxonomy: async () => {
    const res = await fetch(`${API_BASE}/explore/taxonomy`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  exploreVariants: async (params: { category?: string; search?: string; page?: number; pageSize?: number } = {}) => {
    const query = new URLSearchParams();
    if (params.category) query.set("category", params.category);
    if (params.search) query.set("search", params.search);
    if (params.page) query.set("page", String(params.page));
    if (params.pageSize) query.set("page_size", String(params.pageSize));
    const res = await fetch(`${API_BASE}/explore/variants?${query.toString()}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  exploreCategory: async (categoryId: string) => {
    const res = await fetch(`${API_BASE}/explore/categories/${encodeURIComponent(categoryId)}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  exploreSubcategory: async (categoryId: string, subcategoryId: string, params: { search?: string; page?: number; pageSize?: number } = {}) => {
    const query = new URLSearchParams();
    if (params.search) query.set("search", params.search);
    if (params.page) query.set("page", String(params.page));
    if (params.pageSize) query.set("page_size", String(params.pageSize));
    const res = await fetch(`${API_BASE}/explore/categories/${encodeURIComponent(categoryId)}/${encodeURIComponent(subcategoryId)}?${query.toString()}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  exploreInstruction: async (xmlId: string) => {
    const res = await fetch(`${API_BASE}/explore/instructions/${encodeURIComponent(xmlId)}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  exploreRelatedVariants: async (xmlId: string) => {
    const res = await fetch(`${API_BASE}/explore/instructions/${encodeURIComponent(xmlId)}/related`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  /** POST /api/scenario/parse — parse scenario text content */
  parseScenarioContent: async (content: string) => {
    const res = await fetch(`${API_BASE}/scenario/parse`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  /** POST /api/generate_testcase — sync (for scripts) */
  generateTestcase: async (
    instruction: string,
    useLlm = false,
    instructionCount = 100,
  ) => {
    const res = await fetch(`${API_BASE}/generate_testcase`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        instruction,
        use_llm: useLlm,
        instruction_count: instructionCount,
      }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  /** GET /api/testcase/{instruction}/{file_id} — download single file */
  getTestFile: async (instruction: string, fileId: string) => {
    const res = await fetch(`${API_BASE}/testcase/${instruction}/${fileId}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  /** POST /api/testcase/download-all – download all passing files as ZIP */
  downloadAllFiles: async (instruction: string, fileIds?: string[]) => {
    const res = await fetch(`${API_BASE}/testcase/download-all`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ instruction, file_ids: fileIds || null }),
    });
    if (!res.ok) throw new Error(await res.text());
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${instruction}_testcases.zip`;
    a.click();
    URL.revokeObjectURL(url);
  },
};
