"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

interface CoverageViewProps {
  coverage: Record<string, number>;
}

const DIMENSION_LABELS: Record<string, string> = {
  normal: "Normal",
  boundary: "Boundary",
  encoding: "Encoding",
  alias: "Alias",
  invalid: "Invalid",
  feature: "Feature",
  overall: "Overall",
};

export function CoverageView({ coverage }: CoverageViewProps) {
  const data = Object.entries(coverage)
    .filter(([k]) => k !== "overall")
    .map(([key, value]) => ({
      dimension: DIMENSION_LABELS[key] || key,
      coverage: value,
    }));

  const overall = coverage.overall || 0;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
      {/* Radar Chart */}
      <Card className="lg:col-span-3">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm">Coverage Radar</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={280}>
            <RadarChart data={data}>
              <PolarGrid />
              <PolarAngleAxis dataKey="dimension" tick={{ fontSize: 12 }} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 10 }} />
              <Radar
                name="Coverage"
                dataKey="coverage"
                stroke="#2563eb"
                fill="#3b82f6"
                fillOpacity={0.2}
              />
              <Tooltip formatter={(v: unknown) => `${(v as number).toFixed(0)}%`} />
            </RadarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Bar Summary */}
      <Card className="lg:col-span-2">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm">Coverage Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {Object.entries(coverage).map(([key, value]) => (
              <div key={key}>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-muted-foreground">
                    {DIMENSION_LABELS[key] || key}
                  </span>
                  <span className="font-mono font-semibold">
                    {value.toFixed(0)}%
                  </span>
                </div>
                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className="h-2 rounded-full transition-all"
                    style={{
                      width: `${value}%`,
                      backgroundColor:
                        key === "overall"
                          ? "#3b82f6"
                          : value >= 80
                            ? "#22c55e"
                            : value >= 50
                              ? "#eab308"
                              : "#ef4444",
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
