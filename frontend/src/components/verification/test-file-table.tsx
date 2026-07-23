"use client";

import { useMemo, useState } from "react";
import JSZip from "jszip";
import { saveAs } from "file-saver";
import { Download, Filter } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CopyButton } from "@/components/common/copy-button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { TestFileEntry } from "@/lib/api/types";

interface TestFileTableProps {
  files: TestFileEntry[];
}

type FilterStatus = "all" | "pass" | "fail";

export function TestFileTable({ files }: TestFileTableProps) {
  const [statusFilter, setStatusFilter] = useState<FilterStatus>("all");
  const [formatFilter, setFormatFilter] = useState<string>("all");

  const formats = useMemo(() => Array.from(new Set(files.map((f) => f.format))), [files]);

  const filtered = useMemo(() => {
    return files.filter((f) => {
      if (statusFilter !== "all" && f.status !== statusFilter) return false;
      if (formatFilter !== "all" && f.format !== formatFilter) return false;
      return true;
    });
  }, [files, statusFilter, formatFilter]);

  const handleDownloadSingle = (file: TestFileEntry) => {
    const blob = new Blob([file.content], { type: "text/plain;charset=utf-8" });
    saveAs(blob, file.filename);
  };

  const handleDownloadAll = async () => {
    const zip = new JSZip();
    const toDownload = statusFilter === "all" ? files : files.filter((f) => f.status === statusFilter);
    toDownload.forEach((f) => zip.file(f.filename, f.content));
    const blob = await zip.generateAsync({ type: "blob" });
    saveAs(blob, "testcases.zip");
  };

  return (
    <div>
      <div className="flex items-center gap-2 mb-3">
        <Filter className="w-3 h-3 text-muted-foreground" />
        <Badge
          variant={statusFilter === "all" ? "default" : "outline"}
          className="cursor-pointer text-xs"
          onClick={() => setStatusFilter("all")}
        >
          All ({files.length})
        </Badge>
        <Badge
          variant={statusFilter === "pass" ? "default" : "outline"}
          className="cursor-pointer text-xs bg-green-100 text-green-700 hover:bg-green-200"
          onClick={() => setStatusFilter("pass")}
        >
          Pass ({files.filter((f) => f.status === "pass").length})
        </Badge>
        <Badge
          variant={statusFilter === "fail" ? "default" : "outline"}
          className="cursor-pointer text-xs bg-red-100 text-red-700 hover:bg-red-200"
          onClick={() => setStatusFilter("fail")}
        >
          Fail ({files.filter((f) => f.status === "fail").length})
        </Badge>

        <div className="flex-1" />

        <select
          className="border rounded px-2 py-1 text-xs"
          value={formatFilter}
          onChange={(e) => setFormatFilter(e.target.value)}
        >
          <option value="all">All Formats</option>
          {formats.map((fmt) => (
            <option key={fmt} value={fmt}>
              .{fmt}
            </option>
          ))}
        </select>

        <Button size="sm" variant="outline" onClick={handleDownloadAll}>
          <Download className="w-3 h-3 mr-1" />
          ZIP
        </Button>
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-10">Status</TableHead>
            <TableHead>Filename</TableHead>
            <TableHead className="w-14">Format</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Description</TableHead>
            <TableHead className="w-24">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((f) => (
            <TableRow key={f.file_id}>
              <TableCell>
                {f.status === "pass" ? (
                  <Badge variant="outline" className="bg-green-100 text-green-700 text-xs px-1">
                    OK
                  </Badge>
                ) : (
                  <Badge variant="outline" className="bg-red-100 text-red-700 text-xs px-1">
                    FAIL
                  </Badge>
                )}
              </TableCell>
              <TableCell className="font-mono text-sm">{f.filename}</TableCell>
              <TableCell>
                <Badge variant="secondary" className="text-xs">
                  .{f.format}
                </Badge>
              </TableCell>
              <TableCell className="text-xs text-muted-foreground">{f.test_type}</TableCell>
              <TableCell className="text-xs text-muted-foreground max-w-40 truncate">
                {f.description}
              </TableCell>
              <TableCell>
                <div className="flex gap-1">
                  <CopyButton content={f.content} label="Copy" />
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDownloadSingle(f)}
                    title="Download file"
                  >
                    <Download className="w-3 h-3" />
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {filtered.length === 0 && (
        <p className="text-sm text-muted-foreground text-center py-8">
          No test files match the selected filters.
        </p>
      )}
    </div>
  );
}
