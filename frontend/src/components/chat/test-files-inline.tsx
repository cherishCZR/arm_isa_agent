"use client";

import { cn } from "@/lib/utils";
import type { TestFileEntry } from "@/lib/api/types";
import { CodeBlockWithDl } from "./code-block-with-dl";

interface TestFilesInlineProps {
  files: TestFileEntry[];
  onDownload?: (entry: TestFileEntry) => void;
  className?: string;
}

export function TestFilesInline({ files, onDownload, className }: TestFilesInlineProps) {
  if (!files || files.length === 0) return null;

  return (
    <div className={cn("space-y-3", className)}>
      {files.slice(0, 5).map((entry) => (
        <CodeBlockWithDl key={entry.file_id} entry={entry} onDownload={onDownload} />
      ))}
      {files.length > 5 && (
        <p className="text-xs text-muted-foreground text-center py-1">
          + {files.length - 5} more test files
        </p>
      )}
    </div>
  );
}
