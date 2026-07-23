"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Copy, Check, Download } from "lucide-react";
import type { TestFileEntry } from "@/lib/api/types";

interface CodeBlockWithDlProps {
  entry: TestFileEntry;
  onDownload?: (entry: TestFileEntry) => void;
  className?: string;
}

export function CodeBlockWithDl({ entry, onDownload, className }: CodeBlockWithDlProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(entry.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const lines = entry.content.split("\n");
  const previewLines = lines.slice(0, 20);
  const truncated = lines.length > 20;

  return (
    <div className={cn("rounded-lg border bg-card overflow-hidden", className)}>
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 bg-muted/50 border-b">
        <div className="flex items-center gap-2">
          <span
            className={cn(
              "w-2 h-2 rounded-full",
              entry.status === "pass" ? "bg-green-500" : "bg-red-500"
            )}
          />
          <code className="text-xs font-mono font-semibold">{entry.filename}</code>
          <span className="text-[10px] text-muted-foreground uppercase">{entry.format}</span>
          {entry.test_type && (
            <span className="text-[10px] bg-muted px-1.5 py-0.5 rounded">{entry.test_type}</span>
          )}
        </div>
        <div className="flex items-center gap-1">
          <Button size="icon" variant="ghost" className="h-7 w-7" onClick={handleCopy}>
            {copied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
          </Button>
          <Button
            size="icon"
            variant="ghost"
            className="h-7 w-7"
            onClick={() => onDownload?.(entry)}
          >
            <Download className="w-3 h-3" />
          </Button>
        </div>
      </div>

      {/* Code */}
      <pre className="p-3 overflow-x-auto text-xs font-mono leading-relaxed bg-muted/20">
        <code>
          {previewLines.join("\n")}
          {truncated && (
            <span className="block mt-1 text-muted-foreground italic">
              ... {lines.length - 20} more lines
            </span>
          )}
        </code>
      </pre>
    </div>
  );
}
