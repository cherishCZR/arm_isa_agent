"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

interface IssueTableProps {
  issues: Array<Record<string, unknown>>;
}

const SEVERITY_COLOR: Record<string, string> = {
  high: "bg-red-100 text-red-700",
  medium: "bg-yellow-100 text-yellow-700",
  low: "bg-blue-100 text-blue-700",
};

export function IssueTable({ issues }: IssueTableProps) {
  if (!issues.length) {
    return (
      <p className="text-sm text-green-600 font-medium">
        ✅ No issues found — all tests are clean.
      </p>
    );
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-12">#</TableHead>
          <TableHead className="w-20">Severity</TableHead>
          <TableHead className="w-28">Type</TableHead>
          <TableHead className="w-24">Dimension</TableHead>
          <TableHead>Description</TableHead>
          <TableHead>Suggestion</TableHead>
          <TableHead className="w-40">Location</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {issues.map((issue, i) => {
          const description = issue.description != null ? String(issue.description) : "";
          const suggestion = issue.suggestion != null ? String(issue.suggestion) : "";
          const location = issue.location != null ? String(issue.location) : "";

          return (
            <TableRow key={i}>
              <TableCell className="text-xs text-muted-foreground">{i + 1}</TableCell>
              <TableCell>
                <Badge
                  variant="outline"
                  className={`text-xs ${SEVERITY_COLOR[String(issue.severity || "low")] || ""}`}
                >
                  {String(issue.severity || "?")}
                </Badge>
              </TableCell>
              <TableCell className="font-mono text-xs">{String(issue.type || "?")}</TableCell>
              <TableCell className="text-xs text-muted-foreground">
                {String(issue.dimension || "-")}
              </TableCell>
              <TableCell className="text-sm max-w-sm whitespace-pre-wrap break-words" title={description}>
                {description || "—"}
              </TableCell>
              <TableCell
                className="text-sm text-muted-foreground max-w-sm whitespace-pre-wrap break-words"
                title={suggestion}
              >
                {suggestion || "No suggestion"}
              </TableCell>
              <TableCell className="text-xs text-muted-foreground max-w-xs truncate" title={location}>
                {location || "—"}
              </TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
}
