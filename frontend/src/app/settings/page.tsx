"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function SettingsPage() {
  return (
    <div className="max-w-4xl mx-auto pt-8">
      <h1 className="text-2xl font-bold mb-2">Settings</h1>
      <p className="text-muted-foreground mb-6">Configure the ARM ISA Verification Agent.</p>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">API Configuration</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-muted-foreground">Backend URL</span>
            <code className="font-mono">{process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000"}</code>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">Version</span>
            <code className="font-mono">0.1.0</code>
          </div>
          <p className="text-xs text-muted-foreground mt-4">
            Set NEXT_PUBLIC_API_BASE environment variable to change the backend URL.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
