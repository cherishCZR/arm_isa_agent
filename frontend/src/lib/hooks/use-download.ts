"use client";

import { useCallback } from "react";
import JSZip from "jszip";
import { saveAs } from "file-saver";
import type { TestFileEntry, VerificationResult } from "@/lib/api/types";

export function useDownload() {
  const downloadSingle = useCallback((entry: TestFileEntry) => {
    const blob = new Blob([entry.content], { type: "text/plain;charset=utf-8" });
    saveAs(blob, entry.filename);
  }, []);

  const downloadAllAsZip = useCallback(
    async (instruction: string, entries: TestFileEntry[], onlyPassing = true) => {
      const zip = new JSZip();
      const folder = zip.folder(instruction)!;
      const files = onlyPassing ? entries.filter((e) => e.status === "pass") : entries;
      files.forEach((e) => folder.file(e.filename, e.content));
      const blob = await zip.generateAsync({ type: "blob" });
      saveAs(blob, `${instruction}_testcases.zip`);
    },
    [],
  );

  const batchDownloadAsZip = useCallback(async (results: VerificationResult[]) => {
    const zip = new JSZip();
    results.forEach((r) => {
      const folder = zip.folder(r.instruction)!;
      r.test_files.filter((f) => f.status === "pass").forEach((f) => folder.file(f.filename, f.content));
    });
    const blob = await zip.generateAsync({ type: "blob" });
    const date = new Date().toISOString().slice(0, 10);
    saveAs(blob, `arm_testcases_${date}.zip`);
  }, []);

  const copyToClipboard = useCallback(async (content: string): Promise<boolean> => {
    try {
      await navigator.clipboard.writeText(content);
      return true;
    } catch {
      return false;
    }
  }, []);

  return { downloadSingle, downloadAllAsZip, batchDownloadAsZip, copyToClipboard };
}
